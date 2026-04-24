#!/usr/bin/env python3
"""Generate deterministic regression text fixture from Cyrillic corpora."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

try:
    from tests.sentence_extraction import extract_sentences, iter_text_files
except ModuleNotFoundError:
    from sentence_extraction import extract_sentences, iter_text_files

TEXT_FILES_DIR = Path(__file__).resolve().parent / "text_files"
OUTPUT_TXT = Path(__file__).resolve().parent / "regression_texts_cyr.txt"
SEED = 20260423
MAX_SENTENCES_PER_FILE = 100


@dataclass(frozen=True)
class SentenceRow:
    source_file: str
    sentence: str


def _sample_sentences(sentences: list[str], rng: random.Random) -> list[str]:
    if len(sentences) <= MAX_SENTENCES_PER_FILE:
        return sentences
    sampled = rng.sample(sentences, MAX_SENTENCES_PER_FILE)
    sampled.sort()
    return sampled


def collect_sentence_rows() -> list[SentenceRow]:
    rng = random.Random(SEED)
    rows: list[SentenceRow] = []
    for path in iter_text_files(TEXT_FILES_DIR):
        text = path.read_text(encoding="utf-8", errors="ignore")
        extracted = extract_sentences(text)
        selected = _sample_sentences(extracted, rng)
        rows.extend(SentenceRow(source_file=path.name, sentence=s) for s in selected)
    return rows


def generate_txt() -> tuple[int, int]:
    rows = collect_sentence_rows()
    source_files = list(iter_text_files(TEXT_FILES_DIR))
    OUTPUT_TXT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_TXT.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(f"{row.sentence}\n")

    return len(source_files), len(rows)


if __name__ == "__main__":
    files_count, rows_count = generate_txt()
    print(
        f"Generated {OUTPUT_TXT} from {files_count} files with {rows_count} rows "
        f"(seed={SEED}, cap={MAX_SENTENCES_PER_FILE}/file)."
    )
