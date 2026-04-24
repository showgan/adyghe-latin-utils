#!/usr/bin/env python3
"""
Comprehensive test suite for AdigaCharacterUtils.cyrillic_to_latin().

This test suite serves as a regression safety net while fixing bugs in the
Cyrillic-to-Latin conversion. It covers:
- Known bugs from bad_conversions.txt
- Every mapping table entry (single, 2/3/4-char, prefix 1/2/3-char)
- Context-aware vowel combination rules
- Capitalization preservation
- Multi-word sentences
- Punctuation prefix handling (-, ()
- Words from the fineweb corpus (for regression after user review)
"""
import os
from pathlib import Path

import pytest

from adyghe_latin_utils.character_utils import AdigaCharacterUtils
from tests.regression_comparator import compare_lines_with_report, read_lines


@pytest.fixture(scope="module")
def utils():
    return AdigaCharacterUtils()


# ============================================================
# KNOWN BUGS from bad_conversions.txt
# These are marked xfail until fixed, then the marker is removed.
# ============================================================

class TestKnownBugs:
    """Tests for known conversion bugs from bad_conversions.txt."""

    def test_bug1_guа_mid_word(self, utils):
        # къагъэлъэгъуагъ: гъуа should produce ğoá not ğua
        assert utils.cyrillic_to_latin('къагъэлъэгъуагъ') == 'kağeĺeğoáğ'

    def test_bug2_palochka_prefix(self, utils):
        # IофшIэнхэр: word-initial I should not produce apostrophe
        assert utils.cyrillic_to_latin('IофшIэнхэр') == "ofş'enxer"

    def test_bug_word_ending_i_palochka(self, utils):
        # иӀ should not keep extra ı before apostrophe
        assert utils.cyrillic_to_latin('иӀ') == "yi'"

    def test_bug_word_ending_ya_palochka(self, utils):
        # яӀ should emit apostrophe, not raw palochka
        assert utils.cyrillic_to_latin('яӀ') == "ya'"

    def test_bug_i_palochka_ua_sequence(self, utils):
        # иӀуа at word start should remain explicit as yioá, not collapse to yi'wa
        assert utils.cyrillic_to_latin('иӀуагъ') == 'yioáğ'

    def test_bug_l2c_noninitial_ioa_sequence(self, utils):
        # Non-word-initial ioá should keep palochka: ...иӀуа...
        assert utils.latin_to_cyrillic('kıwioáğ') == 'къыуиӀуагъ'


# ============================================================
# SINGLE CHARACTER MAPPINGS
# ============================================================

class TestSingleCharMappings:
    """Test each single-character Cyrillic-to-Latin mapping."""

    @pytest.mark.parametrize("cyrillic,expected_latin", [
        ('а', 'a'),
        ('б', 'b'),
        ('в', 'v'),
        ('г', 'ǵ'),
        ('д', 'd'),
        ('е', 'é'),
        ('ж', 'j'),
        ('з', 'z'),
        ('к', 'ḱ'),
        ('л', 'l'),
        ('м', 'm'),
        ('н', 'n'),
        ('о', 'o'),
        ('п', 'p'),
        ('р', 'r'),
        ('с', 's'),
        ('т', 't'),
        ('ф', 'f'),
        ('х', 'x'),
        ('ц', 'ś'),
        ('ч', 'ç'),
        ('ш', 'ş'),
        ('ы', 'ı'),
        ('э', 'e'),
    ])
    def test_single_char(self, utils, cyrillic, expected_latin):
        # Single chars in isolation get prefix rules applied for some vowels,
        # so we test them mid-word by wrapping with consonants
        result = utils.cyrillic_to_latin('н' + cyrillic + 'н')
        # Extract the middle character(s) from the result
        assert result.startswith('n')
        assert result.endswith('n')
        middle = result[1:-1]
        assert middle == expected_latin, f"'{cyrillic}' mid-word: expected '{expected_latin}', got '{middle}'"

    def test_soft_sign_disappears(self, utils):
        # ь should produce empty string (disappear)
        result = utils.cyrillic_to_latin('нь')
        assert result == 'n'

    def test_yu(self, utils):
        result = utils.cyrillic_to_latin('нюн')
        assert 'yu' in result

    def test_ya(self, utils):
        result = utils.cyrillic_to_latin('нян')
        assert 'ya' in result


