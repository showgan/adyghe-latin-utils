import os
import subprocess
import sys

import pytest

from adyghe_latin_utils.number_utils import AdigaNumberUtils


@pytest.fixture(scope="module")
def utils():
    return AdigaNumberUtils()


# ============================================================
# SINGLE DIGITS (0-9)
# ============================================================
class TestSingleDigits:
    @pytest.mark.parametrize("number, expected", [
        (0, "ziy"),
        (1, "zı"),
        (2, "ṫu"),
        (3, "şı"),
        (4, "pĺ'ı"),
        (5, "tfı"),
        (6, "xı"),
        (7, "blı"),
        (8, "yi"),
        (9, "bğu"),
    ])
    def test_single_digit(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected


# ============================================================
# TENS (10-99)
# ============================================================
class TestTens:
    @pytest.mark.parametrize("number, expected", [
        (10, "zıć"),
        (20, "ṫuć"),
        (30, "şıć"),
        (40, "pĺ'ıć"),
        (50, "tfıć"),
        (60, "xıć"),
        (70, "blıć"),
        (80, "yić"),
        (90, "bğuć"),
    ])
    def test_round_tens(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected

    @pytest.mark.parametrize("number, expected", [
        (11, "zıć zı"),
        (12, "zıć ṫu"),
        (25, "ṫuć tfı"),
        (33, "şıć şı"),
        (49, "pĺ'ıć bğu"),
        (57, "tfıć blı"),
        (68, "xıć yi"),
        (74, "blıć pĺ'ı"),
        (86, "yić xı"),
        (99, "bğuć bğu"),
    ])
    def test_tens_with_ones(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected


# ============================================================
# HUNDREDS (100-999)
# ============================================================
class TestHundreds:
    @pytest.mark.parametrize("number, expected", [
        (100, "şe"),
        (200, "ṫu şe"),
        (300, "şı şe"),
        (400, "pĺ'ı şe"),
        (500, "tfı şe"),
        (600, "xı şe"),
        (700, "blı şe"),
        (800, "yi şe"),
        (900, "bğu şe"),
    ])
    def test_round_hundreds(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected

    @pytest.mark.parametrize("number, expected", [
        (101, "şe zı"),
        (110, "şe zıć"),
        (111, "şe zıć zı"),
        (150, "şe tfıć"),
        (199, "şe bğuć bğu"),
        (250, "ṫu şe tfıć"),
        (999, "bğu şe bğuć bğu"),
    ])
    def test_hundreds_with_tens_and_ones(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected


# ============================================================
# THOUSANDS (1000+)
# ============================================================
class TestThousands:
    @pytest.mark.parametrize("number, expected", [
        (1000, "min"),
        (2000, "ṫu min"),
        (3000, "şı min"),
        (10000, "zıć min"),
        (100000, "şe min"),
        (999000, "bğu şe bğuć bğu min"),
    ])
    def test_round_thousands(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected

    @pytest.mark.parametrize("number, expected", [
        (1001, "min zı"),
        (1010, "min zıć"),
        (1100, "min şe"),
        (1983, "min bğu şe yić şı"),
        (2025, "ṫu min ṫuć tfı"),
        (10001, "zıć min zı"),
        (12345, "zıć ṫu min şı şe pĺ'ıć tfı"),
        (100001, "şe min zı"),
        (999999, "bğu şe bğuć bğu min bğu şe bğuć bğu"),
    ])
    def test_thousands_with_remainder(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected


# ============================================================
# LARGE NUMBERS (millions, billions, trillions)
# ============================================================
class TestLargeNumbers:
    @pytest.mark.parametrize("number, expected", [
        (1_000_000, "milyon"),
        (2_000_000, "ṫu milyon"),
        (1_000_001, "milyon zı"),
        (1_001_000, "milyon zı min"),
        (1_001_001, "milyon zı min zı"),
        (5_432_100, "tfı milyon pĺ'ı şe şıć ṫu min şe"),
    ])
    def test_millions(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected

    @pytest.mark.parametrize("number, expected", [
        (1_000_000_000, "milyard"),
        (2_000_000_000, "ṫu milyard"),
        (1_000_000_001, "milyard zı"),
    ])
    def test_billions(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected

    @pytest.mark.parametrize("number, expected", [
        (1_000_000_000_000, "trilyon"),
        (5_000_000_000_000, "tfı trilyon"),
        (1_000_000_000_001, "trilyon zı"),
    ])
    def test_trillions(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected

    def test_max_valid_number(self):
        result = AdigaNumberUtils.number_to_words(999_999_999_999_999)
        assert result == "bğu şe bğuć bğu trilyon bğu şe bğuć bğu milyard bğu şe bğuć bğu milyon bğu şe bğuć bğu min bğu şe bğuć bğu"


# ============================================================
# OVERFLOW
# ============================================================
class TestOverflow:
    def test_at_max(self):
        assert AdigaNumberUtils.number_to_words(1_000_000_000_000_000) == "trilyonım yeḣu'"

    def test_above_max(self):
        assert AdigaNumberUtils.number_to_words(9_999_999_999_999_999) == "trilyonım yeḣu'"


# ============================================================
# LEADING ZEROS
# ============================================================
class TestLeadingZeros:
    @pytest.mark.parametrize("digit_string, expected", [
        ("0", "ziy"),
        ("00", "ziy ziy"),
        ("000", "ziy ziy ziy"),
        ("007", "ziy ziy blı"),
        ("01", "ziy zı"),
        ("010", "ziy zıć"),
        ("0123", "ziy şe ṫuć şı"),
    ])
    def test_leading_zeros(self, digit_string, expected):
        assert AdigaNumberUtils._convert_digit_string_to_words(digit_string) == expected


# ============================================================
# ZERO TRIPLETS (numbers with zeros in the middle)
# ============================================================
class TestZeroTriplets:
    @pytest.mark.parametrize("number, expected", [
        (1_000_001, "milyon zı"),
        (1_000_100, "milyon şe"),
        (10_000_000, "zıć milyon"),
        (1_000_000_001, "milyard zı"),
        (1_001_000_000, "milyard zı milyon"),
        (100_000_000_000, "şe milyard"),
    ])
    def test_zero_triplets_in_middle(self, number, expected):
        assert AdigaNumberUtils.number_to_words(number) == expected


# ============================================================
# TEXT CONVERSION
# ============================================================
class TestConvertNumbersInText:
    def test_user_example(self):
        text = "the year was 1,983 when I started high school"
        expected = "the year was min bğu şe yić şı when I started high school"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_plain_number_in_text(self):
        text = "I have 5 apples"
        expected = "I have tfı apples"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_multiple_numbers(self):
        text = "from 10 to 20"
        expected = "from zıć to ṫuć"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_no_numbers(self):
        text = "no numbers here"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == text

    def test_number_at_start(self):
        text = "100 people"
        expected = "şe people"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_number_at_end(self):
        text = "chapter 3"
        expected = "chapter şı"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_number_only(self):
        text = "42"
        expected = "pĺ'ıć ṫu"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_comma_separated_large(self):
        text = "population is 1,000,000"
        expected = "population is milyon"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_leading_zeros_in_text(self):
        text = "agent 007"
        expected = "agent ziy ziy blı"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_zero_standalone(self):
        text = "score is 0"
        expected = "score is ziy"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_overflow_in_text(self):
        text = "the number 9999999999999999 is huge"
        expected = "the number trilyonım yeḣu' is huge"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_adjacent_numbers(self):
        text = "dial 1 800 555"
        expected = "dial zı yi şe tfı şe tfıć tfı"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_preserves_punctuation(self):
        text = "in (1983) they"
        expected = "in (min bğu şe yić şı) they"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected

    def test_year_2025(self):
        text = "the year 2025"
        expected = "the year ṫu min ṫuć tfı"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# EDGE CASES
# ============================================================
class TestEdgeCases:
    def test_empty_string(self):
        assert AdigaNumberUtils.convert_numbers_in_text("") == ""

    def test_none(self):
        assert AdigaNumberUtils.convert_numbers_in_text(None) is None

    def test_whitespace_only(self):
        assert AdigaNumberUtils.convert_numbers_in_text("   ") == "   "

    def test_single_digit_in_text(self):
        text = "I ate 1 cookie"
        expected = "I ate zı cookie"
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# POSTFIX WITH DASH
# ============================================================
class TestPostfixDash:
    @pytest.mark.parametrize("text, expected", [
        ("13-re", "zıć şıre"),
        ("36-će", "şıć xıće"),
        ("1-2-će", "zı ṫuće"),
        ("12-m", "zıć ṫum"),
        ("50,000-m", "tfıć minım"),
        ("12-nere", "zıć ṫunere"),
        ("2010/11-m", "ṫu min zıć zıć zım"),
    ])
    def test_postfix_dash(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# POSTFIX SYMBOLS (no dash)
# ============================================================
class TestPostfixSymbols:
    @pytest.mark.parametrize("text, expected", [
        ("804+", "yi şe pĺ'ı xaḣo"),
        ("65-", "xıć tfı xećı"),
        ("4%", "pĺ'ı pérsént"),
    ])
    def test_postfix_symbols(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# PREFIX WITH DASH
# ============================================================
class TestPrefixDash:
    @pytest.mark.parametrize("text, expected", [
        ("ya-20", "yaṫuć"),
    ])
    def test_prefix_dash(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# PREFIX SYMBOLS (no dash)
# ============================================================
class TestPrefixSymbols:
    @pytest.mark.parametrize("text, expected", [
        ("+14", "positif zıć pĺ'ı"),
        ("-32", "négatif şıć ṫu"),
        ("$16,918", "zıć xı min bğu şe zıć yi dolar"),
    ])
    def test_prefix_symbols(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# DECIMAL NUMBERS
# ============================================================
class TestDecimalNumbers:
    @pytest.mark.parametrize("text, expected", [
        ("+5.1", "positif tfı fı zı"),
        ("-0.053", "négatif ziy fı ziy tfıć şı"),
        ("5.11", "tfı fı zıć zı"),
    ])
    def test_decimal_numbers(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# MULTI-DOT NUMBERS
# ============================================================
class TestMultiDotNumbers:
    @pytest.mark.parametrize("text, expected", [
        ("28.57.23", "ṫuć yi fı tfıć blı fı ṫuć şı"),
    ])
    def test_multi_dot(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# DECIMAL WITH PERCENT
# ============================================================
class TestDecimalPercent:
    @pytest.mark.parametrize("text, expected", [
        ("50.06%", "tfıć fı ziy xı pérsént"),
    ])
    def test_decimal_percent(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# RANGES (number-number)
# ============================================================
class TestRanges:
    @pytest.mark.parametrize("text, expected", [
        ("1042-1814", "min pĺ'ıć ṫu min yi şe zıć pĺ'ı"),
        ("1040 - 1815", "min pĺ'ıć min yi şe zıć tfı"),
        ("7-12+", "blı zıć ṫu xaḣo"),
    ])
    def test_ranges(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# SLASH-SEPARATED NUMBERS
# ============================================================
class TestSlashSeparated:
    @pytest.mark.parametrize("text, expected", [
        ("2010/11", "ṫu min zıć zıć zı"),
    ])
    def test_slash(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# PHONE NUMBERS
# ============================================================
class TestPhoneNumbers:
    @pytest.mark.parametrize("text, expected", [
        ("+972-582062315", "positif bğu blı ṫu tfı yi ṫu ziy xı ṫu şı zı tfı"),
        ("+972-58-206-2315", "positif bğu blı ṫu tfı yi ṫu ziy xı ṫu şı zı tfı"),
        ("058-206-2315", "ziy tfı yi ṫu ziy xı ṫu şı zı tfı"),
    ])
    def test_phone_numbers(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# ROMAN NUMERALS
# ============================================================
class TestRomanNumerals:
    @pytest.mark.parametrize("text, expected", [
        ("II", "ṫu"),
        ("III", "şı"),
        ("IV", "pĺ'ı"),
        ("I.", "zı"),
        ("V.", "tfı"),
        ("II.", "ṫu"),
        ("III.", "şı"),
        ("IV.", "pĺ'ı"),
        ("V.", "tfı"),
        ("XIV", "zıć pĺ'ı"),
    ])
    def test_roman_numerals(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# VOWEL INSERTION (postfix helper)
# ============================================================
class TestVowelInsertion:
    @pytest.mark.parametrize("words, postfix, expected", [
        ("zıć ṫu", "m", "zıć ṫum"),          # ṫu ends in vowel u
        ("tfıć min", "m", "tfıć minım"),       # min ends in consonant n
        ("zıć zı", "m", "zıć zım"),            # zı ends in vowel ı
        ("zıć ṫu", "nere", "zıć ṫunere"),      # vowel ending, no insertion
        ("şıć xı", "će", "şıć xıće"),          # vowel ending
    ])
    def test_vowel_insertion(self, words, postfix, expected):
        assert AdigaNumberUtils._append_postfix(words, postfix) == expected


# ============================================================
# DECIMAL WITH PLUS/MINUS SUFFIX
# ============================================================
class TestDecimalSuffix:
    @pytest.mark.parametrize("text, expected", [
        ("7.3+", "blı fı şı xaḣo"),
        ("7.3-", "blı fı şı xećı"),
        ("1.5+", "zı fı tfı xaḣo"),
        ("1.5-", "zı fı tfı xećı"),
        ("0.1+", "ziy fı zı xaḣo"),
        ("0.1-", "ziy fı zı xećı"),
    ])
    def test_decimal_suffix(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# SIGN PREFIX WITH PERCENT
# ============================================================
class TestSignPrefixPercent:
    @pytest.mark.parametrize("text, expected", [
        ("+5.1%", "positif tfı fı zı pérsént"),
        ("-0.053%", "négatif ziy fı ziy tfıć şı pérsént"),
    ])
    def test_sign_prefix_percent(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# RANGE WITH PERCENT
# ============================================================
class TestRangePercent:
    @pytest.mark.parametrize("text, expected", [
        ("7-12%", "blı zıć ṫu pérsént"),
    ])
    def test_range_percent(self, text, expected):
        assert AdigaNumberUtils.convert_numbers_in_text(text) == expected


# ============================================================
# CLI INTERFACE
# ============================================================


def run_num_cli(*args):
    """Helper: run the number utils script with the given arguments."""
    return subprocess.run(
        [sys.executable, '-m', 'adyghe_latin_utils.number_utils', *args],
        capture_output=True,
        text=True,
    )


class TestCli:

    def test_text_flag_to_stdout(self):
        result = run_num_cli('-t', '42 100 2024')
        assert result.returncode == 0
        assert "pĺ'ıć ṫu şe ṫu min ṫuć pĺ'ı" in result.stdout

    def test_input_file(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('I have 5 apples\n', encoding='utf-8')
        result = run_num_cli('-i', str(infile))
        assert result.returncode == 0
        assert 'tfı' in result.stdout

    def test_output_file(self, tmp_path):
        outfile = tmp_path / 'output.txt'
        result = run_num_cli('-t', '42', '-o', str(outfile))
        assert result.returncode == 0
        output = outfile.read_text(encoding='utf-8')
        assert "pĺ'ıć ṫu" in output

    def test_input_and_output_file(self, tmp_path):
        infile = tmp_path / 'input.txt'
        outfile = tmp_path / 'output.txt'
        infile.write_text('the year 2025\n', encoding='utf-8')
        result = run_num_cli('-i', str(infile), '-o', str(outfile))
        assert result.returncode == 0
        output = outfile.read_text(encoding='utf-8')
        assert 'ṫu min ṫuć tfı' in output

    def test_mutually_exclusive_flags(self):
        result = run_num_cli('-i', '/dev/null', '-t', 'hello')
        assert result.returncode != 0

    def test_no_input_flag(self):
        result = run_num_cli()
        assert result.returncode != 0

    def test_stderr_shows_stats(self):
        result = run_num_cli('-t', '123')
        assert result.returncode == 0
        assert 'Completed in' in result.stderr
        assert 'chars/s' in result.stderr

    def test_mixed_text_with_numbers(self):
        result = run_num_cli('-t', 'I ate 3 of the 12 cookies')
        assert result.returncode == 0
        assert result.stdout.strip() == 'I ate şı of the zıć ṫu cookies'

    def test_multiline_file(self, tmp_path):
        infile = tmp_path / 'input.txt'
        infile.write_text('year 2025\ncount 100\n', encoding='utf-8')
        result = run_num_cli('-i', str(infile))
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert len(lines) == 2
        assert 'ṫu min ṫuć tfı' in lines[0]
        assert 'şe' in lines[1]
