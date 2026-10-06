"""Static, read-only report. Never exposes an endpoint that can execute models."""
import html
import json
import shutil
import statistics
from pathlib import Path
from .core import read_json, write_json


def aggregate(rows):
    groups = {}
    for row in rows:
        groups.setdefault((row["model"],row["task"]),[]).append(row)
    result = []
    for (model, task), values in sorted(groups.items()):
        # Failures and malformed responses count as zero for structured-task accuracy.
        accuracies = [(r.get("score",{}).get("field_accuracy") or 0) if r["status"] == "ok" else 0 for r in values]
        durations = [r["metrics"]["latency_s"] for r in values if "latency_s" in r.get("metrics",{})]
        per_case = {}
        for row, accuracy in zip(values,accuracies):
            per_case.setdefault(row["case_id"],[]).append(accuracy)
        spreads = [max(v)-min(v) for v in per_case.values() if len(v)>1]
        result.append({"model":model,"task":task,"n":len(values),"distinct_cases":len(per_case),
          "error_rate":sum(r["status"]!="ok" for r in values)/len(values),
          "format_rate":sum(r["status"]=="ok" and r.get("score",{}).get("schema_valid",False) for r in values)/len(values),
          "field_accuracy":statistics.mean(accuracies) if task!="synthesis" else None,
          "critical_errors":sum(len(r.get("score",{}).get("critical_errors",[])) for r in values),
          "latency_median_s":statistics.median(durations) if durations else None,
          "mean_repeat_range":statistics.mean(spreads) if spreads and task!="synthesis" else None})
    return result


def export(root, run_dirs, dest, include_documents=False):
    root, dest = Path(root), Path(dest)
    dest.mkdir(parents=True,exist_ok=True)
    datasets = []
    for run_dir in run_dirs:
        run_dir = Path(run_dir)
        manifest = read_json(run_dir / "manifest.json")
        rows = [json.loads(line) for line in (run_dir/"results.jsonl").read_text().splitlines() if line.strip()]
        sources = manifest["manifest"]["sources"]
        datasets.append({"run_id":manifest["run_id"],"split":manifest["split"],"created_at":manifest["created_at"],
             "status":manifest["status"],"protocol_version":manifest["protocol_version"],"models":manifest["models"],
             "corpus_hash":manifest["corpus_hash"],"cases_hash":manifest["cases_hash"],
             "reference_review":manifest["reference_review"],"sources":sources,
             "cases":manifest["cases"],"results":[{k:v for k,v in row.items() if k!="prompt"} for row in rows],
             "aggregates":aggregate(rows),"environment":manifest["environment"]})
        if include_documents:
            # Explicit local convenience only. Public deployment should use source links.
            for s in sources:
                target = dest / "sources" / (s["id"]+".pdf")
                target.parent.mkdir(exist_ok=True)
                shutil.copy2(root/"data/raw"/(s["id"]+".pdf"),target)
    write_json(dest/"results.json",datasets)
    # JSON-in-script escaped against closing script tags and HTML parsing.
    payload = json.dumps(datasets,ensure_ascii=False).replace("<","\\u003c").replace("\u2028","\\u2028").replace("\u2029","\\u2029")
    template = (root/"web/index.html").read_text()
    (dest/"index.html").write_text(template.replace("__BENCHMARK_DATA__",payload),encoding="utf-8")
    for name in ["app.js","style.css"]:
        shutil.copy2(root/"web"/name,dest/name)
    print(f"Static report: {dest / 'index.html'}")
    return dest
