#!/usr/bin/env python3
"""Round-trip regression: Cyr -> Lat -> Cyr on a sampled corpus.

Randomly samples Cyrillic sentences from every ``*.txt`` file under a folder,
runs each sentence through ``cyrillic_to_latin`` followed by
``latin_to_cyrillic``, and reports any sentence whose round-tripped Cyrillic
differs from the original.

Usage::

    .venv/bin/python3 tests/roundtrip_corpus.py \
        [--folder tests/text_files/] [--seed 123] [--count 5000] \
        [--report tests/regression_reports/roundtrip_report.txt] \
        [--ignore-known-limitations]

Same ``--folder``/``--seed``/``--count`` always produce the same sample.

``--ignore-known-limitations`` classifies each diff as either a
"known limitation" diff (the lossy Cyrillic collapses documented in
``LIMITATIONS.md`` plus palochka source normalization: Latin
``I``/``i``/``l``/``1``/``ı``/``İ`` rewritten to Cyrillic ``Ӏ``) or an
"other" diff. Known-limitation diffs remain counted in the report
header but are omitted from the per-diff listing, and the script exits
0 when only known-limitation diffs remain.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from random import Random
from typing import Literal

from adyghe_latin_utils.character_utils import AdigaCharacterUtils

try:
    from tests.sentence_extraction import extract_sentences, iter_text_files
except ModuleNotFoundError:
    from sentence_extraction import extract_sentences, iter_text_files

TESTS_DIR = Path(__file__).resolve().parent
DEFAULT_FOLDER = TESTS_DIR / "text_files"
DEFAULT_SEED = 123
DEFAULT_COUNT = 5000
DEFAULT_REPORT = TESTS_DIR / "regression_reports" / "roundtrip_report.txt"

DiffKind = Literal["known_limitation", "other"]

_PALOCHKA_STAND_INS: tuple[str, ...] = ("I", "i", "l", "1", "ı", "İ")
_PALOCHKA = "Ӏ"  # U+04C0

_KNOWN_LIMITATION_COLLAPSES: tuple[tuple[str, str], ...] = (
    ("Жъ", "Ж"), ("жъ", "ж"),
    ("Шъ", "Ш"), ("шъ", "ш"),
    ("Чъ", "Ч"), ("чъ", "ч"),
    ("ЧӀ", "КӀ"), ("чӀ", "кӀ"),
    ("Щ", "Ш"), ("щ", "ш"),
)

# The soft sign ``ь`` has no Latin grapheme, so Cyrillic → Latin drops it
# for every consonant it follows. The only exception is the digraph ``хь``
# (→ Latin ``h``), which does round-trip losslessly. This regex strips
# ``ь`` everywhere except after ``х``/``Х``.
_SOFT_SIGN_EXCEPT_X = re.compile(r"(?<![хХ])ь")


def collapse_known_limitations(text: str) -> str:
    """Apply palochka source normalization and the known lossy collapses.

    Two Cyrillic strings that become equal under this function differ only
    by effects that are documented in ``LIMITATIONS.md`` (or, for palochka,
    by the ``Ӏ`` stand-in normalization described there). Such diffs are
    not round-trip regressions.

    Palochka stand-ins (Latin ``I`` / ``i`` / ``l`` / ``1`` / ``ı`` / ``İ``)
    are rewritten to Cyrillic ``Ӏ`` first, so that trigraph collapses that
    contain palochka (e.g. ``чӀ → кӀ``) also match when the source text
    spells palochka with a Latin stand-in such as ``чI``.

    After the digraph collapses, any remaining soft sign ``ь`` is dropped
    unless it is preceded by ``х``/``Х`` (the ``хь`` digraph is the only
    place where ``ь`` is actually preserved by the converter). This covers
    the full family of ``<consonant>ь`` collapses such as ``жь → ж``,
    ``ть → т``, ``нь → н`` etc.
    """
    for stand_in in _PALOCHKA_STAND_INS:
        text = text.replace(stand_in, _PALOCHKA)
    for old, new in _KNOWN_LIMITATION_COLLAPSES:
        text = text.replace(old, new)
    text = _SOFT_SIGN_EXCEPT_X.sub("", text)
    return text


@dataclass(frozen=True)
class Sample:
    source_file: str
    sentence: str


@dataclass(frozen=True)
class RoundtripDiff:
    index: int
    source_file: str
    original: str
    latin: str
    roundtrip: str
    kind: DiffKind = "other"


def collect_pool(folder: Path) -> list[Sample]:
    """Extract every sentence candidate from every ``*.txt`` under ``folder``."""
    pool: list[Sample] = []
    for path in iter_text_files(folder):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for sentence in extract_sentences(text):
            pool.append(Sample(source_file=path.name, sentence=sentence))
    return pool


def sample_pool(pool: list[Sample], seed: int, count: int) -> list[Sample]:
    """Shuffle ``pool`` deterministically and return the first ``count`` items."""
    rng = Random(seed)
    shuffled = list(pool)
    rng.shuffle(shuffled)
    if count > len(shuffled):
        print(
            f"WARNING: only {len(shuffled)} sentences available, using all "
            f"{len(shuffled)} (requested {count})",
            file=sys.stderr,
        )
    return shuffled[: min(count, len(shuffled))]


def classify_diff(original: str, roundtrip: str) -> DiffKind:
    """Return ``"known_limitation"`` iff the diff is fully explained by
    the lossy Cyrillic collapses or palochka source normalization."""
    if collapse_known_limitations(original) == collapse_known_limitations(roundtrip):
        return "known_limitation"
    return "other"


def run_roundtrip(
    selected: list[Sample], utils: AdigaCharacterUtils
) -> list[RoundtripDiff]:
    """Convert each selected Cyrillic sentence through Lat and back."""
    diffs: list[RoundtripDiff] = []
    for idx, sample in enumerate(selected, start=1):
        latin = utils.cyrillic_to_latin(sample.sentence)
        roundtrip = utils.latin_to_cyrillic(latin)
        if roundtrip != sample.sentence:
            diffs.append(
                RoundtripDiff(
                    index=idx,
                    source_file=sample.source_file,
                    original=sample.sentence,
                    latin=latin,
                    roundtrip=roundtrip,
                    kind=classify_diff(sample.sentence, roundtrip),
                )
            )
    return diffs


def write_report(
    report_path: Path,
    *,
    folder: Path,
    seed: int,
    requested_count: int,
    sampled_count: int,
    diffs: list[RoundtripDiff],
    ignore_known_limitations: bool = False,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    separator = "-" * 80
    known_limitation_count = sum(1 for d in diffs if d.kind == "known_limitation")
    other_count = len(diffs) - known_limitation_count
    with report_path.open("w", encoding="utf-8") as handle:
        handle.write("Cyrillic -> Latin -> Cyrillic round-trip regression\n")
        handle.write(f"folder={folder}\n")
        handle.write(f"seed={seed}\n")
        handle.write(f"requested_count={requested_count}\n")
        handle.write(f"sampled_count={sampled_count}\n")
        handle.write(f"diff_count={len(diffs)}\n")
        handle.write(f"known_limitation_diff_count={known_limitation_count}\n")
        handle.write(f"other_diff_count={other_count}\n")
        handle.write(f"ignore_known_limitations={str(ignore_known_limitations).lower()}\n\n")

        if not diffs:
            handle.write("No differences found.\n")
            return

        listed = [
            d for d in diffs
            if not (ignore_known_limitations and d.kind == "known_limitation")
        ]
        if not listed:
            handle.write(
                "No differences to list "
                "(all diffs are known-limitation diffs and were suppressed).\n"
            )
            return

        for diff in listed:
            handle.write(f"Line {diff.index}  [{diff.source_file}] ({diff.kind})\n")
            handle.write(f"ORIGINAL: {diff.original}\n")
            handle.write(f"LATIN   : {diff.latin}\n")
            handle.write(f"ROUND   : {diff.roundtrip}\n")
            handle.write(separator + "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Round-trip Cyrillic -> Latin -> Cyrillic regression over a "
            "randomly sampled set of sentences from a corpus folder."
        )
    )
    parser.add_argument(
        "--folder",
        type=Path,
        default=DEFAULT_FOLDER,
        help=f"Folder of *.txt corpus files (default: {DEFAULT_FOLDER}).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"Random seed for deterministic sampling (default: {DEFAULT_SEED}).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help=(
            "Target number of sentences to sample. Capped to the number "
            f"available in the folder (default: {DEFAULT_COUNT})."
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help=f"Output report path (default: {DEFAULT_REPORT}).",
    )
    parser.add_argument(
        "--ignore-known-limitations",
        action="store_true",
        default=False,
        help=(
            "Classify each diff as either a known-limitation diff "
            "(the lossy Cyrillic collapses documented in LIMITATIONS.md "
            "plus palochka source normalization: Latin I/i/l/1/ı/İ "
            "rewritten to Cyrillic Ӏ) or an 'other' diff. Known-limitation "
            "diffs are still counted in the report header but are omitted "
            "from the per-diff listing. Exit code is 0 when only "
            "known-limitation diffs remain."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.folder.is_dir():
        print(f"ERROR: folder does not exist or is not a directory: {args.folder}",
              file=sys.stderr)
        return 2
    if args.count <= 0:
        print(f"ERROR: --count must be positive, got {args.count}", file=sys.stderr)
        return 2

    pool = collect_pool(args.folder)
    selected = sample_pool(pool, args.seed, args.count)

    utils = AdigaCharacterUtils()
    diffs = run_roundtrip(selected, utils)

    write_report(
        args.report,
        folder=args.folder,
        seed=args.seed,
        requested_count=args.count,
        sampled_count=len(selected),
        diffs=diffs,
        ignore_known_limitations=args.ignore_known_limitations,
    )

    known_limitation_diffs = [d for d in diffs if d.kind == "known_limitation"]
    other_diffs = [d for d in diffs if d.kind == "other"]
    print(
        f"[roundtrip] folder={args.folder} seed={args.seed} "
        f"requested={args.count} sampled={len(selected)} "
        f"diffs={len(diffs)} "
        f"known_limitation={len(known_limitation_diffs)} "
        f"other={len(other_diffs)} "
        f"ignore_known_limitations={str(args.ignore_known_limitations).lower()} "
        f"report={args.report}"
    )
    if args.ignore_known_limitations:
        return 0 if not other_diffs else 1
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())
