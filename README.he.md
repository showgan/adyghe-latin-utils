# adyghe-latin-utils

[![גרסת PyPI](https://img.shields.io/pypi/v/adyghe-latin-utils)](https://pypi.org/project/adyghe-latin-utils/)
[![Python](https://img.shields.io/pypi/pyversions/adyghe-latin-utils)](https://pypi.org/project/adyghe-latin-utils/)
[![רישיון: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🌐 [English](https://github.com/showgan/adyghe-latin-utils/blob/main/README.md) | [Türkçe](https://github.com/showgan/adyghe-latin-utils/blob/main/README.tr.md) | [Русский](https://github.com/showgan/adyghe-latin-utils/blob/main/README.ru.md) | **עברית**

כלי עזר ב-Python לשפה ה**אדיגית** (צ'רקסית מערבית) — **המרה בין אלפבית קירילי ולטיני** ו**המרת מספרים למילים**.

## אודות השפה האדיגית

[אדיגית](https://he.wikipedia.org/wiki/%D7%90%D7%93%D7%99%D7%92%D7%99%D7%AA) (адыгабзэ / adıǵabze) היא שפה צפון-קווקזית המדוברת על ידי כ-600,000 דוברים, בעיקר ברפובליקת אדיגיאה (רוסיה), טורקיה, ירדן, סוריה ובקהילות תפוצה ברחבי העולם. קוד השפה לפי ISO 639-3 הוא **ady**.

השפה האדיגית נכתבת באופן מסורתי בכתב קירילי (מאז 1938). קיים גם אלפבית אדיגי מבוסס לטינית כמערכת כתיבה רשמית. חבילה זו מספקת כלים להמרה בין שני האלפביתים הרשמיים הללו, ולהמרת מספרים למילים באדיגית.

## תכונות

- **המרה מקירילית ללטינית** — המרה מודעת הקשר בין האלפביתים הרשמיים הקיריליים והלטיניים של האדיגית, עם טיפול בתווים מורכבים (гу, гъ, дж, дз, жь, кӀ, ку, шъ וכו')
- **המרה מלטינית לקירילית** — המרה הפוכה עם כללי הוספת תנועות ופלוצ'קה (Ӏ)
- **מספרים למילים** — המרת מספרים שלמים (0 עד 10¹⁵) למילים באדיגית באמצעות **שיטת הספירה העשרונית (בסיס 10) המודרנית**
- **מספרים בטקסט** — זיהוי והמרת 12 סוגי דפוסי מספרים בטקסט מעורב:
  מספרי טלפון, מטבעות ($), אחוזים (%), טווחים (7-12), מספרים עשרוניים (5.11),
  ספרות רומיות (IV), מספרים עם סימן (+14,‏ -32) ועוד
- **כלי רישיות** — אותיות גדולות, קטנות ואות ראשונה גדולה עם טיפול נכון
  בתווים לטיניים מיוחדים (İ/ı) ופלוצ'קה קירילית (Ӏ)
- **זיהוי כתב** — זיהוי האם טקסט כתוב באדיגית קירילית
- **כלי שורת פקודה** — כלי CLI להמרת קבצים בצובר עם תמיכה בריבוי תהליכים

## התקנה

```bash
pip install adyghe-latin-utils
```

או באמצעות [uv](https://docs.astral.sh/uv/):

```bash
uv add adyghe-latin-utils
```

## התחלה מהירה

### המרת אלפבית

```python
from adyghe_latin_utils import AdigaCharacterUtils

utils = AdigaCharacterUtils()

# מקירילית ללטינית
utils.cyrillic_to_latin("гупшысэ")        # → "ǵupşıśé"
utils.cyrillic_to_latin("лъэхъаным")      # → "ĺéḣáním"
utils.cyrillic_to_latin("къещхы")          # → "kéşḣı"

# מלטינית לקירילית
utils.latin_to_cyrillic("selam")           # → "сэлам"
utils.latin_to_cyrillic("adıǵe")          # → "адыгэ"

# זיהוי כתב
utils.is_cyrillic_adyghe("гупшысэ")       # → True
utils.is_cyrillic_adyghe("ǵupşıśé")      # → False
```

### מספרים למילים

ספרייה זו משתמשת ב**שיטה העשרונית (בסיס 10) המודרנית** להמרת מספרים למילים.
באדיגית נהגו באופן מסורתי להשתמש ב**שיטה ויגסימלית (בסיס 20)** הדומה לצרפתית
(לדוגמה, בצרפתית *soixante-douze* = 60 + 12 עבור "72"). בשיטה האדיגית המסורתית,
"72" הוא *ṫoćişıre ṫure* (בערך "שלוש-עשרים-ושתים-עשרה"). השימוש המודרני
עבר ל**שיטה עשרונית (בסיס 10)** פשוטה יותר:

| מספר | עשרוני מודרני (ספרייה זו)      | ויגסימלי מסורתי (אינו נתמך)           |
|------|-------------------------------|---------------------------------------|
| 72   | blıć ṫu (7 עשרות ו-2)        | ṫoćişıre ṫure ‏(3×20 + 12)           |

```python
from adyghe_latin_utils import AdigaNumberUtils

AdigaNumberUtils.number_to_words(5)        # → "tfı"
AdigaNumberUtils.number_to_words(42)       # → "pĺ'ıć ṫu"
AdigaNumberUtils.number_to_words(100)      # → "şe"
AdigaNumberUtils.number_to_words(1000)     # → "min"
AdigaNumberUtils.number_to_words(2025)     # → "ṫu min ṫuć tfı"
```

### מספרים בטקסט מעורב

```python
from adyghe_latin_utils import AdigaNumberUtils

AdigaNumberUtils.convert_numbers_in_text("chapter 3")
# → "chapter şı"

AdigaNumberUtils.convert_numbers_in_text("agent 007")
# → "agent ziy ziy blı"

AdigaNumberUtils.convert_numbers_in_text("the year 2025")
# → "the year ṫu min ṫuć tfı"
```

### כלי רישיות

```python
from adyghe_latin_utils import AdigaCharacterUtils

utils = AdigaCharacterUtils()

# טקסט לטיני
utils.to_lowercase("ADIGE", is_latin=True, is_cyrillic=False)
utils.to_uppercase("adıǵe", is_latin=True, is_cyrillic=False)
utils.capitalize("adıǵe", is_latin=True, is_cyrillic=False)

# פישוט תווים לטיניים מיוחדים לתווי אנגלית בסיסיים
utils.special_chars_to_english_chars("ǵupşıśé")  # → "gupsise"
```

## שימוש ב-CLI

עם החבילה מותקנים שני כלי שורת פקודה:

### המרת אלפבית

```bash
# מקירילית ללטינית (קובץ לקובץ)
adyghe-char-convert -i input.txt -o output.txt -d c2l

# מלטינית לקירילית (קובץ ל-stdout)
adyghe-char-convert -i input.txt -d l2c

# המרת מחרוזת שמועברת ישירות בשורת הפקודה
adyghe-char-convert -t "гупшысэ" -d c2l

# אפשרויות:
#   -t, --text       מחרוזת טקסט קלט (לא ניתן לשלב עם i-)
#   -i, --input      נתיב לקובץ קלט (לא ניתן לשלב עם t-)
#   -o, --output     נתיב לקובץ פלט (ברירת מחדל: stdout)
#   -d, --direction  c2l (קירילית→לטינית) או l2c (לטינית→קירילית) (חובה)
```

CLI המרת האלפבית תומך ב**ריבוי תהליכים** לקבצים גדולים ומציג סרגל התקדמות.

### המרת מספרים

```bash
# המרת מספרים במחרוזת טקסט
adyghe-num-convert -t "chapter 3"

# המרת מספרים בקובץ
adyghe-num-convert -i input.txt -o output.txt

# אפשרויות:
#   -t, --text    מחרוזת טקסט קלט (לא ניתן לשלב עם i-)
#   -i, --input   נתיב לקובץ קלט (לא ניתן לשלב עם t-)
#   -o, --output  נתיב לקובץ פלט (ברירת מחדל: stdout)
```

## מדריך API

### `AdigaCharacterUtils`

| מתודה | תיאור |
|-------|-------|
| `cyrillic_to_latin(text: str) -> str` | המרת טקסט אדיגי קירילי ללטינית |
| `latin_to_cyrillic(text: str) -> str` | המרת טקסט אדיגי לטיני לקירילית |
| `is_cyrillic_adyghe(text: str, threshold: float = 0.5) -> bool` | זיהוי אם הטקסט הוא אדיגית קירילית |
| `to_lowercase(text, is_latin, is_cyrillic) -> str` | אותיות קטנות עם מודעות לכתב |
| `to_uppercase(text, is_latin, is_cyrillic) -> str` | אותיות גדולות עם מודעות לכתב |
| `capitalize(text, is_latin, is_cyrillic) -> str` | אות ראשונה גדולה |
| `special_chars_to_english_chars(text: str) -> str` | פישוט תווים לטיניים מנוקדים ל-ASCII |
| `cyrillic_extra_chars_to_basic_chars(text: str) -> str` | נרמול גרסאות תווים קיריליים |
| `sanitize_latin_text(text: str) -> str` | הסרת תווים שאינם באלפבית האדיגי הלטיני, כיווץ רווחים ונרמול סימני פיסוק חריגים |

### `AdigaNumberUtils`

| מתודה | תיאור |
|-------|-------|
| `number_to_words(number: int) -> str` | המרת מספר שלם (0–10¹⁵) למילים באדיגית |
| `convert_numbers_in_text(text: str) -> str` | איתור והמרת כל דפוסי המספרים בטקסט |

## דפוסי מספרים נתמכים

`()convert_numbers_in_text` מזהה וממיר את הדפוסים הבאים:

| דפוס | דוגמה | תיאור |
|------|-------|-------|
| טלפון בינלאומי | `+972-58-206-2315` | ספרות נקראות בנפרד |
| טלפון מקומי | `058-206-2315` | ספרות נקראות בנפרד |
| תחילית-מקף | `ya-20` | המספר מומר, התחילית נשמרת |
| סיומת-מקף | `13-re` | המספר מומר, הסיומת נשמרת |
| סכום בדולרים | `$16,918` | המרת מספר מלאה |
| מספר עם סימן | `+14`, `-32` | הסימן נשמר, המספר מומר |
| טווח | `1042-1814` | כל מספר מומר בנפרד |
| עשרוני | `5.11`, `50.06%` | חלק שלם ושברי מומרים |
| מופרד בלוכסן | `2010/11` | כל חלק מומר |
| סמל-סיומת | `4%`, `804+` | המספר מומר, הסמל נשמר |
| ספרה רומית | `III`, `IV` | מומר לערבי ואז למילים |
| מספר רגיל | `42`, `1,000,000` | המרת מספר מלאה |

## יציבות

פרויקט זה פועל לפי [ניהול גרסאות סמנטי](https://semver.org/spec/v2.0.0.html).
החל מגרסה `1.0.0`, המרכיבים הבאים נחשבים ל-API הציבורי והיציב:

- המחלקות `AdigaCharacterUtils` ו-`AdigaNumberUtils` המיוצאות מחדש מהחבילה
  `adyghe_latin_utils` (ראו `__all__` בקובץ
  [`src/adyghe_latin_utils/__init__.py`](src/adyghe_latin_utils/__init__.py)).
- כלי שורת הפקודה `adyghe-char-convert` ו-`adyghe-num-convert` והדגלים המתועדים
  שלהם.

שינויים שוברי-תאימות בכל אחד מהפריטים שלמעלה ידרשו העלאת גרסה ראשית (major).
כל דבר שאינו מופיע כאן (מודולים פנימיים, פונקציות עזר, תכונות פרטיות עם קידומת
`_` ופלט ההמרה המדויק במקרי קצה שלא טופלו בעבר) נחשב פנימי ועשוי להשתנות
בגרסת משנה (minor) או בגרסת טלאי (patch). המרות עם אובדן מידע ידועות בין
האלפביתים הקירילי והלטיני מתועדות בקובץ [`LIMITATIONS.md`](LIMITATIONS.md).

## פיתוח

```bash
# שכפול המאגר
git clone https://github.com/showgan/adyghe-latin-utils.git
cd adyghe-latin-utils

# יצירה והפעלה של סביבה וירטואלית
uv venv
source .venv/bin/activate        # bash/zsh
# source .venv/bin/activate.csh  # tcsh

# התקנת החבילה במצב עריכה עם תלויות פיתוח
uv pip install -e ".[dev]"

# הרצת בדיקות
pytest tests/ -v
```

## רישיון

פרויקט זה מורשה תחת רישיון MIT — ראו את קובץ [LICENSE](LICENSE) לפרטים.