# ============================================================
# 2-CHARACTER COMPOUND MAPPINGS
# ============================================================

class TestTwoCharCompounds:
    """Test 2-character Cyrillic-to-Latin compound mappings."""

    @pytest.mark.parametrize("cyrillic,expected_latin", [
        ('гу', 'gu'),
        ('го', 'go'),
        ('гъ', 'ğ'),
        ('дж', 'c'),
        ('дз', 'ź'),
        ('жь', 'j'),
        ('кӀ', 'ć'),
        ('ку', 'ḱu'),
        ('къ', 'k'),
        ('лӀ', "ĺ'"),
        ('лъ', 'ĺ'),
        ('шъ', 'ş'),
        ('шӀ', "ş'"),
        ('пӀ', 'ṕ'),
        ('тӀ', 'ṫ'),
        ('хъ', 'ḣ'),
        ('хь', 'h'),
        ('цӀ', 'š'),
        ('жъ', 'j'),
        ('цо', 'çö'),
        ('цу', 'çü'),
        ('чӀ', 'ć'),
        ('чъ', 'ç'),
    ])
    def test_two_char_compound_mid_word(self, utils, cyrillic, expected_latin):
        # Wrap in consonants to avoid prefix rules
        result = utils.cyrillic_to_latin('н' + cyrillic + 'н')
        assert result.startswith('n')
        assert result.endswith('n')
        middle = result[1:-1]
        assert middle == expected_latin, f"'{cyrillic}' mid-word: expected '{expected_latin}', got '{middle}'"

    @pytest.mark.parametrize("cyrillic,expected_latin", [
        ('Ӏу', 'u'),
        ('Ӏэ', 'e'),
        ('Ӏа', 'aá'),
        ('Ӏо', "'o"),
        ('иӀ', "i'"),
        ('яӀ', "ya'"),
    ])
    def test_palochka_two_char_mid_word(self, utils, cyrillic, expected_latin):
        result = utils.cyrillic_to_latin('н' + cyrillic + 'н')
        assert result.startswith('n')
        assert result.endswith('n')
        middle = result[1:-1]
        assert middle == expected_latin, f"'{cyrillic}' mid-word: expected '{expected_latin}', got '{middle}'"

    @pytest.mark.parametrize("cyrillic,expected_latin", [
        ('уэ', 'we'),
        ('уи', 'wi'),
    ])
    def test_vowel_combination_two_char(self, utils, cyrillic, expected_latin):
        result = utils.cyrillic_to_latin('н' + cyrillic + 'н')
        assert result.startswith('n')
        assert result.endswith('n')
        middle = result[1:-1]
        assert middle == expected_latin, f"'{cyrillic}' mid-word: expected '{expected_latin}', got '{middle}'"


# ============================================================
# 3-CHARACTER COMPOUND MAPPINGS
# ============================================================

class TestThreeCharCompounds:
    """Test 3-character Cyrillic-to-Latin compound mappings."""

    @pytest.mark.parametrize("cyrillic,expected_latin", [
        ('жъу', 'jü'),
        ('жъо', 'jö'),
        ('кӀу', 'qu'),
        ('кӀо', 'qo'),
        ('кӀи', 'ći'),
        ('кӀы', 'ćı'),
        ('куа', 'ḱoá'),
        ('шъу', 'şü'),
        ('шъо', 'şö'),
        ('шӀо', "şü'e"),
        ('шӀу', "şü'ı"),
        ('шӀи', "ş'i"),
        ('пӀу', 'ṕu'),
        ('хъу', 'ḣu'),
        ('къу', 'ku'),
        ('тӀу', 'ṫu'),
        ('дзу', 'źu'),
    ])
    def test_three_char_compound_mid_word(self, utils, cyrillic, expected_latin):
        result = utils.cyrillic_to_latin('н' + cyrillic + 'н')
        assert result.startswith('n')
        assert result.endswith('n')
        middle = result[1:-1]
        assert middle == expected_latin, f"'{cyrillic}' mid-word: expected '{expected_latin}', got '{middle}'"


# ============================================================
# 4-CHARACTER COMPOUND MAPPINGS
# ============================================================

