# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-24

First stable release. The public API — the `AdigaCharacterUtils` and
`AdigaNumberUtils` classes re-exported from `adyghe_latin_utils`, and the
`adyghe-char-convert` and `adyghe-num-convert` command-line tools — is now
covered by [Semantic Versioning](https://semver.org/spec/v2.0.0.html):
backward-incompatible changes will require a major version bump.

### Added

- New `AdigaCharacterUtils.sanitize_latin_text()` method that strips
  characters outside the recognized Latin Adyghe alphabet, collapses
  whitespace, replaces tabs with spaces, drops stray double quotes, and
  normalizes `:` / `;` to `.`.
- `adyghe-char-convert` CLI: new `-t` / `--text` flag for converting a
  string passed directly on the command line. `-t` and `-i` / `--input`
  are mutually exclusive; when `-t` is used the output is written with a
  trailing newline if one is not already present.
- New `LIMITATIONS.md` documenting the Cyrillic characters and digraphs
  (`щ`, `жь`, `жъ`, `шъ`, `чъ`) that cannot be represented losslessly in
  the Latin Adyghe alphabet.
- Regression-testing infrastructure under `tests/`:
  - `roundtrip_corpus.py` — samples sentences from a Cyrillic corpus and
    runs Cyr → Lat → Cyr round-trip comparisons, producing a diff report.
  - `sentence_extraction.py` — corpus sentence extraction helpers.
  - `regression_comparator.py` / `regression_compare.py` — line-level
    comparison utilities used by the corpus regression tests.
  - `generate_regression_texts_cyr.py` — helper script to (re)generate
    the Cyrillic regression input.
  - Golden fixtures: `regression_texts_cyr.txt`,
    `regression_texts_cyr_golden.txt`, `regression_texts_lat.txt`,
    `regression_texts_lat_golden.txt`.
  - Cyrillic corpus files under `tests/text_files/` for round-trip
    sampling.
- New tests:
  - `tests/test_sanitize_latin_text.py` covering the new sanitizer.
  - `tests/test_generate_regression_texts_cyr.py` covering the
    regression corpus generator.
  - `TestCorpusRegression` classes in `tests/test_cyrillic_to_latin.py`
    and `tests/test_latin_to_cyrillic.py` that diff each converter
    against the golden corpora.
  - `TestDigraphCapitalization` in `tests/test_latin_to_cyrillic.py`
    covering word-initial digraph title-casing and all-caps preservation.
  - Additional bug-regression tests for `иӀ`, `яӀ`, `иӀуа` / `yioá`, and
    related palochka sequences.
  - New CLI tests for the `-t` / `--text` flag and its mutual exclusion
    with `-i`.

### Changed

- Cyrillic → Latin / Latin → Cyrillic: word-initial prefix handling now
  supports 4-character prefixes in addition to 1–3, enabling the new
  `иӀуа` ↔ `yioá` mapping (e.g. `иӀуагъ` ↔ `yioáğ`).
- Word-start prefix rules now apply after stripping any run of leading
  non-alphabetic characters (quotes, parentheses, brackets, curly
  quotes, etc.), not just a leading `(` or `-`. Hyphenated compounds
  continue to be split and each part handled independently.
- Cyrillic → Latin digit handling: a bare `1` is only treated as a
  palochka substitute when the preceding character is Cyrillic; in
  every other context it is preserved as the digit `1`.
- Cyrillic → Latin now preserves Roman-numeral-only tokens (`I`, `II`,
  `III`, `IV`, `V`, …, composed of `I V X L C D M`) as-is instead of
  interpreting their `I`s as palochka substitutes.
- Added Cyrillic `Ӏ` (U+04C0) to the Cyrillic → Latin single-character
  map as `'`, removing a gap where the canonical palochka was not
  handled by the basic char map.
- Added `эӀе` → `eé` context rule (and `эiе` / `эIе` variants) for
  correct handling of sequences such as `тхьэIешIа`.

### Fixed

- **Digraph capitalization on round-trip (class 4).** Latin → Cyrillic
  now mirrors the Cyrillic → Latin title-casing logic: a word-initial
  capital that maps to a multi-letter Cyrillic digraph is title-cased
  (e.g. `Cıri` → `Джыри`, `Kaxem` → `Къахэм`, `Ğogur` → `Гъогур`,
  `Ham` → `Хьам`, `Ḣan` → `Хъан`, `Ĺıtén` → `Лъытен`, `Źuz` → `Дзуз`,
  `Şüase` → `Шъуасэ`). If the following Latin character is also
  uppercase (all-caps run), the full digraph is uppercased
  (e.g. `KAXEM` → `КЪАХЭМ`). Previously both letters of the digraph
  were always uppercased, producing outputs such as `ДЖыри` or `ХЪан`.
- **Word-final `й` becoming `и` (class 5).** Latin → Cyrillic now maps
  `y` after a Latin vowel (`a`, `o`, `u`, `e`, `i`, `ı`) to `й` rather
  than `и`, so e.g. `şıdey` now correctly round-trips to `шыдэй`
  instead of `шыдэи`. The generic `y` → `и` fallback after a consonant
  is unchanged.
- **Word-end `иӀ` / `яӀ` sequences.** Cyrillic → Latin no longer emits
  an extra `ı` before the apostrophe: `иӀ` → `yi'` (was `yiı'`) and
  `яӀ` → `ya'`.
- **`иӀуа` ↔ `yioá`.** Cyrillic → Latin and Latin → Cyrillic now both
  recognize the `иӀуа` ↔ `yioá` sequence at any position in the word,
  fixing round-trip of tokens like `иӀуагъ` and `къыуиӀуагъ`.
- `Ḣan` now converts to `Хъан` (title case) instead of `ХЪан`, matching
  the rest of the digraph-capitalization fix.
