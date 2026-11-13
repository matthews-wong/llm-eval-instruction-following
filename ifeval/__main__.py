import argparse
import sys
from pathlib import Path

from ifeval.dataset import load_cases
from ifeval.report import render
from ifeval.scoring import score_case, summarize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ifeval", description="Score instruction-following on recorded responses.")
    parser.add_argument("cases", type=Path, help="JSONL file of cases")
    parser.add_argument("--min-prompt-accuracy", type=float, default=0.0, help="exit 1 if prompt accuracy is lower")
    args = parser.parse_args(argv)

    try:
        cases = load_cases(args.cases)
        results = [score_case(c) for c in cases]
        summary = summarize(results)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(render(results, summary))
    if summary.prompt_accuracy < args.min_prompt_accuracy:
        print(f"prompt accuracy {summary.prompt_accuracy:.3f} is below {args.min_prompt_accuracy}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
