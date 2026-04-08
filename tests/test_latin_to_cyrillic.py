#!/usr/bin/env python3
"""
Comprehensive test suite for AdigaCharacterUtils.latin_to_cyrillic().

Covers:
- Every single-character Latin-to-Cyrillic mapping
- 2-character compound mappings
- 4-character compound mappings
- Prefix rules (1-char and 2-char word-initial)
- Context-aware vowel insertion rules (vowel after vowel)
- Capitalization preservation
- Multi-word sentences
- Roundtrip consistency (cyrillic_to_latin -> latin_to_cyrillic)
- Edge cases (empty, None, whitespace, punctuation prefix)
"""
import pytest

from adyghe_latin_utils.character_utils import AdigaCharacterUtils


@pytest.fixture(scope="module")
def utils():
    return AdigaCharacterUtils()


# ============================================================
# SINGLE CHARACTER MAPPINGS
# ============================================================

class TestSingleCharMappings:
    """Test each single-character Latin-to-Cyrillic mapping mid-word."""

    @pytest.mark.parametrize("latin,expected_cyrillic", [
        ("'", "Ӏ"),
        ("a", "а"),
        ("s", "с"),
        ("d", "д"),
        ("f", "ф"),
        ("g", "г"),
        ("h", "хь"),
        ("j", "ж"),
        ("k", "къ"),
        ("l", "л"),
        ("i", "и"),
        ("q", "кӀ"),
        ("w", "у"),
        ("e", "э"),
        ("r", "р"),
        ("t", "т"),
        ("y", "и"),
        ("u", "у"),
        ("o", "о"),
        ("p", "п"),
        ("z", "з"),
        ("x", "х"),
        ("c", "дж"),
        ("v", "в"),
        ("b", "б"),
        ("n", "н"),
        ("m", "м"),
    ])
    def test_basic_latin_char(self, utils, latin, expected_cyrillic):
        # Wrap in consonants to avoid prefix rules
        result = utils.latin_to_cyrillic('n' + latin + 'n')
        assert result.startswith('н')
        assert result.endswith('н')
        middle = result[1:-1]
        assert middle == expected_cyrillic, \
            f"'{latin}' mid-word: expected '{expected_cyrillic}', got '{middle}'"

    @pytest.mark.parametrize("latin,expected_cyrillic", [
        ("á", "а"),
        ("ç", "ч"),
        ("ć", "кӀ"),
        ("é", "е"),
        ("ǵ", "г"),
        ("ğ", "гъ"),
        ("ḣ", "хъ"),
        ("ı", "ы"),
        ("ḱ", "к"),
        ("ĺ", "лъ"),
        ("ö", "о"),
        ("ṕ", "пӀ"),
        ("ş", "ш"),
        ("ś", "ц"),
        ("š", "цӀ"),
        ("ṫ", "тӀ"),
        ("ź", "дз"),
    ])
    def test_special_latin_char(self, utils, latin, expected_cyrillic):
        result = utils.latin_to_cyrillic('n' + latin + 'n')
        assert result.startswith('н')
        assert result.endswith('н')
        middle = result[1:-1]
        assert middle == expected_cyrillic, \
            f"'{latin}' mid-word: expected '{expected_cyrillic}', got '{middle}'"


# ============================================================
# 2-CHARACTER COMPOUND MAPPINGS
# ============================================================

class TestTwoCharCompounds:
    """Test 2-character Latin-to-Cyrillic compound mappings mid-word."""

    @pytest.mark.parametrize("latin,expected_cyrillic", [
        ("aá", "Ӏа"),
        ("jü", "жъу"),
        ("jö", "жъо"),
        ("wı", "у"),
        ("we", "о"),
        ("ya", "я"),
        ("yu", "ю"),
        ("ye", "е"),
        ("oá", "уа"),
        ("çö", "цо"),
        ("çü", "цу"),
        ("ĺ'", "лӀ"),
        ("şü", "шъу"),
        ("şö", "шъо"),
        ("ş'", "шӀ"),
    ])
    def test_two_char_compound_mid_word(self, utils, latin, expected_cyrillic):
        result = utils.latin_to_cyrillic('n' + latin + 'n')
        assert result.startswith('н')
        assert result.endswith('н')
        middle = result[1:-1]
        assert middle == expected_cyrillic, \
            f"'{latin}' mid-word: expected '{expected_cyrillic}', got '{middle}'"


# ============================================================
# 4-CHARACTER COMPOUND MAPPINGS
# ============================================================

class TestFourCharCompounds:
    """Test 4-character Latin-to-Cyrillic compound mappings mid-word."""

    @pytest.mark.parametrize("latin,expected_cyrillic", [
        ("şü'e", "шӀо"),
        ("şü'ı", "шӀу"),
    ])
    def test_four_char_compound_mid_word(self, utils, latin, expected_cyrillic):
        result = utils.latin_to_cyrillic('n' + latin + 'n')
        assert result.startswith('н')
        assert result.endswith('н')
        middle = result[1:-1]
        assert middle == expected_cyrillic, \
            f"'{latin}' mid-word: expected '{expected_cyrillic}', got '{middle}'"


