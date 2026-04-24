# adyghe-latin-utils

[![PyPI sürümü](https://img.shields.io/pypi/v/adyghe-latin-utils)](https://pypi.org/project/adyghe-latin-utils/)
[![Python](https://img.shields.io/pypi/pyversions/adyghe-latin-utils)](https://pypi.org/project/adyghe-latin-utils/)
[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🌐 [English](https://github.com/showgan/adyghe-latin-utils/blob/main/README.md) | **Türkçe** | [Русский](https://github.com/showgan/adyghe-latin-utils/blob/main/README.ru.md) | [עברית](https://github.com/showgan/adyghe-latin-utils/blob/main/README.he.md)

**Adıge** (Batı Çerkes) dili için Python yardımcı araçları — **Kiril↔Latin alfabe dönüşümü** ve **sayıdan kelimeye dönüşüm**.

## Adıgece Hakkında

[Adıgece](https://tr.wikipedia.org/wiki/Ad%C4%B1gece) (адыгабзэ / adıǵabze), yaklaşık 600.000 kişi tarafından konuşulan bir Kuzeybatı Kafkas dilidir. Başlıca Adıgey Cumhuriyeti (Rusya), Türkiye, Ürdün, Suriye ve dünya genelindeki diaspora toplulukları arasında konuşulmaktadır. ISO 639-3 dil kodu **ady**'dir.

Adıgece geleneksel olarak Kiril alfabesiyle yazılmaktadır (1938'den beri). Latin tabanlı bir Adıge alfabesi de resmi yazı sistemi olarak mevcuttur. Bu paket, bu iki resmi alfabe arasında dönüşüm yapma ve sayıları Adıgece kelimelere çevirme araçları sağlar.

## Özellikler

- **Kiril → Latin dönüşümü** — bağlama duyarlı dönüşüm: bileşik karakterler (гу, гъ, дж, дз, жь, кӀ, ку, шъ vb.) doğru şekilde işlenir
- **Latin → Kiril dönüşümü** — ünlü ekleme ve palochka (Ӏ) kurallarıyla ters dönüşüm
- **Sayıdan kelimeye** — tam sayıları (0 ile 10¹⁵ arası) **modern onluk (10 tabanlı) sistemle** Adıgece kelimelere dönüştürür
- **Metin içindeki sayılar** — karışık metinlerdeki 12 farklı sayısal deseni algılar ve dönüştürür:
  telefon numaraları, para birimleri ($), yüzdeler (%), aralıklar (7-12), ondalıklar (5.11),
  Roma rakamları (IV), işaretli sayılar (+14, -32) ve daha fazlası
- **Büyük/küçük harf araçları** — özel Latin karakterleri (İ/ı) ve Kiril palochka (Ӏ) doğru şekilde işlenerek büyük/küçük harf ve baş harf dönüşümü
- **Alfabe algılama** — metnin Kiril Adıgecesiyle yazılıp yazılmadığını algılar
- **CLI araçları** — çoklu işlemci desteğiyle toplu dosya dönüştürme için komut satırı araçları

## Kurulum

```bash
pip install adyghe-latin-utils
```

Veya [uv](https://docs.astral.sh/uv/) ile:

```bash
uv add adyghe-latin-utils
```

## Hızlı Başlangıç

### Alfabe Dönüşümü

```python
from adyghe_latin_utils import AdigaCharacterUtils

utils = AdigaCharacterUtils()

# Kiril'den Latin'e
utils.cyrillic_to_latin("гупшысэ")        # → "ǵupşıśé"
utils.cyrillic_to_latin("лъэхъаным")      # → "ĺéḣáním"
utils.cyrillic_to_latin("къещхы")          # → "kéşḣı"

# Latin'den Kiril'e
utils.latin_to_cyrillic("selam")           # → "сэлам"
utils.latin_to_cyrillic("adıǵe")          # → "адыгэ"

# Alfabe algılama
utils.is_cyrillic_adyghe("гупшысэ")       # → True
utils.is_cyrillic_adyghe("ǵupşıśé")      # → False
```

### Sayıdan Kelimeye

Bu kütüphane, sayıdan kelimeye dönüşüm için **modern onluk (10 tabanlı) sistemi** kullanır.
Adıgece geleneksel olarak Fransızcaya benzer bir **yirmili (20 tabanlı)** sayı sistemi kullanır
(örneğin, "72" için Fransızca *soixante-douze* = 60 + 12). Geleneksel Adıge sisteminde
"72", *ṫoćişıre ṫure* (yaklaşık olarak "üç-yirmi-ve-on-iki") şeklinde söylenir. Modern kullanım
daha basit bir **onluk (10 tabanlı)** sisteme yönelmiştir:

| Sayı | Modern onluk (bu kütüphane)   | Geleneksel yirmili (desteklenmiyor)   |
|------|-------------------------------|---------------------------------------|
| 72   | blıć ṫu (7-on ve 2)          | ṫoćişıre ṫure (3×20 + 12)            |

```python
from adyghe_latin_utils import AdigaNumberUtils

AdigaNumberUtils.number_to_words(5)        # → "tfı"
AdigaNumberUtils.number_to_words(42)       # → "pĺ'ıć ṫu"
AdigaNumberUtils.number_to_words(100)      # → "şe"
AdigaNumberUtils.number_to_words(1000)     # → "min"
AdigaNumberUtils.number_to_words(2025)     # → "ṫu min ṫuć tfı"
```

### Metin İçindeki Sayılar

```python
from adyghe_latin_utils import AdigaNumberUtils

AdigaNumberUtils.convert_numbers_in_text("bölüm 3")
# → "bölüm şı"

AdigaNumberUtils.convert_numbers_in_text("ajan 007")
# → "ajan ziy ziy blı"

AdigaNumberUtils.convert_numbers_in_text("yıl 2025")
# → "yıl ṫu min ṫuć tfı"
```

### Büyük/Küçük Harf Araçları

```python
from adyghe_latin_utils import AdigaCharacterUtils

utils = AdigaCharacterUtils()

# Latin metin
utils.to_lowercase("ADIGE", is_latin=True, is_cyrillic=False)
utils.to_uppercase("adıǵe", is_latin=True, is_cyrillic=False)
utils.capitalize("adıǵe", is_latin=True, is_cyrillic=False)

# Özel Latin karakterlerini temel İngilizce karakterlere dönüştürme
utils.special_chars_to_english_chars("ǵupşıśé")  # → "gupsise"
```

## CLI Kullanımı

Paketle birlikte iki komut satırı aracı yüklenir:

### Alfabe Dönüşümü

```bash
# Kiril'den Latin'e (dosyadan dosyaya)
adyghe-char-convert -i girdi.txt -o cikti.txt -d c2l

# Latin'den Kiril'e (dosyadan standart çıktıya)
adyghe-char-convert -i girdi.txt -d l2c

# Komut satırında doğrudan bir dize dönüştürme
adyghe-char-convert -t "гупшысэ" -d c2l

# Seçenekler:
#   -t, --text       Girdi metin dizesi (-i ile birlikte kullanılamaz)
#   -i, --input      Girdi dosyası yolu (-t ile birlikte kullanılamaz)
#   -o, --output     Çıktı dosyası yolu (varsayılan: stdout)
#   -d, --direction  c2l (Kiril→Latin) veya l2c (Latin→Kiril) (zorunlu)
```

Alfabe dönüşümü CLI'si büyük dosyalar için **çoklu işlemci** desteği sunar ve ilerleme çubuğu gösterir.

### Sayı Dönüşümü

```bash
# Metin dizesindeki sayıları dönüştürme
adyghe-num-convert -t "bölüm 3"

# Dosyadaki sayıları dönüştürme
adyghe-num-convert -i girdi.txt -o cikti.txt

# Seçenekler:
#   -t, --text    Girdi metin dizesi (-i ile birlikte kullanılamaz)
#   -i, --input   Girdi dosyası yolu (-t ile birlikte kullanılamaz)
#   -o, --output  Çıktı dosyası yolu (varsayılan: stdout)
```

## API Referansı

### `AdigaCharacterUtils`

| Metot | Açıklama |
|-------|----------|
| `cyrillic_to_latin(text: str) -> str` | Kiril Adıge metnini Latin alfabesine dönüştürür |
| `latin_to_cyrillic(text: str) -> str` | Latin Adıge metnini Kiril alfabesine dönüştürür |
| `is_cyrillic_adyghe(text: str, threshold: float = 0.5) -> bool` | Metnin Kiril Adıgecesi olup olmadığını algılar |
| `to_lowercase(text, is_latin, is_cyrillic) -> str` | Alfabeye duyarlı küçük harf dönüşümü |
| `to_uppercase(text, is_latin, is_cyrillic) -> str` | Alfabeye duyarlı büyük harf dönüşümü |
| `capitalize(text, is_latin, is_cyrillic) -> str` | İlk karakteri büyük harfe dönüştürür |
| `special_chars_to_english_chars(text: str) -> str` | Aksan işaretli Latin karakterlerini ASCII'ye dönüştürür |
| `cyrillic_extra_chars_to_basic_chars(text: str) -> str` | Kiril karakter varyantlarını normalleştirir |
| `sanitize_latin_text(text: str) -> str` | Latin Adıge alfabesi dışındaki karakterleri kaldırır, boşlukları sadeleştirir ve gereksiz noktalamayı normalleştirir |

### `AdigaNumberUtils`

| Metot | Açıklama |
|-------|----------|
| `number_to_words(number: int) -> str` | Tam sayıyı (0–10¹⁵) Adıgece kelimelere dönüştürür |
| `convert_numbers_in_text(text: str) -> str` | Metindeki tüm sayısal desenleri bulur ve dönüştürür |

## Desteklenen Sayısal Desenler

`convert_numbers_in_text()` aşağıdaki desenleri tanır ve dönüştürür:

| Desen | Örnek | Açıklama |
|-------|-------|----------|
| Uluslararası telefon | `+972-58-206-2315` | Rakamlar tek tek okunur |
| Yerel telefon | `058-206-2315` | Rakamlar tek tek okunur |
| Ön ek-tire | `ya-20` | Sayı dönüştürülür, ön ek korunur |
| Son ek-tire | `13-re` | Sayı dönüştürülür, son ek korunur |
| Dolar tutarı | `$16,918` | Tam sayı dönüşümü |
| İşaretli sayı | `+14`, `-32` | İşaret korunur, sayı dönüştürülür |
| Aralık | `1042-1814` | Her sayı ayrı ayrı dönüştürülür |
| Ondalık | `5.11`, `50.06%` | Tam ve kesirli kısımlar dönüştürülür |
| Eğik çizgiyle ayrılmış | `2010/11` | Her kısım dönüştürülür |
| Sembol son eki | `4%`, `804+` | Sayı dönüştürülür, sembol korunur |
| Roma rakamı | `III`, `IV` | Arap rakamına, ardından kelimeye dönüştürülür |
| Düz sayı | `42`, `1,000,000` | Tam sayı dönüşümü |

## Kararlılık

Bu proje [Semantik Sürümleme](https://semver.org/spec/v2.0.0.html) kurallarını
takip eder. `1.0.0` sürümünden itibaren aşağıdakiler genel, kararlı API olarak
kabul edilir:

- `adyghe_latin_utils` paketinden yeniden dışa aktarılan `AdigaCharacterUtils`
  ve `AdigaNumberUtils` sınıfları
  ([`src/adyghe_latin_utils/__init__.py`](src/adyghe_latin_utils/__init__.py)
  içindeki `__all__` listesine bakın).
- `adyghe-char-convert` ve `adyghe-num-convert` komut satırı araçları ile
  belgelenen bayrakları.

Yukarıdakilerde yapılacak geriye dönük uyumsuz değişiklikler ana sürüm artışı
gerektirir. Burada listelenmeyen her şey (dahili modüller, yardımcı
fonksiyonlar, `_` ile başlayan özel öznitelikler ve daha önce ele alınmamış
sınır durumlarında tam dönüşüm çıktısı) dahili kabul edilir ve ikincil (minor)
veya yama (patch) sürümlerinde değişebilir. Kiril ve Latin alfabeleri
arasındaki bilinen kayıplı dönüşümler
[`LIMITATIONS.md`](LIMITATIONS.md) dosyasında belgelenmiştir.

## Geliştirme

```bash
# Depoyu klonlayın
git clone https://github.com/showgan/adyghe-latin-utils.git
cd adyghe-latin-utils

# Sanal ortam oluşturun ve etkinleştirin
uv venv
source .venv/bin/activate        # bash/zsh
# source .venv/bin/activate.csh  # tcsh

# Paketi düzenlenebilir modda ve geliştirme bağımlılıklarıyla kurun
uv pip install -e ".[dev]"

# Testleri çalıştırın
pytest tests/ -v
```

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır — ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.
