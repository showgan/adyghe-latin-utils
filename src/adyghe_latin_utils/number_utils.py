import argparse
import re
import sys
import time
from typing import Optional


class AdigaNumberUtils:
    MAX_NUMBER = 1_000_000_000_000_000  # 10^15
    OVERFLOW_TEXT = "trilyonım yeḣu'"

    DIGITS_WORD_MAP = {
        "0": "ziy",
        "1": "zı",
        "2": "ṫu",
        "3": "şı",
        "4": "pĺ'ı",
        "5": "tfı",
        "6": "xı",
        "7": "blı",
        "8": "yi",
        "9": "bğu",
    }

    TRIPLET_SCALE_MAP = {
        1: "min",
        2: "milyon",
        3: "milyard",
        4: "trilyon",
    }

    ADYGHE_VOWELS = {'a', 'e', 'ı', 'i', 'o', 'u', 'é'}

    ROMAN_VALUES = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    # A NUM token: digits optionally with comma-thousands grouping
    _NUM = r'\d{1,3}(?:,\d{3})+|\d+'
    # Adyghe Latin letters (including special chars used in the language)
    _LETTER = r"[a-zA-Zçćéğḣĺṫışžǯʻʼ'']"

    _ENHANCED_PATTERN = re.compile(
        r'(?:'
        # Group 1: International phone +XXX-digits(-digits)*
        r'(\+\d{1,3}(?:-\d+)+)'
        r'|'
        # Group 2: Local phone 0XX-XXX-XXXX (at least 2 dash-groups)
        r'(0\d{1,2}(?:-\d+){2,})'
        r'|'
        # Group 3: Text prefix-dash-number: ya-20
        r'(' + _LETTER + r'+-(?:' + _NUM + r')(?:[/-](?:' + _NUM + r'))*)'
        r'|'
        # Group 4: Number(s)-dash-text postfix: 13-re, 1-2-će, 2010/11-m
        r'((?:' + _NUM + r')(?:[/-](?:' + _NUM + r'))*-' + _LETTER + r'+)'
        r'|'
        # Group 5: Dollar sign prefix: $16,918
        r'(\$(?:' + _NUM + r')(?:\.(?:' + _NUM + r'))?)'
        r'|'
        # Group 6: Sign prefix with optional decimal and optional trailing symbol
        r'([+-](?:' + _NUM + r')(?:\.(?:' + _NUM + r'))?[%]?)'
        r'|'
        # Group 7: Number range with optional spaces around dash, optional trailing symbol
        r'((?:' + _NUM + r')\s*-\s*(?:' + _NUM + r')[%+]?)'
        r'|'
        # Group 8: Decimal or multi-dot number with optional trailing symbol
        r'((?:' + _NUM + r')(?:\.(?:' + _NUM + r'))+[%+\-]?)'
        r'|'
        # Group 9: Slash-separated numbers: 2010/11
        r'((?:' + _NUM + r')(?:/(?:' + _NUM + r'))+)'
        r'|'
        # Group 10: Plain number with symbol postfix: 4%, 804+, 65-
        r'((?:' + _NUM + r')[%+\-])'
        r'|'
        # Group 11: Roman numerals with optional dot (2+ chars, or 1 char with dot)
        r'(?<![a-zA-Z])([IVXLCDM]{2,}\.?|[IVXLCDM]\.)(?![a-zA-Z])'
        r'|'
        # Group 12: Plain or comma-separated number (existing)
        r'(' + _NUM + r')'
        r')'
    )

    @staticmethod
    def _divide_to_triplets(number_str: str) -> list:
        triplets = []
        i = len(number_str)
        while i > 0:
            start = max(0, i - 3)
            triplet = number_str[start:i]
            triplets.append(triplet)
            i -= 3
        return triplets

    @classmethod
    def _convert_triplet_to_words(cls, triplet: str) -> str:
        length = len(triplet)
        if length == 1:
            return cls.DIGITS_WORD_MAP[triplet]

        if length == 2:
            tens = triplet[0]
            ones = triplet[1]
            if tens == "0":
                if ones == "0":
                    return ""
                return cls.DIGITS_WORD_MAP[ones]
            if ones == "0":
                return cls.DIGITS_WORD_MAP[tens] + "ć"
            return cls.DIGITS_WORD_MAP[tens] + "ć " + cls.DIGITS_WORD_MAP[ones]

        # length == 3
        hundreds_digit = triplet[0]
        tens = triplet[1]
        ones = triplet[2]

        if hundreds_digit == "1":
            hundreds = "şe"
        elif hundreds_digit == "0":
            hundreds = ""
        else:
            hundreds = cls.DIGITS_WORD_MAP[hundreds_digit] + " şe"

        if tens == "0":
            if ones == "0":
                remainder = ""
            else:
                remainder = cls.DIGITS_WORD_MAP[ones]
        else:
            if ones == "0":
                remainder = cls.DIGITS_WORD_MAP[tens] + "ć"
            else:
                remainder = cls.DIGITS_WORD_MAP[tens] + "ć " + cls.DIGITS_WORD_MAP[ones]

        if hundreds and remainder:
            return hundreds + " " + remainder
        return hundreds + remainder

    @classmethod
    def number_to_words(cls, number: int) -> str:
        if number == 0:
            return "ziy"
        if number >= cls.MAX_NUMBER:
            return cls.OVERFLOW_TEXT

        number_str = str(number)
        triplets = cls._divide_to_triplets(number_str)
        num_triplets = len(triplets)

        parts = []
        for i in range(num_triplets - 1, -1, -1):
            triplet_str = triplets[i]
            triplet_words = cls._convert_triplet_to_words(triplet_str)
            if not triplet_words:
                continue
            if i > 0:
                scale = cls.TRIPLET_SCALE_MAP.get(i, "")
                if scale:
                    parts.append(triplet_words + " " + scale)
                else:
                    parts.append(triplet_words)
            else:
                parts.append(triplet_words)

        result = " ".join(parts)

        # Match Java: strip leading "zı " (so 1000 -> "min", not "zı min")
        if result.startswith("zı "):
            result = result[3:]

        return result

    @classmethod
    def _convert_digit_string_to_words(cls, digit_string: str) -> str:
        if not digit_string:
            return ""

        # Count leading zeros
        leading_zeros = len(digit_string) - len(digit_string.lstrip("0"))

        if leading_zeros == len(digit_string):
            # All zeros
            return " ".join(["ziy"] * len(digit_string))

        prefix_parts = ["ziy"] * leading_zeros
        remaining = int(digit_string)
        suffix = cls.number_to_words(remaining)

        if prefix_parts:
            return " ".join(prefix_parts) + " " + suffix
        return suffix

    @classmethod
    def _convert_number_string(cls, number_str: str) -> str:
        digits = number_str.replace(",", "")
        return cls._convert_digit_string_to_words(digits)

    @classmethod
    def _is_vowel(cls, char: str) -> bool:
        return char.lower() in cls.ADYGHE_VOWELS

    @classmethod
    def _append_postfix(cls, words: str, postfix: str) -> str:
        word_list = words.split()
        if not word_list:
            return postfix
        last_word = word_list[-1]
        last_char = last_word[-1] if last_word else ""
        if last_char and not cls._is_vowel(last_char):
            word_list[-1] = last_word + "ı" + postfix
        else:
            word_list[-1] = last_word + postfix
        return " ".join(word_list)

    @staticmethod
    def _prepend_prefix(words: str, prefix: str) -> str:
        word_list = words.split()
        if not word_list:
            return prefix
        word_list[0] = prefix + word_list[0]
        return " ".join(word_list)

    @classmethod
    def _convert_dotted_number(cls, number_str: str) -> str:
        segments = number_str.split(".")
        converted = [cls._convert_number_string(seg) for seg in segments]
        return " fı ".join(converted)

    @classmethod
    def _convert_phone_digits(cls, digit_str: str) -> str:
        return " ".join(cls.DIGITS_WORD_MAP[d] for d in digit_str if d in cls.DIGITS_WORD_MAP)

    @staticmethod
    def _roman_to_int(roman_str: str) -> Optional[int]:
        values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        total = 0
        prev = 0
        for ch in reversed(roman_str):
            val = values.get(ch)
            if val is None:
                return None
            if val < prev:
                total -= val
            else:
                total += val
            prev = val
        return total if total > 0 else None

    @classmethod
    def convert_numbers_in_text(cls, text: str) -> str:
        if not text:
            return text

        def replace_match(match: re.Match) -> str:
            # Determine which group matched
            for group_idx in range(1, 13):
                captured = match.group(group_idx)
                if captured is not None:
                    return cls._dispatch(group_idx, captured)
            return match.group(0)

        return cls._ENHANCED_PATTERN.sub(replace_match, text)

    @classmethod
    def _dispatch(cls, group: int, matched: str) -> str:
        if group == 1:
            return cls._handle_international_phone(matched)
        if group == 2:
            return cls._handle_local_phone(matched)
        if group == 3:
            return cls._handle_prefix_dash(matched)
        if group == 4:
            return cls._handle_postfix_dash(matched)
        if group == 5:
            return cls._handle_dollar(matched)
        if group == 6:
            return cls._handle_sign_prefix(matched)
        if group == 7:
            return cls._handle_range(matched)
        if group == 8:
            return cls._handle_dotted(matched)
        if group == 9:
            return cls._handle_slash(matched)
        if group == 10:
            return cls._handle_symbol_postfix(matched)
        if group == 11:
            return cls._handle_roman(matched)
        if group == 12:
            return cls._handle_plain(matched)
        return matched

    @classmethod
    def _handle_international_phone(cls, matched: str) -> str:
        # +972-58-206-2315 -> strip + and dashes, convert digit by digit
        digits = matched.replace("-", "").replace("+", "")
        return "positif " + cls._convert_phone_digits(digits)

    @classmethod
    def _handle_local_phone(cls, matched: str) -> str:
        # 058-206-2315 -> strip dashes, convert digit by digit
        digits = matched.replace("-", "")
        return cls._convert_phone_digits(digits)

    @classmethod
    def _handle_prefix_dash(cls, matched: str) -> str:
        # ya-20 -> find first dash before digits
        idx = matched.index("-")
        prefix = matched[:idx]
        number_part = matched[idx + 1:]
        # number_part could contain slashes or dashes between numbers
        segments = re.split(r'[/-]', number_part)
        converted_parts = [cls._convert_number_string(seg) for seg in segments]
        words = " ".join(converted_parts)
        return cls._prepend_prefix(words, prefix)

    @classmethod
    def _handle_postfix_dash(cls, matched: str) -> str:
        # 13-re, 1-2-će, 2010/11-m
        # Find the last dash that is followed by letters (the postfix)
        m = re.match(r'^(.*)-(' + cls._LETTER + r'+)$', matched)
        if not m:
            return matched
        number_part = m.group(1)
        postfix = m.group(2)
        # number_part could be "13", "1-2", "2010/11"
        segments = re.split(r'[/-]', number_part)
        converted_parts = [cls._convert_number_string(seg) for seg in segments]
        words = " ".join(converted_parts)
        return cls._append_postfix(words, postfix)

    @classmethod
    def _handle_dollar(cls, matched: str) -> str:
        # $16,918 -> convert number, append " dolar"
        core = matched[1:]  # strip $
        if "." in core:
            words = cls._convert_dotted_number(core)
        else:
            words = cls._convert_number_string(core)
        return words + " dolar"

    @classmethod
    def _handle_sign_prefix(cls, matched: str) -> str:
        # +14, -32, +5.1, -0.053, +5.1%
        sign = matched[0]
        sign_word = "positif" if sign == "+" else "négatif"
        core = matched[1:]
        # Check for trailing %
        suffix_word = ""
        if core.endswith("%"):
            core = core[:-1]
            suffix_word = " pérsént"
        if "." in core:
            words = cls._convert_dotted_number(core)
        else:
            words = cls._convert_number_string(core)
        return sign_word + " " + words + suffix_word

    @classmethod
    def _handle_range(cls, matched: str) -> str:
        # 1042-1814, 1040 - 1815, 7-12+
        # Check for trailing symbol
        suffix_word = ""
        core = matched
        if core.endswith("%"):
            core = core[:-1]
            suffix_word = " pérsént"
        elif core.endswith("+"):
            core = core[:-1]
            suffix_word = " xaḣo"
        # Split on dash with optional spaces
        parts = re.split(r'\s*-\s*', core)
        converted = [cls._convert_number_string(p) for p in parts]
        return " ".join(converted) + suffix_word

    @classmethod
    def _handle_dotted(cls, matched: str) -> str:
        # 5.11, 50.06%, 28.57.23, 7.3+, 7.3-
        suffix_word = ""
        core = matched
        if core.endswith("%"):
            core = core[:-1]
            suffix_word = " pérsént"
        elif core.endswith("+"):
            core = core[:-1]
            suffix_word = " xaḣo"
        elif core.endswith("-"):
            core = core[:-1]
            suffix_word = " xećı"
        return cls._convert_dotted_number(core) + suffix_word

    @classmethod
    def _handle_slash(cls, matched: str) -> str:
        # 2010/11 -> convert each part, join with space
        parts = matched.split("/")
        converted = [cls._convert_number_string(p) for p in parts]
        return " ".join(converted)

    @classmethod
    def _handle_symbol_postfix(cls, matched: str) -> str:
        # 4%, 804+, 65-
        symbol = matched[-1]
        number_str = matched[:-1]
        words = cls._convert_number_string(number_str)
        if symbol == "%":
            return words + " pérsént"
        if symbol == "+":
            return words + " xaḣo"
        if symbol == "-":
            return words + " xećı"
        return words

    @classmethod
    def _handle_roman(cls, matched: str) -> str:
        # III, IV., strip trailing dot
        roman = matched.rstrip(".")
        if not roman:
            return matched
        value = cls._roman_to_int(roman)
        if value is None:
            return matched
        return cls.number_to_words(value)

    @classmethod
    def _handle_plain(cls, matched: str) -> str:
        digits = matched.replace(",", "")
        return cls._convert_digit_string_to_words(digits)