# ============================================================
# PREFIX RULES (word-initial)
# ============================================================

class TestPrefixOneChar:
    """Test 1-character prefix mappings at word start."""

    @pytest.mark.parametrize("latin,expected_prefix", [
        ("ı", "ы"),
        ("e", "Ӏэ"),
        ("o", "Ӏо"),
        ("u", "Ӏу"),
    ])
    def test_prefix_1_char(self, utils, latin, expected_prefix):
        result = utils.latin_to_cyrillic(latin + 'n')
        assert result.startswith(expected_prefix), \
            f"'{latin}n': expected start '{expected_prefix}', got '{result}'"
        assert result.endswith('н')


class TestPrefixTwoChars:
    """Test 2-character prefix mappings at word start."""

    @pytest.mark.parametrize("latin,expected_prefix", [
        ("yi", "и"),
        ("ye", "е"),
        ("aá", "Ӏа"),
    ])
    def test_prefix_2_char(self, utils, latin, expected_prefix):
        result = utils.latin_to_cyrillic(latin + 'n')
        assert result.startswith(expected_prefix), \
            f"'{latin}n': expected start '{expected_prefix}', got '{result}'"
        assert result.endswith('н')


# ============================================================
# CONTEXT-AWARE VOWEL RULES (vowel after vowel)
# ============================================================

class TestContextAwareVowelRules:
    """Test vowel-after-vowel palochka insertion rules."""

    @pytest.mark.parametrize("latin,expected", [
        ("neu", "нэӀу"),    # eu -> э + Ӏу
        ("nie", "ниӀэ"),    # ie -> и + Ӏэ
        ("neo", "нэӀо"),    # eo -> э + Ӏо
    ])
    def test_vowel_after_vowel_palochka(self, utils, latin, expected):
        result = utils.latin_to_cyrillic(latin)
        assert result == expected, \
            f"'{latin}': expected '{expected}', got '{result}'"

    @pytest.mark.parametrize("latin,expected_contains", [
        ("nau", "Ӏу"),      # u after vowel a -> Ӏу
        ("nao", "Ӏо"),      # o after vowel a -> Ӏо
        ("nae", "Ӏэ"),      # e after vowel a -> Ӏэ
    ])
    def test_vowel_after_a_inserts_palochka(self, utils, latin, expected_contains):
        result = utils.latin_to_cyrillic(latin)
        assert expected_contains in result, \
            f"'{latin}': expected '{expected_contains}' in '{result}'"


# ============================================================
# CAPITALIZATION
# ============================================================

class TestCapitalization:
    """Test capitalization preservation during conversion."""

    def test_first_letter_capitalized(self, utils):
        result = utils.latin_to_cyrillic('Selam')
        assert result == 'Сэлам'

    def test_special_char_capitalized(self, utils):
        result = utils.latin_to_cyrillic('Ḣan')
        assert result == 'ХЪан'

    def test_lowercase_word(self, utils):
        result = utils.latin_to_cyrillic('selam')
        assert result == 'сэлам'


# ============================================================
# MULTI-WORD SENTENCES
# ============================================================

class TestMultiWord:
    """Test conversion of multi-word text."""

    def test_two_words(self, utils):
        result = utils.latin_to_cyrillic('selam adıǵe')
        assert result == 'сэлам адыгэ'

    def test_preserves_whitespace(self, utils):
        result = utils.latin_to_cyrillic('selam  adıǵe')
        assert result == 'сэлам  адыгэ'


# ============================================================
# ROUNDTRIP CONSISTENCY (cyrillic -> latin -> cyrillic)
# ============================================================

class TestRoundtrip:
    """Test that cyrillic_to_latin -> latin_to_cyrillic recovers original."""

    @pytest.mark.parametrize("cyrillic", [
        'адыгэ',
        'сэлам',
        'тхылъ',
        'шъуашэ',
    ])
    def test_roundtrip(self, utils, cyrillic):
        latin = utils.cyrillic_to_latin(cyrillic)
        back = utils.latin_to_cyrillic(latin)
        assert back == cyrillic, \
            f"Roundtrip failed: '{cyrillic}' -> '{latin}' -> '{back}'"


# ============================================================
# EDGE CASES
# ============================================================

class TestEdgeCases:
    """Test edge cases for latin_to_cyrillic."""

    def test_empty_string(self, utils):
        assert utils.latin_to_cyrillic('') == ''

    def test_none(self, utils):
        assert utils.latin_to_cyrillic(None) is None

    def test_whitespace_only(self, utils):
        assert utils.latin_to_cyrillic('   ') == '   '

    def test_single_char(self, utils):
        result = utils.latin_to_cyrillic('n')
        assert result == 'н'

    def test_punctuation_prefix_paren(self, utils):
        result = utils.latin_to_cyrillic('(selam')
        assert result.startswith('(')
        assert 'сэлам' in result

    def test_punctuation_prefix_dash(self, utils):
        result = utils.latin_to_cyrillic('-selam')
        assert result.startswith('-')

    def test_numbers_pass_through(self, utils):
        result = utils.latin_to_cyrillic('n123n')
        # digits are not in the mapping, should pass through
        assert 'н' in result