class TestFourCharCompounds:
    """Test 4-character Cyrillic-to-Latin compound mappings."""

    @pytest.mark.parametrize("cyrillic,expected_latin", [
        ('кӀуа', 'qoá'),
        ('кӀуэ', 'qo'),
        ('шӀои', "şü'ey"),
    ])
    def test_four_char_compound_mid_word(self, utils, cyrillic, expected_latin):
        result = utils.cyrillic_to_latin('н' + cyrillic + 'н')
        assert result.startswith('n')
        assert result.endswith('n')
        middle = result[1:-1]
        assert middle == expected_latin, f"'{cyrillic}' mid-word: expected '{expected_latin}', got '{middle}'"

    def test_four_char_кӏуа_all_i_variants(self, utils):
        """All I-like variants of кӏуа should produce the same result qoá."""
        expected = 'qoá'
        # These should all normalize to the same thing
        variants = [
            'кӀуа',   # U+04C0 (uppercase palochka)
            'кIуа',   # Latin I
            'кiуа',   # Latin i
            'кӏуа',   # U+04CF (lowercase palochka)
        ]
        for variant in variants:
            result = utils.cyrillic_to_latin('н' + variant + 'н')
            middle = result[1:-1]
            assert middle == expected, f"Variant '{variant}' mid-word: expected '{expected}', got '{middle}' (full: {result})"


# ============================================================
# PREFIX MAPPINGS (word-initial rules)
# ============================================================

class TestPrefixOneChar:
    """Test 1-character prefix rules (word-initial only)."""

    def test_prefix_е_ye(self, utils):
        # Word-initial е → ye
        result = utils.cyrillic_to_latin('ежьы')
        assert result.startswith('ye')

    def test_prefix_и_yi(self, utils):
        # Word-initial и → yi
        result = utils.cyrillic_to_latin('ины')
        assert result.startswith('yi')

    def test_prefix_о_we(self, utils):
        # Word-initial о → we
        result = utils.cyrillic_to_latin('оны')
        assert result.startswith('we')

    def test_prefix_у_wı(self, utils):
        # Word-initial у before non-vowel → wı
        result = utils.cyrillic_to_latin('уны')
        assert result.startswith('wı')


class TestPrefixTwoChars:
    """Test 2-character prefix rules (word-initial only)."""

    def test_prefix_Ӏо_latin_I(self, utils):
        # Word-initial Iо (Latin I) → o (not 'o!)
        result = utils.cyrillic_to_latin('Iон')
        assert result == 'on'

    def test_prefix_Ӏа(self, utils):
        # Word-initial Ӏа → aá (has U+04C0 variant)
        result = utils.cyrillic_to_latin('Ӏан')
        assert result.startswith('aá')

    def test_prefix_ио(self, utils):
        result = utils.cyrillic_to_latin('ион')
        assert result.startswith('yiwe')

    def test_prefix_уу(self, utils):
        result = utils.cyrillic_to_latin('уун')
        assert result.startswith('wıw')

    def test_prefix_уэ(self, utils):
        result = utils.cyrillic_to_latin('уэн')
        assert result.startswith('we')

    def test_prefix_уа(self, utils):
        result = utils.cyrillic_to_latin('уахътэ')
        assert result.startswith('wa')

    def test_prefix_уе(self, utils):
        result = utils.cyrillic_to_latin('уен')
        assert result.startswith('wé')

    def test_prefix_уи(self, utils):
        result = utils.cyrillic_to_latin('уин')
        assert result.startswith('wi')


class TestPrefixThreeChars:
    """Test 3-character prefix rules (word-initial only)."""

    def test_prefix_иIэ(self, utils):
        # Word-initial иIэ → yie
        result = utils.cyrillic_to_latin('иIэн')
        assert result.startswith('yie')

    def test_prefix_Iае(self, utils):
        # Word-initial Iае → aye
        result = utils.cyrillic_to_latin('Iаен')
        assert result.startswith('aye')


# ============================================================
# CONTEXT-AWARE VOWEL RULES (single-char with prev-char context)
# ============================================================

