"""Verify and render the shipped results, without PDFs, Ollama or network calls."""
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from autoeval.core import read_json, write_json
from autoeval.report import aggregate


def verify(datasets):
    if not isinstance(datasets, list) or not datasets:
        raise ValueError("Expected a nonempty list of exported runs")
    seen_runs = set()
    for run in datasets:
        if run["run_id"] in seen_runs:
            raise ValueError("Duplicate run ID")
        seen_runs.add(run["run_id"])
        case_ids = {c["id"] for c in run["cases"]}
        keys = set()
        for row in run["results"]:
            key = (row["model"], row["case_id"], row["repeat"])
            if key in keys or row["case_id"] not in case_ids or row["run_id"] != run["run_id"]:
                raise ValueError("Duplicate or inconsistent observation")
            keys.add(key)
        if aggregate(run["results"]) != run["aggregates"]:
            raise ValueError("Saved aggregates differ from recomputed aggregates")
    return {"runs": len(datasets), "observations": sum(len(d["results"]) for d in datasets)}


def render(datasets, destination, root=ROOT):
    verify(datasets)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    # All text is data. Escape the HTML script terminator before embedding JSON.
    payload = json.dumps(datasets, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = (Path(root) / "web/index.html").read_text(encoding="utf-8")
    (destination / "index.html").write_text(template.replace("__BENCHMARK_DATA__", payload), encoding="utf-8")
    write_json(destination / "results.json", datasets)
    for asset in ["app.js", "style.css"]:
        shutil.copy2(Path(root) / "web" / asset, destination / asset)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "results/pilot-v0.1.json")
    parser.add_argument("--output", type=Path, default=ROOT / "site")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    try:
        datasets = read_json(args.input)
        print(json.dumps(verify(datasets)))
        if not args.verify_only:
            print(f"Static report: {render(datasets, args.output) / 'index.html'}")
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
