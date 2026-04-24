"""
Tests for the CLI interface of adiga_character_utils.py.
"""
import subprocess
import sys

import pytest


def run_cli(*args):
    """Helper: run the script as a module and return the result."""
    return subprocess.run(
        [sys.executable, '-m', 'adyghe_latin_utils.character_utils', *args],
        capture_output=True,
        text=True,
    )


# ============================================================
# Cyrillic to Latin (c2l)
# ============================================================

class TestCyrillicToLatin:

    def test_c2l_to_output_file(self, tmp_path):
        infile = tmp_path / 'input.txt'
        outfile = tmp_path / 'output.txt'
        infile.write_text('адыгэ\n', encoding='utf-8')

        result = run_cli('-i', str(infile), '-o', str(outfile), '-d', 'c2l')

        assert result.returncode == 0
        output = outfile.read_text(encoding='utf-8')
        assert output == 'adıǵe\n'

    def test_c2l_to_stdout(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('адыгэ\n', encoding='utf-8')

        result = run_cli('-i', str(infile), '-d', 'c2l')

        assert result.returncode == 0
        assert result.stdout == 'adıǵe\n'

    def test_c2l_multiline(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('адыгэ\nсэлам\n', encoding='utf-8')

        result = run_cli('-i', str(infile), '-d', 'c2l')

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert len(lines) == 2

    def test_c2l_text_to_stdout(self):
        result = run_cli('-t', 'адыгэ', '-d', 'c2l')

        assert result.returncode == 0
        assert result.stdout == 'adıǵe\n'

    def test_c2l_text_bug_i_palochka_ua(self):
        result = run_cli('-t', 'иӀуагъ', '-d', 'c2l')

        assert result.returncode == 0
        assert result.stdout == 'yioáğ\n'


# ============================================================
# Latin to Cyrillic (l2c)
# ============================================================

class TestLatinToCyrillic:

    def test_l2c_to_output_file(self, tmp_path):
        infile = tmp_path / 'input.txt'
        outfile = tmp_path / 'output.txt'
        infile.write_text('selam\n', encoding='utf-8')

        result = run_cli('-i', str(infile), '-o', str(outfile), '-d', 'l2c')

        assert result.returncode == 0
        output = outfile.read_text(encoding='utf-8')
        assert 'с' in output  # Cyrillic 'с'

    def test_l2c_to_stdout(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('selam\n', encoding='utf-8')

        result = run_cli('-i', str(infile), '-d', 'l2c')

        assert result.returncode == 0
        assert len(result.stdout) > 0

    def test_l2c_multiline(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('selam\nadıǵe\n', encoding='utf-8')

        result = run_cli('-i', str(infile), '-d', 'l2c')

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert len(lines) == 2

    def test_l2c_text_to_stdout(self):
        result = run_cli('-t', 'selam', '-d', 'l2c')

        assert result.returncode == 0
        assert len(result.stdout) > 0
        assert result.stdout.endswith('\n')

    def test_l2c_text_bug_yioa(self):
        result = run_cli('-t', 'yioáğ', '-d', 'l2c')

        assert result.returncode == 0
        assert result.stdout == 'иӀуагъ\n'

    def test_l2c_text_bug_kewioa(self):
        result = run_cli('-t', 'kıwioáğ', '-d', 'l2c')

        assert result.returncode == 0
        assert result.stdout == 'къыуиӀуагъ\n'

    def test_text_to_output_file(self, tmp_path):
        outfile = tmp_path / 'output.txt'

        result = run_cli('-t', 'адыгэ', '-o', str(outfile), '-d', 'c2l')

        assert result.returncode == 0
        output = outfile.read_text(encoding='utf-8')
        assert output == 'adıǵe'


# ============================================================
# Error handling
# ============================================================

class TestErrorHandling:

    def test_missing_input_arg(self):
        result = run_cli('-d', 'c2l')

        assert result.returncode != 0
        assert 'required' in result.stderr.lower() or 'error' in result.stderr.lower()

    def test_missing_direction_arg(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('test\n', encoding='utf-8')

        result = run_cli('-i', str(infile))

        assert result.returncode != 0
        assert 'required' in result.stderr.lower() or 'error' in result.stderr.lower()

    def test_invalid_direction(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('test\n', encoding='utf-8')

        result = run_cli('-i', str(infile), '-d', 'invalid')

        assert result.returncode != 0
        assert 'invalid choice' in result.stderr.lower() or 'error' in result.stderr.lower()

    def test_nonexistent_input_file(self):
        result = run_cli('-i', '/tmp/nonexistent_file_xyz.txt', '-d', 'c2l')

        assert result.returncode != 0

    def test_input_and_text_are_mutually_exclusive(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('test\n', encoding='utf-8')

        result = run_cli('-i', str(infile), '-t', 'test', '-d', 'c2l')

        assert result.returncode != 0
        assert 'not allowed with argument' in result.stderr.lower() \
            or 'mutually exclusive' in result.stderr.lower()

    def test_help_flag(self):
        result = run_cli('-h')

        assert result.returncode == 0
        assert 'input' in result.stdout.lower()
        assert 'text' in result.stdout.lower()
        assert 'output' in result.stdout.lower()
        assert 'direction' in result.stdout.lower()
        assert 'c2l' in result.stdout
        assert 'l2c' in result.stdout
