"""Load cases from JSONL: {"id", "prompt", "response", "constraints": [{"kind", "arg"}]}."""
import json
from dataclasses import dataclass
from pathlib import Path

from ifeval.constraints import CHECKERS

REQUIRED_FIELDS = ("id", "prompt", "response", "constraints")


@dataclass(frozen=True)
class Constraint:
    kind: str
    arg: object


@dataclass(frozen=True)
class Case:
    id: str
    prompt: str
    response: str
    constraints: tuple[Constraint, ...]


def parse_case(line: str, lineno: int) -> Case:
    try:
        raw = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ValueError(f"line {lineno}: invalid JSON ({exc.msg})") from exc
    missing = [f for f in REQUIRED_FIELDS if f not in raw]
    if missing:
        raise ValueError(f"line {lineno}: missing fields {missing}")
    constraints = []
    for item in raw["constraints"]:
        if item.get("kind") not in CHECKERS:
            raise ValueError(f"line {lineno} ({raw['id']}): unknown constraint kind {item.get('kind')!r}")
        constraints.append(Constraint(item["kind"], item.get("arg")))
    if not constraints:
        raise ValueError(f"line {lineno} ({raw['id']}): case has no constraints")
    return Case(raw["id"], raw["prompt"], raw["response"], tuple(constraints))


def load_cases(path: Path) -> list[Case]:
    cases = [
        parse_case(line, n)
        for n, line in enumerate(Path(path).read_text().splitlines(), start=1)
        if line.strip()
    ]
    ids = [c.id for c in cases]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        raise ValueError(f"duplicate case ids: {duplicates}")
    return cases
