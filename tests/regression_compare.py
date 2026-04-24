#!/usr/bin/env python3
"""CLI wrapper for corpus regression comparison reports."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from adyghe_latin_utils.character_utils import AdigaCharacterUtils

try:
    from tests.regression_comparator import compare_lines_with_report, read_lines
except ModuleNotFoundError:
    from regression_comparator import compare_lines_with_report, read_lines


@dataclass(frozen=True)
class RegressionJob:
    name: str
    input_path: Path
    expected_path: Path
    report_path: Path
    title: str


def _run_job(job: RegressionJob, utils: AdigaCharacterUtils) -> int:
    input_lines = read_lines(job.input_path)
    expected_lines = read_lines(job.expected_path)

    if job.name == "cyrillic_to_latin":
        actual_lines = [utils.cyrillic_to_latin(line) for line in input_lines]
    else:
        actual_lines = [utils.latin_to_cyrillic(line) for line in input_lines]

    result = compare_lines_with_report(
        expected_lines=expected_lines,
        actual_lines=actual_lines,
        report_path=job.report_path,
        title=job.title,
    )
    print(f"[{job.name}] {result.fail_message()}")
    return 0 if result.matches else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate human-readable corpus regression diff reports."
    )
    parser.add_argument(
        "--c2l",
        action="store_true",
        help="Run Cyrillic -> Latin regression comparison.",
    )
    parser.add_argument(
        "--l2c",
        action="store_true",
        help="Run Latin -> Cyrillic regression comparison.",
    )
    args = parser.parse_args()

    tests_dir = Path(__file__).resolve().parent
    jobs: list[RegressionJob] = []
    if args.c2l:
        jobs.append(
            RegressionJob(
                name="cyrillic_to_latin",
                input_path=tests_dir / "regression_texts_cyr.txt",
                expected_path=tests_dir / "regression_texts_lat_golden.txt",
                report_path=tests_dir / "regression_reports" / "cyrillic_to_latin_report.txt",
                title="Cyrillic to Latin regression comparison",
            )
        )
    if args.l2c:
        jobs.append(
            RegressionJob(
                name="latin_to_cyrillic",
                input_path=tests_dir / "regression_texts_lat.txt",
                expected_path=tests_dir / "regression_texts_cyr_golden.txt",
                report_path=tests_dir / "regression_reports" / "latin_to_cyrillic_report.txt",
                title="Latin to Cyrillic regression comparison",
            )
        )

    if not jobs:
        jobs = [
            RegressionJob(
                name="cyrillic_to_latin",
                input_path=tests_dir / "regression_texts_cyr.txt",
                expected_path=tests_dir / "regression_texts_lat_golden.txt",
                report_path=tests_dir / "regression_reports" / "cyrillic_to_latin_report.txt",
                title="Cyrillic to Latin regression comparison",
            ),
            RegressionJob(
                name="latin_to_cyrillic",
                input_path=tests_dir / "regression_texts_lat.txt",
                expected_path=tests_dir / "regression_texts_cyr_golden.txt",
                report_path=tests_dir / "regression_reports" / "latin_to_cyrillic_report.txt",
                title="Latin to Cyrillic regression comparison",
            ),
        ]

    utils = AdigaCharacterUtils()
    exit_code = 0
    for job in jobs:
        exit_code |= _run_job(job, utils)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
