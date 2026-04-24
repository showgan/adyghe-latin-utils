# Known Limitations

This document lists known limitations of `adyghe-latin-utils`. They are not
bugs in the conversion code — they follow from the design of the official
Latin Adyghe alphabet itself, which does not provide distinct graphemes for a
small number of Cyrillic characters and digraphs. As a result, these
sequences cannot be recovered losslessly by a Cyrillic → Latin → Cyrillic
round-trip.

All limitations below are Cyrillic → Latin lossy collapses. Conversion in
either direction still runs without errors and still produces valid text in
the target script; the only effect is that re-converting the Latin output
back to Cyrillic may not reproduce the original Cyrillic string exactly.

## Characters that share a Latin grapheme

### `щ` collapses to `ш`

Both Cyrillic `щ` and `ш` map to Latin `ş`. The Latin alphabet has no
separate grapheme for `щ`, so Latin → Cyrillic always picks `ш` and any
`щ` in the original Cyrillic is lost on the round-trip.

```text
Cyrillic: Щамсэт       Latin: Şamset       Round-trip: Шамсэт
```

### Soft sign `ь` is dropped (except in `хь`)

The soft sign `ь` has no Latin grapheme. Cyrillic → Latin simply removes
it, so Latin → Cyrillic cannot know when to restore it. As a result
every `<consonant>ь` combination round-trips to the bare consonant. The
only exception is the digraph `хь` (→ Latin `h` → `хь`), which survives
the round-trip intact.

```text
Cyrillic: шӀэжьыгъ                 Latin: ş'ejığ                 Round-trip: шӀэжыгъ
Cyrillic: Реабилитировать          Latin: Réabilitirovat         Round-trip: Реабилитироват
Cyrillic: Терентьевичыр            Latin: Téréntéviçır           Round-trip: Терентевичыр
```

This affects the full family `бь`, `вь`, `гь`, `дь`, `жь`, `зь`, `кь`,
`ль`, `мь`, `нь`, `пь`, `рь`, `сь`, `ть`, `фь`, `ць`, `чь`, `шь`, `щь`
(and their capitalized counterparts). In practice most of these only
appear in Russian loanwords where the soft sign encodes palatalization
that Adyghe does not mark.

### `жъ`, `шъ`, `чъ` lose the hard sign

In the digraphs `жъ`, `шъ`, and `чъ`, the trailing hard sign `ъ` is not
represented in the Latin alphabet — these digraphs map to the same Latin
grapheme as the base letters `ж`, `ш`, `ч` respectively. Latin → Cyrillic
therefore produces the base letter without `ъ`.

```text
Cyrillic: тинэнэжъ      Latin: tinenej      Round-trip: тинэнэж
Cyrillic: ашъыу         Latin: aşıwı        Round-trip: ашыу
Cyrillic: пачъыхьэ      Latin: paçıhe       Round-trip: пачыхьэ
```

### `чӀ` collapses to `кӀ`

The trigraphs `чӀ` and `кӀ` (plus their capitalized forms `ЧӀ` / `КӀ`)
both map to Latin `ć`. Latin → Cyrillic always picks `кӀ`, so any `чӀ`
in the original Cyrillic is rewritten to `кӀ` on the round-trip.

```text
Cyrillic: ычIыпIэкIэ    Latin: ıćıṕeće      Round-trip: ыкӀыпӀэкӀэ
```

## Source-text normalization

### Latin `I` / `i` / `l` / `1` / `ı` / `İ` normalize to palochka `Ӏ`

Many Cyrillic Adyghe source texts type palochka as Latin `I` (or one of
`i`, `l`, `1`, `ı`, `İ`) because the proper Cyrillic `Ӏ` (U+04C0) is hard
to produce on common keyboards. `latin_to_cyrillic` maps all of these
stand-ins to `Ӏ`, so a Cyrillic → Latin → Cyrillic round-trip rewrites
any such stand-in in the original text to the canonical Cyrillic
palochka. This is not a regression: the round-trip output is the
correct canonical Cyrillic form.

```text
Cyrillic (source): СишIуагъэ    Latin: Sişü'ıağe    Round-trip: СишӀуагъэ
```

The round-trip regression tool in
[`tests/roundtrip_corpus.py`](tests/roundtrip_corpus.py) treats these
palochka-normalization diffs — together with the lossy Cyrillic
collapses above — as "known limitation" diffs under its
`--ignore-known-limitations` flag.

## Impact

- **Cyrillic → Latin:** produces correct, readable Latin output in the
  official alphabet. The ambiguity is inherent to the target script, not a
  bug in the converter.
- **Latin → Cyrillic:** produces the most likely Cyrillic form. For the
  cases above it picks `ш`, `ж`, `ш`, `ч`, `кӀ` respectively (and drops
  the soft sign outright), which is the correct default for the vast
  majority of words but will not recover the less common `щ` / `жъ` /
  `шъ` / `чъ` / `чӀ` forms nor any `<consonant>ь` combination other
  than `хь`.
- **Round-trip (Cyr → Lat → Cyr):** not lossless for any word containing
  the sequences above. This is a known limitation, not a regression.

If your use case requires lossless round-trip for these characters, you
need to keep the original Cyrillic text alongside the Latin version —
the Latin side alone cannot distinguish them.
