"""Constraint checkers: each takes the response text and the rule's argument."""
import json
import re
from typing import Any, Callable

BULLET_RE = re.compile(r"^\s*[-*]\s+\S", re.MULTILINE)
SENTENCE_END_RE = re.compile(r"[.!?]+(?:\s|$)")


def _words(text: str) -> list[str]:
    return text.split()


def max_words(text: str, limit: int) -> bool:
    return len(_words(text)) <= limit


def min_words(text: str, limit: int) -> bool:
    return len(_words(text)) >= limit


def max_sentences(text: str, limit: int) -> bool:
    return len(SENTENCE_END_RE.findall(text.strip())) <= limit


def include(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def exclude(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return not any(term.lower() in lowered for term in terms)


def bullets(text: str, count: int) -> bool:
    return len(BULLET_RE.findall(text)) == count


def lowercase(text: str, enabled: bool) -> bool:
    return text == text.lower() if enabled else True


def no_commas(text: str, enabled: bool) -> bool:
    return "," not in text if enabled else True


def ends_with(text: str, suffix: str) -> bool:
    return text.rstrip().endswith(suffix)


def json_object(text: str, enabled: bool) -> bool:
    if not enabled:
        return True
    try:
        return isinstance(json.loads(text), dict)
    except json.JSONDecodeError:
        return False


CHECKERS: dict[str, Callable[[str, Any], bool]] = {
    "max_words": max_words,
    "min_words": min_words,
    "max_sentences": max_sentences,
    "include": include,
    "exclude": exclude,
    "bullets": bullets,
    "lowercase": lowercase,
    "no_commas": no_commas,
    "ends_with": ends_with,
    "json_object": json_object,
}


def check(text: str, kind: str, arg: Any) -> bool:
    checker = CHECKERS.get(kind)
    if checker is None:
        raise ValueError(f"unknown constraint kind {kind!r}; expected one of {sorted(CHECKERS)}")
    return checker(text, arg)
