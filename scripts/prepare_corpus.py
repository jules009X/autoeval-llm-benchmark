"""Fetch pinned public reports and extract their text. PDFs remain outside Git."""
import argparse
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from autoeval.core import digest, read_json, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        import pypdf
    except ImportError:
        raise SystemExit('Install corpus dependency: python3 -m pip install "pypdf==6.10.0"')
    manifest = read_json(args.root / "data/manifest.json")
    for source in manifest["sources"]:
        dest = args.root / "data/raw" / (source["id"] + ".pdf")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            tmp = dest.with_suffix(".download")
            try:
                subprocess.run(["curl", "--fail", "--location", "--silent", "--show-error", "--max-time", "90",
                                "--proto", "=https", source["url"], "-o", str(tmp)], check=True)
                if hashlib.sha256(tmp.read_bytes()).hexdigest() != source["sha256"]:
                    raise ValueError(f"Source changed: {source['id']}; do not overwrite the reference version")
                tmp.replace(dest)
            finally:
                tmp.unlink(missing_ok=True)
        if hashlib.sha256(dest.read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError(f"PDF hash mismatch: {source['id']}")
        pages = [{"page": i + 1, "text": p.extract_text()} for i, p in enumerate(pypdf.PdfReader(dest).pages)]
        if digest(pages) != source["text_sha256"]:
            raise ValueError(f"Extraction differs for {source['id']}; expected pypdf {manifest['extractor_version']}")
        write_json(args.root / "data/processed" / (source["id"] + ".json"), pages)
        print(source["id"], len(pages), "pages; verified")
    write_json(args.root / "data/processed/retrieval.json", {
        "retrieved_at": datetime.now(timezone.utc).isoformat(), "pypdf_version": pypdf.__version__})


if __name__ == "__main__":
    main()