class TestContextAwareVowelRules:
    """Test context-dependent vowel conversion in single-char handler."""

    def test_trailing_у_gets_apostrophe(self, utils):
        # Word-final у → u'
        result = utils.cyrillic_to_latin('ну')
        assert result == "nu'"

    @pytest.mark.parametrize("cyrillic_pair,expected", [
        ('оу', 'ow'),     # о→o, then у with prev оу → w
        ('еу', 'éw'),     # е→é, then у with prev еу → w
        ('ыу', 'ıwı'),    # ыу\S pattern → ıwı (3-char regex match)
        ('эу', 'ew'),     # э→e, then у with prev эу → w
    ])
    def test_vowel_у_becomes_w(self, utils, cyrillic_pair, expected):
        # Non-initial position, wrapped in consonants
        result = utils.cyrillic_to_latin('н' + cyrillic_pair + 'н')
        middle = result[1:-1]
        assert middle == expected, f"'{cyrillic_pair}': expected '{expected}', got '{middle}'"


# ============================================================
# CAPITALIZATION PRESERVATION
# ============================================================

class TestCapitalization:
    """Test that uppercase input is preserved in output."""

    def test_capitalized_word(self, utils):
        result = utils.cyrillic_to_latin('Нэ')
        assert result[0] == 'N'

    def test_all_uppercase_word(self, utils):
        result = utils.cyrillic_to_latin('НЭ')
        assert result == result.upper() or result == 'NE'

    def test_lowercase_word(self, utils):
        result = utils.cyrillic_to_latin('нэ')
        assert result == result.lower() or result[0].islower()


# ============================================================
# MULTI-WORD AND SENTENCE TESTS
# ============================================================

class TestMultiWord:
    """Test multi-word input (tokenization and spacing)."""

    def test_two_words(self, utils):
        result = utils.cyrillic_to_latin('нэ нэ')
        parts = result.split(' ')
        assert len(parts) == 2

    def test_preserves_spaces(self, utils):
        result = utils.cyrillic_to_latin('а б')
        assert ' ' in result

    def test_punctuation_prefix_paren(self, utils):
        result = utils.cyrillic_to_latin('(нэ)')
        assert result.startswith('(')

    def test_punctuation_prefix_dash(self, utils):
        result = utils.cyrillic_to_latin('-нэ')
        assert result.startswith('-')


# ============================================================
# I-VARIANT NORMALIZATION (all I-like characters should be equivalent)
# ============================================================

class TestIVariantNormalization:
    """Verify that all I-like characters produce the same conversion."""

    def test_кӀ_all_variants_produce_ć(self, utils):
        """All I-variants of кI should produce ć."""
        variants = [
            'кӀн',   # U+04C0
            'кIн',   # Latin I
            'кiн',   # Latin i
            'кӏн',   # U+04CF
        ]
        for v in variants:
            result = utils.cyrillic_to_latin(v)
            assert result.startswith('ć'), f"'{v}' should start with ć, got '{result}'"

    def test_тӀ_all_variants_produce_ṫ(self, utils):
        """All I-variants of тI should produce ṫ."""
        variants = ['тӀн', 'тIн', 'тiн', 'тӏн']
        for v in variants:
            result = utils.cyrillic_to_latin(v)
            assert result.startswith('ṫ'), f"'{v}' should start with ṫ, got '{result}'"


# ============================================================
# FULL WORD TESTS (from the fineweb corpus)
# These test current behavior as a regression baseline.
# After user review, correct_latin values will be verified.
# ============================================================

class TestCorpusWordsBaseline:
    """
    Baseline tests for corpus words.
    These capture CURRENT behavior (which may contain bugs).
    They will be updated after user reviews the generated CSV.
    """

    def test_simple_word_нэ(self, utils):
        assert utils.cyrillic_to_latin('нэ') == 'ne'

    def test_word_лъэхъаным(self, utils):
        result = utils.cyrillic_to_latin('лъэхъаным')
        assert result.startswith('ĺe')

    def test_word_шъхьафит(self, utils):
        result = utils.cyrillic_to_latin('шъхьафит')
        assert result == "şhafyit" or result.startswith('ş')  # baseline

    def test_word_гупшысэ(self, utils):
        result = utils.cyrillic_to_latin('гупшысэ')
        assert result.startswith('gu')

    def test_word_зэрагъэдэIуагъэр(self, utils):
        # Contains гъ, Ӏу, агъ
        result = utils.cyrillic_to_latin('зэрагъэдэIуагъэр')
        assert 'ğ' in result

    def test_word_начало_уахътэ(self, utils):
        # уахътэ is a common word starting with уа → wa prefix
        result = utils.cyrillic_to_latin('уахътэ')
        assert result.startswith('wa')

    def test_word_къещхы(self, utils):
        result = utils.cyrillic_to_latin('къещхы')
        assert result.startswith('k')

    def test_word_зэхъум(self, utils):
        result = utils.cyrillic_to_latin('зэхъум')
        assert 'ḣ' in result


