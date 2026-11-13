"""Strict scoring: a case passes only when every constraint passes."""
from dataclasses import dataclass

from ifeval.constraints import check
from ifeval.dataset import Case


@dataclass(frozen=True)
class CaseResult:
    id: str
    outcomes: tuple[tuple[str, bool], ...]

    @property
    def passed(self) -> bool:
        return all(ok for _, ok in self.outcomes)


@dataclass(frozen=True)
class Summary:
    cases: int
    instructions: int
    prompt_accuracy: float
    instruction_accuracy: float
    by_kind: dict[str, tuple[int, int]]


def score_case(case: Case) -> CaseResult:
    outcomes = tuple((c.kind, check(case.response, c.kind, c.arg)) for c in case.constraints)
    return CaseResult(case.id, outcomes)


def summarize(results: list[CaseResult]) -> Summary:
    if not results:
        raise ValueError("cannot summarize zero results")
    by_kind: dict[str, tuple[int, int]] = {}
    for result in results:
        for kind, ok in result.outcomes:
            passed, total = by_kind.get(kind, (0, 0))
            by_kind[kind] = (passed + ok, total + 1)
    instructions = sum(total for _, total in by_kind.values())
    satisfied = sum(passed for passed, _ in by_kind.values())
    return Summary(
        cases=len(results),
        instructions=instructions,
        prompt_accuracy=sum(r.passed for r in results) / len(results),
        instruction_accuracy=satisfied / instructions,
        by_kind=dict(sorted(by_kind.items())),
    )
