"""Plain-text report for a scored run."""
from ifeval.scoring import CaseResult, Summary


def render(results: list[CaseResult], summary: Summary) -> str:
    lines = [f"{'case':<24}{'result':<8}failed constraints"]
    for r in results:
        failed = ", ".join(kind for kind, ok in r.outcomes if not ok) or "-"
        lines.append(f"{r.id:<24}{'pass' if r.passed else 'FAIL':<8}{failed}")
    lines.append("")
    lines.append(f"{'constraint':<16}{'passed':>7}{'total':>7}")
    for kind, (passed, total) in summary.by_kind.items():
        lines.append(f"{kind:<16}{passed:>7}{total:>7}")
    lines.append("")
    lines.append(f"prompt accuracy:      {summary.prompt_accuracy:.1%} ({summary.cases} cases)")
    lines.append(f"instruction accuracy: {summary.instruction_accuracy:.1%} ({summary.instructions} constraints)")
    return "\n".join(lines)