# ============================================================
# EDGE CASES
# ============================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_none_input(self, utils):
        assert utils.cyrillic_to_latin(None) is None

    def test_empty_string(self, utils):
        assert utils.cyrillic_to_latin('') == ''

    def test_single_char_word(self, utils):
        # Single character should still work
        result = utils.cyrillic_to_latin('а')
        assert result == 'a'

    def test_non_cyrillic_passthrough(self, utils):
        # Non-Cyrillic characters should be passed through
        result = utils.cyrillic_to_latin('.')
        assert result == '.'

    def test_mixed_punctuation(self, utils):
        result = utils.cyrillic_to_latin('нэ.')
        assert result.endswith('.')

    def test_multiple_spaces(self, utils):
        result = utils.cyrillic_to_latin('нэ  нэ')
        assert '  ' in result


# ============================================================
# REGRESSION: KNOWN-GOOD WORDS
# These are words whose conversion is verified correct.
# Do NOT change these without linguistic review.
# ============================================================

class TestKnownGoodConversions:
    """
    Words whose Latin conversion has been verified as correct.
    These serve as regression guards — if any of these break,
    something went wrong with a fix.
    """

    @pytest.mark.parametrize("cyrillic,correct_latin", [
        # Simple consonant-vowel words
        ('нэ', 'ne'),
        ('мы', 'mı'),
        ('ба', 'ba'),
        # Words with digraph consonants
        ('гъэ', 'ğe'),
        ('къэ', 'ke'),
        ('хъу', 'ḣu'),
        # Word-initial prefix: е → ye
        ('ежь', 'yej'),
    ])
    def test_known_good(self, utils, cyrillic, correct_latin):
        assert utils.cyrillic_to_latin(cyrillic) == correct_latin


# ============================================================
# CORPUS REGRESSION TESTS
# Generated from fineweb_edu_ady_cyr_5401lines.txt corpus.
# These lock in current conversion output as a regression baseline.
# If a fix changes any of these, review the new output for correctness.
# ============================================================

def _load_corpus_test_data():
    """Load test data from corpus_test_data.csv."""
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..',
                            'corpus_test_data.csv')
    if not os.path.exists(csv_path):
        return []
    pairs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        header = f.readline()  # skip header
        for line in f:
            line = line.strip()
            if '|' in line:
                cyr, lat = line.split('|', 1)
                pairs.append((cyr, lat))
    return pairs


_CORPUS_DATA = _load_corpus_test_data()


class TestCorpusRegression:
    """
    Regression tests from the fineweb corpus (304 words).
    These capture current behavior. Review and update if a fix
    intentionally changes any output.
    """

    @pytest.mark.parametrize("cyrillic,expected_latin", _CORPUS_DATA,
                             ids=[p[0] for p in _CORPUS_DATA])
    def test_corpus_word(self, utils, cyrillic, expected_latin):
        assert utils.cyrillic_to_latin(cyrillic) == expected_latin

    def test_regression_corpus_lines_match_latin_golden(self, utils):
        tests_dir = Path(__file__).resolve().parent
        input_lines = read_lines(tests_dir / 'regression_texts_cyr.txt')
        expected_lines = read_lines(tests_dir / 'regression_texts_lat_golden.txt')
        converted_lines = [utils.cyrillic_to_latin(line) for line in input_lines]
        comparison = compare_lines_with_report(
            expected_lines=expected_lines,
            actual_lines=converted_lines,
            report_path=tests_dir / 'regression_reports' / 'cyrillic_to_latin_report.txt',
            title='Cyrillic to Latin regression comparison',
        )
        assert comparison.matches, comparison.fail_message()
