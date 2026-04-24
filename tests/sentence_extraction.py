"""Shared helpers for extracting Cyrillic sentences from corpus text files.

Used by both the regression fixture generator
(``tests/generate_regression_texts_cyr.py``) and the round-trip regression
script (``tests/roundtrip_corpus.py``) so the two tools agree on what
constitutes an eligible sentence.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

PAGE_MARKER_RE = re.compile(r"^\s*---\s*Page\s+\d+\s*---\s*$", re.IGNORECASE)
SENTENCE_END_RE = re.compile(r"(?<=[.!?…])\s+")
CYRILLIC_CHAR_RE = re.compile(r"[А-Яа-яЁёӀӏ]")


def iter_text_files(directory: Path) -> Iterable[Path]:
    """Yield ``*.txt`` files in ``directory`` sorted by name."""
    return sorted(p for p in directory.glob("*.txt") if p.is_file())


def normalize_text(text: str) -> str:
    """Collapse whitespace and drop blank lines / page markers."""
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or PAGE_MARKER_RE.match(line):
            continue
        lines.append(re.sub(r"\s+", " ", line))
    return "\n".join(lines)


def is_sentence_candidate(piece: str) -> bool:
    """Return ``True`` if ``piece`` looks like a sentence worth sampling."""
    candidate = piece.strip()
    if not candidate:
        return False
    if len(candidate) < 12:
        return False
    if not CYRILLIC_CHAR_RE.search(candidate):
        return False
    # Dictionary-like entries are often comma-separated fragments with no
    # terminal punctuation; keep them out unless they are sentence-like.
    ends_with_terminal = candidate[-1] in ".!?…"
    has_verb_like_flow = " " in candidate and len(candidate.split()) >= 3
    return ends_with_terminal or has_verb_like_flow


def extract_sentences(text: str) -> list[str]:
    """Extract sentence-like fragments from raw corpus ``text``."""
    normalized = normalize_text(text)
    if not normalized:
        return []

    pieces: list[str] = []
    for line in normalized.split("\n"):
        if line[-1] in ".!?…":
            pieces.extend(SENTENCE_END_RE.split(line))
        else:
            # Keep short dialog/corpus lines in 50languages-like files.
            pieces.append(line)

    return [piece.strip() for piece in pieces if is_sentence_candidate(piece)]
