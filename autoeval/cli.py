import argparse
import json
from pathlib import Path
from .core import validate_corpus
from .runner import run
from .report import export


def main():
    parser = argparse.ArgumentParser(description="AutoEval — local automotive LLM benchmark")
    parser.add_argument("--root",type=Path,default=Path.cwd())
    sub = parser.add_subparsers(dest="command",required=True)
    sub.add_parser("validate",help="Verify source hashes, reference quotes and split isolation")
    r = sub.add_parser("run")
    r.add_argument("--model",action="append",default=[])
    r.add_argument("--split",choices=["dev","pilot"],default="dev")
    r.add_argument("--repeats",type=int,default=1)
    r.add_argument("--base-url",default="http://127.0.0.1:11434")
    r.add_argument("--timeout",type=int,default=180)
    r.add_argument("--baseline",action="store_true")
    e = sub.add_parser("export")
    e.add_argument("--run",type=Path,action="append",required=True)
    e.add_argument("--dest",type=Path,default=Path("site"))
    e.add_argument("--include-documents",action="store_true")
    args = parser.parse_args()
    try:
        if args.command=="validate":
            print(json.dumps(validate_corpus(args.root),ensure_ascii=False,indent=2))
        elif args.command=="run":
            run(args.root,args.model,args.split,args.repeats,args.base_url,args.baseline,args.timeout)
        else:
            export(args.root,args.run,args.dest,args.include_documents)
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(1,f"Error: {exc}\n")


if __name__=="__main__":
    main()