def main():
    parser = argparse.ArgumentParser(
        description='Convert numbers in text to Adyghe (Circassian) words.'
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-i', '--input',
                             help='Path to the input text file')
    input_group.add_argument('-t', '--text',
                             help='Input text string containing numbers')
    parser.add_argument('-o', '--output', default=None,
                        help='Path to the output text file (default: stdout)')
    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r', encoding='utf-8') as infile:
            text = infile.read()
        source_label = args.input
    else:
        text = args.text
        source_label = '<text>'

    total_chars = len(text)
    print(f'Input:      {source_label}', file=sys.stderr)
    print(f'Output:     {args.output if args.output else "<stdout>"}',
          file=sys.stderr)
    print(f'Characters: {total_chars}', file=sys.stderr)
    print(file=sys.stderr)

    start_time = time.time()
    result = AdigaNumberUtils.convert_numbers_in_text(text)
    elapsed = time.time() - start_time

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as outfile:
            outfile.write(result)
    else:
        sys.stdout.write(result)
        if not result.endswith('\n'):
            sys.stdout.write('\n')

    chars_per_sec = total_chars / elapsed if elapsed > 0 else 0
    print(file=sys.stderr)
    print(f'Completed in {elapsed:.3f}s', file=sys.stderr)
    print(f'Speed: {chars_per_sec:,.0f} chars/s', file=sys.stderr)


if __name__ == '__main__':
    main()
