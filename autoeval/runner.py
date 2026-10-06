"""Append-only execution records and a frozen manifest for each run."""
import json
import platform
import random
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .core import PROTOCOL_VERSION, corpus, digest, make_prompt, score_response, validate_corpus, write_json
from .providers import Ollama, regex_baseline


def run(root, models, split="dev", repeats=1, base_url="http://127.0.0.1:11434", baseline=False, timeout=180):
    root = Path(root)
    validate_corpus(root)
    if not 1 <= repeats <= 10:
        raise ValueError("repeats must be between 1 and 10")
    if not models and not baseline:
        raise ValueError("Choose at least one model or --baseline")
    if len(set(models)) != len(models):
        raise ValueError("Duplicate models")
    if split not in {"dev", "pilot"}:
        raise ValueError("Unknown split")
    manifest, docs, all_cases = corpus(root)
    cases = [c for c in all_cases if c["split"] == split]
    provider = Ollama(base_url, timeout)
    identities = [provider.identity(m) for m in models]  # Fail before creating a run if unavailable.
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    run_dir = root / "data/runs" / run_id
    run_dir.mkdir(parents=True)
    # Snapshot enough input to interpret a run even if the working corpus is edited later.
    frozen = {"run_id":run_id,"protocol_version":PROTOCOL_VERSION,"created_at":datetime.now(timezone.utc).isoformat(),
              "split":split,"repeats":repeats,"models":identities,"baseline":baseline,
              "corpus_hash":digest(manifest),"cases_hash":digest(all_cases),"manifest":manifest,
              "cases":cases,"documents":docs,"environment":{"python":platform.python_version(),"platform":platform.platform(),
              "machine":platform.machine()},"execution_policy":"sequential, no retries, temperature 0.2, seeds 41+repeat",
              "reference_review":"pending independent human validation","status":"running"}
    write_json(run_dir / "manifest.json", frozen)
    total = len(cases) * len(models) * repeats + (sum(c["task"] == "extraction" for c in cases) if baseline else 0)
    count, errors = 0, 0
    try:
        with (run_dir / "results.jsonl").open("a", encoding="utf-8") as output:
            def record(row):
                nonlocal count, errors
                output.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                output.flush()
                count += 1
                errors += row["status"] != "ok"
                print(f"[{count}/{total}] {row['model']} {row['case_id']} #{row['repeat']}: {row['status']}", flush=True)

            if baseline:
                for case in cases:
                    if case["task"] != "extraction":
                        continue
                    doc = docs[case["source_id"]]
                    start = time.perf_counter()
                    raw = regex_baseline(case, doc)
                    record({"run_id":run_id,"model":"regex-labels-v1","provider":"rules","case_id":case["id"],
                      "task":case["task"],"repeat":0,"status":"ok","raw_response":raw,
                      "metrics":{"latency_s":time.perf_counter()-start,"api_cost_eur":0,"energy_cost_eur":None},
                      "score":score_response(raw,case,doc)})
            # Alternate model order between repetitions; randomize cases with a fixed seed.
            for repetition in range(repeats):
                order = identities if repetition % 2 == 0 else list(reversed(identities))
                for identity in order:
                    selected = cases[:]
                    random.Random(41 + repetition).shuffle(selected)
                    for case in selected:
                        doc = docs[case["source_id"]]
                        messages = make_prompt(case, doc)
                        row = {"run_id":run_id,"model":identity["name"],"provider":"ollama",
                               "model_digest":identity["digest"],"case_id":case["id"],"task":case["task"],
                               "repeat":repetition,"seed":41+repetition,"prompt":messages,"prompt_hash":digest(messages),
                               "started_at":datetime.now(timezone.utc).isoformat()}
                        started = time.perf_counter()
                        try:
                            generation = provider.generate(identity["name"],messages,41+repetition,
                                                           "thinking" in identity["capabilities"])
                            row.update(generation)
                            row["status"] = "truncated" if generation["done_reason"] == "length" else "ok"
                            row["score"] = score_response(generation["raw_response"],case,doc)
                        except Exception as exc:
                            row.update(status="error",error=f"{type(exc).__name__}: {exc}",raw_response="",
                                       metrics={"latency_s":time.perf_counter()-started,"api_cost_eur":0,"energy_cost_eur":None})
                        record(row)
    except BaseException:
        frozen["status"] = "interrupted"
        raise
    else:
        frozen["status"] = "completed"
    finally:
        frozen.update(completed_at=datetime.now(timezone.utc).isoformat(), records=count, failed_requests=errors)
        write_json(run_dir / "manifest.json", frozen)
        print(f"Run saved: {run_dir}", flush=True)
    return run_dir
