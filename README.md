# adyghe-latin-utils

[![PyPI version](https://img.shields.io/pypi/v/adyghe-latin-utils)](https://pypi.org/project/adyghe-latin-utils/)
[![Python](https://img.shields.io/pypi/pyversions/adyghe-latin-utils)](https://pypi.org/project/adyghe-latin-utils/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python utilities for the **Adyghe** (Western Circassian) language — **Cyrillic↔Latin alphabet conversion** and **number-to-words conversion**.

## About Adyghe

[Adyghe](https://en.wikipedia.org/wiki/Adyghe_language) (адыгабзэ / adıǵabze) is a Northwest Caucasian language spoken by approximately 600,000 people, primarily in the Republic of Adygea (Russia), Turkey, Jordan, Syria, and diaspora communities worldwide. Its ISO 639-3 language code is **ady**.

Adyghe is traditionally written in the Cyrillic script (since 1938). A Latin-based Adyghe alphabet also exists as an official writing system. This package provides tools for converting between these two official alphabets, as well as converting numbers into Adyghe words.

## Features

- **Cyrillic → Latin conversion** — context-aware conversion between the official Cyrillic and Latin Adyghe alphabets, handling compound characters (гу, гъ, дж, дз, жь, кӀ, ку, шъ, etc.)
- **Latin → Cyrillic conversion** — reverse conversion with vowel insertion and palochka (Ӏ) rules
- **Number to words** — converts integers (0 to 10¹⁵) into Adyghe words
- **Numbers in text** — detects and converts 12 types of numeric patterns in mixed text:
  phone numbers, currencies ($), percentages (%), ranges (7-12), decimals (5.11),
  Roman numerals (IV), signed numbers (+14, -32), and more
- **Case utilities** — uppercase, lowercase, and capitalize with proper handling of
  special Latin characters (İ/ı) and Cyrillic palochka (Ӏ)
- **Script detection** — detect whether text is written in Cyrillic Adyghe
- **CLI tools** — command-line utilities for batch file conversion with multiprocessing support

## Installation

```bash
pip install adyghe-latin-utils
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add adyghe-latin-utils
```

## Quick Start

### Alphabet Conversion

```python
from adyghe_latin_utils import AdigaCharacterUtils

utils = AdigaCharacterUtils()

# Cyrillic to Latin
utils.cyrillic_to_latin("гупшысэ")        # → "ǵupşıśé"
utils.cyrillic_to_latin("лъэхъаным")      # → "ĺéḣáním"
utils.cyrillic_to_latin("къещхы")          # → "kéşḣı"

# Latin to Cyrillic
utils.latin_to_cyrillic("selam")           # → "сэлам"
utils.latin_to_cyrillic("adıǵe")          # → "адыгэ"

# Script detection
utils.is_cyrillic_adyghe("гупшысэ")       # → True
utils.is_cyrillic_adyghe("ǵupşıśé")      # → False
```

### Number to Words

```python
from adyghe_latin_utils import AdigaNumberUtils

AdigaNumberUtils.number_to_words(5)        # → "tfı"
AdigaNumberUtils.number_to_words(42)       # → "pĺ'ıć ṫu"
AdigaNumberUtils.number_to_words(100)      # → "şe"
AdigaNumberUtils.number_to_words(1000)     # → "min"
AdigaNumberUtils.number_to_words(2025)     # → "ṫu min ṫuć tfı"
```

### Numbers in Mixed Text

```python
from adyghe_latin_utils import AdigaNumberUtils

AdigaNumberUtils.convert_numbers_in_text("chapter 3")
# → "chapter şı"

AdigaNumberUtils.convert_numbers_in_text("agent 007")
# → "agent ziy ziy blı"

AdigaNumberUtils.convert_numbers_in_text("the year 2025")
# → "the year ṫu min ṫuć tfı"
```

### Case Utilities

```python
from adyghe_latin_utils import AdigaCharacterUtils

utils = AdigaCharacterUtils()

# Latin text
utils.to_lowercase("ADIGE", is_latin=True, is_cyrillic=False)
utils.to_uppercase("adıǵe", is_latin=True, is_cyrillic=False)
utils.capitalize("adıǵe", is_latin=True, is_cyrillic=False)

# Simplify special Latin chars to basic English
utils.special_chars_to_english_chars("ǵupşıśé")  # → "gupsise"
```

## CLI Usage

Two command-line tools are installed with the package:

### Script Conversion

```bash
# Cyrillic to Latin (file to file)
adyghe-char-convert -i input.txt -o output.txt -d c2l

# Latin to Cyrillic (file to stdout)
adyghe-char-convert -i input.txt -d l2c

# Options:
#   -i, --input      Path to input text file (required)
#   -o, --output     Path to output file (default: stdout)
#   -d, --direction  c2l (Cyrillic→Latin) or l2c (Latin→Cyrillic) (required)
```

The script conversion CLI supports **multiprocessing** for large files and displays a progress bar.

### Number Conversion

```bash
# Convert numbers in a text string
adyghe-num-convert -t "chapter 3"

# Convert numbers in a file
adyghe-num-convert -i input.txt -o output.txt

# Options:
#   -t, --text    Input text string (mutually exclusive with -i)
#   -i, --input   Path to input text file (mutually exclusive with -t)
#   -o, --output  Path to output file (default: stdout)
```

## API Reference

### `AdigaCharacterUtils`

| Method | Description |
|--------|-------------|
| `cyrillic_to_latin(text: str) -> str` | Convert Cyrillic Adyghe text to Latin script |
| `latin_to_cyrillic(text: str) -> str` | Convert Latin Adyghe text to Cyrillic script |
| `is_cyrillic_adyghe(text: str, threshold: float = 0.5) -> bool` | Detect if text is Cyrillic Adyghe |
| `to_lowercase(text, is_latin, is_cyrillic) -> str` | Lowercase with script-aware rules |
| `to_uppercase(text, is_latin, is_cyrillic) -> str` | Uppercase with script-aware rules |
| `capitalize(text, is_latin, is_cyrillic) -> str` | Capitalize first character |
| `special_chars_to_english_chars(text: str) -> str` | Simplify accented Latin chars to ASCII |
| `cyrillic_extra_chars_to_basic_chars(text: str) -> str` | Normalize Cyrillic character variants |

### `AdigaNumberUtils`

| Method | Description |
|--------|-------------|
| `number_to_words(number: int) -> str` | Convert integer (0–10¹⁵) to Adyghe words |
| `convert_numbers_in_text(text: str) -> str` | Find and convert all numeric patterns in text |

## Supported Numeric Patterns

`convert_numbers_in_text()` recognizes and converts these patterns:

| Pattern | Example | Description |
|---------|---------|-------------|
| International phone | `+972-58-206-2315` | Digits read individually |
| Local phone | `058-206-2315` | Digits read individually |
| Prefix-dash | `ya-20` | Number converted, prefix preserved |
| Postfix-dash | `13-re` | Number converted, postfix preserved |
| Dollar amount | `$16,918` | Full number conversion |
| Signed number | `+14`, `-32` | Sign preserved, number converted |
| Range | `1042-1814` | Each number converted separately |
| Decimal | `5.11`, `50.06%` | Integer and fractional parts converted |
| Slash-separated | `2010/11` | Each part converted |
| Symbol postfix | `4%`, `804+` | Number converted, symbol preserved |
| Roman numeral | `III`, `IV` | Converted to Arabic then to words |
| Plain number | `42`, `1,000,000` | Full number conversion |

## Development

```bash
# Clone the repository
git clone https://github.com/showgan/adyghe-latin-utils.git
cd adyghe-latin-utils

# Set up development environment
uv venv
uv pip install -e ".[dev]"

# Run tests
uv run pytest tests/ -v
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
