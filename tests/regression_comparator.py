from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DiffItem:
    line_number: int
    expected: str
    actual: str


@dataclass(frozen=True)
class ComparisonResult:
    report_path: Path
    expected_count: int
    actual_count: int
    diffs: list[DiffItem]

    @property
    def matches(self) -> bool:
        return not self.diffs and self.expected_count == self.actual_count

    def fail_message(self) -> str:
        return (
            f"{len(self.diffs)} differing lines "
            f"(expected={self.expected_count}, actual={self.actual_count}). "
            f"See full report: {self.report_path}"
        )


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def compare_lines_with_report(
    expected_lines: list[str],
    actual_lines: list[str],
    report_path: Path,
    *,
    title: str,
) -> ComparisonResult:
    max_count = max(len(expected_lines), len(actual_lines))
    diffs: list[DiffItem] = []
    for index in range(max_count):
        expected = expected_lines[index] if index < len(expected_lines) else "<missing>"
        actual = actual_lines[index] if index < len(actual_lines) else "<missing>"
        if expected != actual:
            diffs.append(DiffItem(line_number=index + 1, expected=expected, actual=actual))

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        handle.write(f"{title}\n")
        handle.write(f"expected_lines={len(expected_lines)}\n")
        handle.write(f"actual_lines={len(actual_lines)}\n")
        handle.write(f"diff_count={len(diffs)}\n\n")

        if not diffs:
            handle.write("No differences found.\n")
        else:
            for diff in diffs:
                handle.write(f"Line {diff.line_number}\n")
                handle.write(f"EXPECTED: {diff.expected}\n")
                handle.write(f"ACTUAL  : {diff.actual}\n")
                handle.write("-" * 80 + "\n")

    return ComparisonResult(
        report_path=report_path,
        expected_count=len(expected_lines),
        actual_count=len(actual_lines),
        diffs=diffs,
    )
