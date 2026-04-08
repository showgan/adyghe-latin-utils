# AdigaNumberUtils

Converts numbers (digits) to words in the Adyghe language using the Latin Adyghe alphabet.

## Location

`src/adyghe_latin_utils/number_utils.py`

## Overview

`AdigaNumberUtils` parses numbers in text and replaces them with their Adyghe word equivalents. The algorithm is ported from the Android app [AdigaNumbers](https://github.com/user/AdigaNumbers) (`MainActivity.java`).

## Digit-to-Word Mapping

| Digit | Adyghe Word |
|-------|-------------|
| 0     | ziy         |
| 1     | zı          |
| 2     | ṫu          |
| 3     | şı          |
| 4     | pĺ'ı        |
| 5     | tfı         |
| 6     | xı          |
| 7     | blı         |
| 8     | yi          |
| 9     | bğu         |

### Tens

Formed by appending **ć** to the digit word: `zıć` (10), `ṫuć` (20), `şıć` (30), etc.

### Hundreds

- 100 = `şe`
- 200 = `ṫu şe`, 300 = `şı şe`, ..., 900 = `bğu şe`

### Scale Words (Triplet Groups)

| Scale          | Adyghe Word |
|----------------|-------------|
| Thousands      | min         |
| Millions       | milyon      |
| Billions       | milyard     |
| Trillions      | trilyon     |

Numbers ≥ 10¹⁵ produce the overflow text: **trilyonım yeḣu'**

## Public Methods

### `number_to_words(number: int) -> str`

Converts a non-negative integer to Adyghe words.

```python
AdigaNumberUtils.number_to_words(0)        # "ziy"
AdigaNumberUtils.number_to_words(1)        # "zı"
AdigaNumberUtils.number_to_words(10)       # "zıć"
AdigaNumberUtils.number_to_words(100)      # "şe"
AdigaNumberUtils.number_to_words(1000)     # "min"
AdigaNumberUtils.number_to_words(1983)     # "min bğu şe yić şı"
AdigaNumberUtils.number_to_words(2025)     # "ṫu min ṫuć tfı"
AdigaNumberUtils.number_to_words(1000000)  # "milyon"
```

**Rules:**
- Leading `zı` is stripped for scale-prefixed numbers (1000 → `min`, not `zı min`).
- Zero triplets in the middle are skipped (1,000,001 → `milyon zı`).
- Returns `"trilyonım yeḣu'"` for numbers ≥ 1,000,000,000,000,000.

### `convert_numbers_in_text(text: str) -> str`

Finds all numbers in a text string and replaces them with Adyghe words. Supports many number formats for TTS (text-to-speech) use.

```python
AdigaNumberUtils.convert_numbers_in_text("the year was 1,983 when I started high school")
# "the year was min bğu şe yić şı when I started high school"

AdigaNumberUtils.convert_numbers_in_text("agent 007")
# "agent ziy ziy blı"

AdigaNumberUtils.convert_numbers_in_text("population is 1,000,000")
# "population is milyon"
```

**Supported number formats:**

| Format | Example | Output |
|--------|---------|--------|
| Plain integers | `42` | `pĺ'ıć ṫu` |
| Comma-separated | `1,983` | `min bğu şe yić şı` |
| Postfix with dash | `13-re` | `zıć şıre` |
| Postfix with dash (vowel insertion) | `50,000-m` | `tfıć minım` |
| Multi-segment postfix | `1-2-će` | `zı ṫuće` |
| Slash+postfix | `2010/11-m` | `ṫu min zıć zıć zım` |
| Symbol postfix `+` | `804+` | `yi şe pĺ'ı xaḣo` |
| Symbol postfix `-` | `65-` | `xıć tfı xećı` |
| Symbol postfix `%` | `4%` | `pĺ'ı pérsént` |
| Prefix with dash | `ya-20` | `yaṫuć` |
| Sign prefix `+` | `+14` | `positif zıć pĺ'ı` |
| Sign prefix `-` | `-32` | `négatif şıć ṫu` |
| Dollar prefix `$` | `$16,918` | `zıć xı min bğu şe zıć yi dolar` |
| Decimal number | `5.11` | `tfı fı zıć zı` |
| Decimal with sign | `+5.1` | `positif tfı fı zı` |
| Decimal with percent | `50.06%` | `tfıć fı ziy xı pérsént` |
| Multi-dot number | `28.57.23` | `ṫuć yi fı tfıć blı fı ṫuć şı` |
| Number range | `1042-1814` | `min pĺ'ıć ṫu min yi şe zıć pĺ'ı` |
| Range with symbol | `7-12+` | `blı zıć ṫu xaḣo` |
| Slash-separated | `2010/11` | `ṫu min zıć zıć zı` |
| Phone (international) | `+972-58-206-2315` | `positif bğu blı ṫu tfı yi ṫu ziy xı ṫu şı zı tfı` |
| Phone (local) | `058-206-2315` | `ziy tfı yi ṫu ziy xı ṫu şı zı tfı` |
| Roman numeral | `IV` | `pĺ'ı` |
| Roman with dot | `III.` | `şı` |

#### Postfix Rules

- **Dash postfix:** The postfix text is appended to the last converted word. If the last character is a consonant, `ı` is inserted before the postfix (e.g., `min` + `m` → `minım`).
- **Symbol postfix:** `+` → `xaḣo`, `-` → `xećı`, `%` → `pérsént` (appended as separate words with a space).

#### Prefix Rules

- **Dash prefix:** The prefix text is prepended to the first converted word without a space.
- **Sign prefix:** `+` → `positif`, `-` → `négatif` (prepended as separate words with a space).
- **Dollar prefix:** `$` → `dolar` (appended at the end of the converted number).

#### Decimal Numbers

Split at the decimal point; the word `fı` (meaning "dot/period") is inserted between the segments. Each segment is converted as a number (with leading-zero handling for the fractional part).

#### Phone Numbers

All digits are converted individually (digit by digit). International numbers starting with `+` get `positif` prepended.

#### Roman Numerals

Standard Roman numerals (I–M) with subtractive notation (IV=4, IX=9, etc.). Single-character Roman numerals require a trailing dot to avoid ambiguity with English text.

### Leading Zeros

Numbers with leading zeros are handled specially — each leading zero becomes `ziy`, then the remaining digits are converted normally:

- `"0"` → `ziy`
- `"007"` → `ziy ziy blı`
- `"00"` → `ziy ziy`

## Algorithm

1. **Divide** the number into groups of 3 digits (triplets) from right to left.
2. **Convert each triplet** independently:
   - Ones digit → digit word
   - Tens digit → digit word + `ć`
   - Hundreds digit → `şe` (for 1) or digit word + ` şe` (for 2–9)
   - Combine: hundreds + tens + ones with spaces
3. **Append scale words** (`min`, `milyon`, `milyard`, `trilyon`) to each non-zero triplet based on its position.
4. **Strip leading `zı `** from the final result (so `zı min` becomes `min`).

## Tests

Test suite: `tests/test_adiga_number_utils.py` (147 tests)

Test classes:
- `TestSingleDigits` — digits 0–9
- `TestTens` — 10–99
- `TestHundreds` — 100–999
- `TestThousands` — 1,000–999,999
- `TestLargeNumbers` — millions, billions, trillions
- `TestOverflow` — numbers ≥ 10¹⁵
- `TestLeadingZeros` — numbers with leading zeros
- `TestZeroTriplets` — numbers with zero triplets in the middle
- `TestConvertNumbersInText` — in-text number replacement
- `TestEdgeCases` — empty strings, None, whitespace
- `TestPostfixDash` — postfix with dash (vowel insertion)
- `TestPostfixSymbols` — symbol postfix (+, -, %)
- `TestPrefixDash` — prefix with dash
- `TestPrefixSymbols` — sign/dollar prefix (+, -, $)
- `TestDecimalNumbers` — decimal numbers with sign
- `TestMultiDotNumbers` — multi-dot numbers
- `TestDecimalPercent` — decimal with percent
- `TestRanges` — number ranges with optional symbol
- `TestSlashSeparated` — slash-separated numbers
- `TestPhoneNumbers` — international and local phone numbers
- `TestRomanNumerals` — Roman numerals with/without dot
- `TestVowelInsertion` — `_append_postfix` vowel insertion logic

Run tests:
```bash
uv run pytest tests/test_adiga_number_utils.py -v
```
