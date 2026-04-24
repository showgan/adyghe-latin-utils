from collections import Counter
from pathlib import Path

from tests.generate_regression_texts_cyr import (
    MAX_SENTENCES_PER_FILE,
    OUTPUT_TXT,
    collect_sentence_rows,
    generate_txt,
)
from tests.sentence_extraction import iter_text_files


def _read_txt_rows(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines, "TXT fixture is empty"
    return lines


def test_regression_txt_exists_and_has_sentence_rows():
    assert OUTPUT_TXT.exists(), f"Expected generated file at {OUTPUT_TXT}"
    rows = _read_txt_rows(OUTPUT_TXT)
    assert rows
    assert all("|" not in row for row in rows)


def test_regression_txt_per_source_cap_respected():
    rows = collect_sentence_rows()
    counts = Counter(row.source_file for row in rows)
    for source, count in counts.items():
        assert count <= MAX_SENTENCES_PER_FILE, (
            f"{source} has {count} rows, max is {MAX_SENTENCES_PER_FILE}"
        )


def test_generate_txt_is_deterministic_for_fixed_seed(tmp_path):
    output_a = tmp_path / "a.txt"
    output_b = tmp_path / "b.txt"

    import tests.generate_regression_texts_cyr as generator

    original_output = generator.OUTPUT_TXT
    try:
        generator.OUTPUT_TXT = output_a
        generate_txt()
        content_a = output_a.read_text(encoding="utf-8")

        generator.OUTPUT_TXT = output_b
        generate_txt()
        content_b = output_b.read_text(encoding="utf-8")
    finally:
        generator.OUTPUT_TXT = original_output

    assert content_a == content_b


def test_generator_scans_text_files_directory():
    import tests.generate_regression_texts_cyr as generator

    files = list(iter_text_files(generator.TEXT_FILES_DIR))
    assert files
    assert all(path.suffix == ".txt" for path in files)
