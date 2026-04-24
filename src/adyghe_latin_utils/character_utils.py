import argparse
import multiprocessing
import os
import re
import sys
import time


class AdigaCharacterUtils:
    RECOGNIZED_LATIN_CHARS_PATTERN = re.compile(r"[^a-záçćéǵğḣıḱĺöṕşśšṫüź\',.;:\?\! ]")

    def __init__(self):
        # Cyrillic Allowed Chars:
        self._cyrillic_allowed = "АБВГДЕЖЗИЙКЛМНОӀПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя?,.;:-()[]{}_\"'`"

        # Latin Special to English simplification:
        self._special_to_english = {
            'á': 'a',
            'ç': 'c',
            'ć': 'c',
            'é': 'e',
            'ǵ': 'g',
            'ğ': 'g',
            'ḣ': 'h',
            'ı': 'i',
            'ḱ': 'k',
            'ĺ': 'l',
            'ö': 'o',
            'ṕ': 'p',
            'ş': 's',
            'ś': 's',
            'š': 's',
            'ṫ': 't',
            'ü': 'u',
            'ź': 'z',
            'Á': 'A',
            'Ç': 'C',
            'Ć': 'C',
            'É': 'E',
            'Ǵ': 'G',
            'Ğ': 'G',
            'Ḣ': 'H',
            'İ': 'I',
            'Ḱ': 'K',
            'Ĺ': 'L',
            'Ö': 'O',
            'Ṕ': 'P',
            'Ş': 'S',
            'Ś': 'S',
            'Š': 'S',
            'Ṫ': 'T',
            'Ü': 'U',
            'Ź': 'Z'
        }

        # Cyrillic extra characters to basic set:
        self._cyrillic_extra_to_basic = {
            'щ': 'ш',
            'Щ': 'Ш',
            '1': 'Ӏ',
            'l': 'Ӏ',
            'i': 'Ӏ',
            'I': 'Ӏ',
            'ı': 'Ӏ',
            'İ': 'Ӏ',
            't': 'т',
            'T': 'Т',
            'a': 'а',
            'A': 'А',
            'o': 'о',
            'O': 'О',
            'H': 'Н',
            'B': 'В',
            'b': 'Ь',
            'E': 'Е',
            'e': 'е',
            'K': 'К',
            'k': 'к',
            'M': 'М',
            'm': 'м',
            'P': 'Р',
            'p': 'р',
            'C': 'С',
            'c': 'с',
            'Y': 'У',
            'y': 'у',
            'X': 'Х',
            'x': 'х'
        }

        #######################################
        #          Cyrillic-to-Latin          #
        #######################################

        # Cyrillic to Latin regexps, single char:
        self._cyrillic_to_latin_single_char = {
            'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'ǵ',
            'д': 'd',
            'e': 'é',
            'е': 'é',
            'ж': 'j',
            'з': 'z',
            'и': 'i',
            'й': 'y',
            'к': 'ḱ',
            'k': 'ḱ',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'p': 'r',
            'c': 'с',
            'с': 's',
            'т': 't',
            'у': 'u',
            # 'у': 'w',
            'ф': 'f',
            'х': 'x',
            'ц': 'ś',
            'ч': 'ç',
            'ш': 'ş',
            'щ': 'ş',
            'ы': 'ı',
            'ь': '',
            'Ӏ': "'",
            'э': 'e',
            'ю': 'yu',
            'я': 'ya'
        }

        # Cyrillic to Latin regexps, 2 chars:
        self._cyrillic_to_latin_regexp_2_chars = {
            'гу': 'gu',
            'го': 'go',
            'га': 'ga',
            'гъ': 'ğ',
            'дж': 'c',
            'дз': 'ź',
            'жь': 'j',
            'кӏ': 'ć',
            'кi': 'ć',
            'кӀ': 'ć',
            'ку': 'ḱu',
            'къ': 'k',
            'kӏ': 'ć',
            'ki': 'ć',
            'kӀ': 'ć',
            'kу': 'ḱu',
            'kъ': 'k',
            'лӏ': "ĺ'",
            'лi': "ĺ'",
            'лӀ': "ĺ'",
            'лъ': 'ĺ',
            'шъ': 'ş',
            'шӏ': "ş'",
            'шi': "ş'",
            'шӀ': "ş'",
            'щъ': 'ş',
            'щӏ': "ş'",
            'щi': "ş'",
            'щӀ': "ş'",
            'пӏ': 'ṕ',
            'пi': 'ṕ',
            'пӀ': 'ṕ',
            'тӏ': 'ṫ',
            'тi': 'ṫ',
            'тӀ': 'ṫ',
            'тI': 'ṫ',
            'tӏ': 'ṫ',
            'ti': 'ṫ',
            'tӀ': 'ṫ',
            'tI': 'ṫ',
            'хъ': 'ḣ',
            'хь': 'h',
            'цӏ': 'š',
            'цi': 'š',
            'цӀ': 'š',
            'жъ': 'j',
            'цо': 'çö',
            'цу': 'çü',
            'чӏ': 'ć',
            'чi': 'ć',
            'чӀ': 'ć',
            'чъ': 'ç',
            'ӏу': 'u',
            'iу': 'u',
            'Ӏу': 'u',
            'уэ': 'we',
            'уу': 'wıw',
            'уи': 'wi',
            'ио': 'yiwe',
            'ий': 'yiy',
            'йи': 'yiy',
            'иа': 'iya',
            'йу': 'ywı',
            'оо': 'wewe',
            'ой': 'wey',
            # 'ео': 'yewe',
            'ео': 'éwe',
            'эи': 'ey',
            'эй': 'ey',
            'эе': 'eye',
            'эо': 'ewe',
            'ау': 'aw',
            'эу': 'ew',
            'ао': 'awe',
            'ае': 'aye',
            'уа': 'wa',
            'ие': 'iye',
            'ыо': 'ıwe',
            'ые': 'ıye',
            'ый': 'ıy',
            'ӏэ': 'e',
            'iэ': 'e',
            'Ӏэ': 'e',
            # 'ӏэ': 'a',
            # 'iэ': 'a',
            # 'Ӏэ': 'a',
            'ӏа': 'aá',
            'iа': 'aá',
            'Ӏа': 'aá',
            # 'Iо': 'o',
            # 'ӏо': 'o',
            # 'Ӏо': 'o',
            # 'iо': 'o',
            'Iо': "'o",
            'ӏо': "'o",
            'Ӏо': "'o",
            'iо': "'o",
            'Iи': 'i',
            'ӏи': 'i',
            'iи': 'i',
            'Ӏи': 'i',
            'Iы': 'ı',
            'ӏы': 'ı',
            'iы': 'ı',
            'Ӏы': 'ı',
            # 'ыи': 'ıyı',
            'ыи': 'ıy',
            'ыу\\S': 'ıwı'
        }

        # Cyrillic to Latin regexps, 3 chars:
        self._cyrillic_to_latin_regexp_3_chars = {
            'ыуи': 'ıwi',
            'ӏуа': "oá",
            'iуа': "oá",
            'Ӏуа': "oá",
            # 'гъу': "ğu",
            'жъу': "jü",
            'жъо': "jö",
            'кӏу': "qu",
            'кiу': "qu",
            'кӀу': "qu",
            'кlу': "qu",
            'кӏо': "qo",
            'кiо': "qo",
            'кӀо': "qo",
            # 'кӏи': "ćiy",
            'кӏи': "ći",
            # 'кiи': "ćiy",
            'кiи': "ći",
            # 'кӀи': "ćiy",
            'кӀи': "ći",
            'кӏы': "ćı",
            'кiы': "ćı",
            'кӀы': "ćı",
            'кlы': "ćı",
            'куа': "ḱoá",
            'гуа': "goá",
            'kӏу': "qu",
            'kiу': "qu",
            'kӀу': "qu",
            'klу': "qu",
            'kӏо': "qo",
            'kiо': "qo",
            'kӀо': "qo",
            # 'kӏи': "ćiy",
            'kӏи': "ći",
            # 'kiи': "ćiy",
            'kiи': "ći",
            # 'kӀи': "ćiy",
            'kӀи': "ći",
            'kӏы': "ćı",
            'kiы': "ćı",
            'kӀы': "ćı",
            'klы': "ćı",
            'kуа': "ḱoá",
            'шъу': "şü",
            'шъо': "şö",
            'шӏо': "şü'e",
            'шiо': "şü'e",
            'шӀо': "şü'e",
            'шӏу': "şü'ı",
            'шiу': "şü'ı",
            'шӀу': "şü'ı",
            'шӏи': "ş'i",
            'шiи': "ş'i",
            'шӀи': "ş'i",
            'щъу': "şü",
            'щӏо': "şü'e",
            'щiо': "şü'e",
            'щӀо': "şü'e",
            'щӏу': "şü'ı",
            'щiу': "şü'ı",
            'щӀу': "şü'ı",
            'щӏи': "ş'i",
            'щiи': "ş'i",
            'щӀи': "ş'i",
            'пӏу': "ṕu",
            'пiу': "ṕu",
            'пӀу': "ṕu",
            'хъу': "ḣu",
            'къу': "ku",
            'къo': "ko",
            'kъу': "ku",
            'kъo': "ko",
            'тӏу': "ṫu",
            'тiу': "ṫu",
            'тӀу': "ṫu",
            'тIу': "ṫu",
            'tӏу': "ṫu",
            'tiу': "ṫu",
            'tӀу': "ṫu",
            'tIу': "ṫu",
            'tӏy': "ṫu",
            'tiy': "ṫu",
            'tӀy': "ṫu",
            'tIy': "ṫu",
            'тӏy': "ṫu",
            'тiy': "ṫu",
            'тӀy': "ṫu",
            'тIy': "ṫu",
            'дзу': "źu",
            'Iае': "aye",
            'ӏае': "aye",
            'iае': "aye",
            'Ӏае': "aye",
            'иiу': "iu",
            'иӀу': "iu",
            'иIу': "iu",
            'иiо': "io",
            'иӀо': "io",
            'иIо': "io",
            'эӀе': "eé",
            'эiе': "eé",
            'эIе': "eé"
        }

        # NOTE the upper case and lower case of the Cyrillic "I" looks the same
        # as follows respectively: uc: Ӏ, lc: ӏ

        # Cyrillic to Latin regexps, 4 chars:
        self._cyrillic_to_latin_regexp_4_chars = {
            "кӏуа": "qoá",
            "кiуа": "qoá",
            "кӀуа": "qoá",
            "кӏуa": "qoá",
            "кiуa": "qoá",
            "кӀуa": "qoá",
            "кlуa": "qoá",
            "kӏуа": "qoá",
            "kiуа": "qoá",
            "kӀуа": "qoá",
            "kӏуa": "qoá",
            "kiуa": "qoá",
            "kӀуa": "qoá",
            "klуa": "qoá",
            "кӏуэ": "qo",
            "кiуэ": "qo",
            "кӀуэ": "qo",
            "кlуэ": "qo",
            "kӏуэ": "qo",
            "kiуэ": "qo",
            "kӀуэ": "qo",
            "klуэ": "qo",
            "шӏои": "şü'ey",
            "шiои": "şü'ey",
            "шӀои": "şü'ey",
            "щӏои": "şü'ey",
            "щiои": "şü'ey",
            "щӀои": "şü'ey",
            "гъуа": "ğoá",
            "гъуa": "ğoá",
            "хъуа": "ḣoá",
            "хъуa": "ḣoá",
            "къуа": "koá",
            "къуa": "koá",
            "иӏуа": "ioá",
            "иiуа": "ioá",
            "иӀуа": "ioá"
        }

        # Cyrillic to Latin regexps, prefixes, 1 char:
        self._cyrillic_to_latin_regexp_prefixes_1_char = {
            "^е": "ye",
            "^у[^эаеи]": "wı",
            "^и": "yi",
            "^о": "we"
        }

        # Cyrillic to Latin regexps, prefixes, 2 chars:
        self._cyrillic_to_latin_regexp_prefixes_2_chars = {
            "^Iо": "o",
            "^ӏо": "o",
            "^iо": "o",
            "^Ӏо": "o",
            "^ӏа": "aá",
            "^iа": "aá",
            "^Ӏа": "aá",
            "^ио": "yiwe",
            "^иа": "ya",
            "^уу": "wıw",
            "^уэ": "we",
            "^уа": "wa",
            "^уе": "wé",
            "^уи": "wi"
            # "^аэ": "a"
        }

        # Cyrillic to Latin regexps, prefixes, 3 chars:
        self._cyrillic_to_latin_regexp_prefixes_3_chars = {
            "^иIэ": "yie",
            "^иӏэ": "yie",
            "^иiэ": "yie",
            "^иӀэ": "yie",
            "^иIа": "yia",
            "^иӏа": "yia",
            "^иiа": "yia",
            "^иӀа": "yia",
            "^Iае": "aye",
            "^ӏае": "aye",
            "^iае": "aye",
            "^Ӏае": "aye"
        }

        # Cyrillic to Latin regexps, prefixes, 4 chars:
        self._cyrillic_to_latin_regexp_prefixes_4_chars = {
            "^иIуа": "yioá",
            "^иӏуа": "yioá",
            "^иiуа": "yioá",
            "^иӀуа": "yioá",
        }

        #######################################
        #          Latin-to-Cyrillic          #
        #######################################

        # Latin to Cyrillic regexps, single char:
        self._latin_to_cyrillic_single_char = {
            "'": "Ӏ",
            "a": "а",
            "s": "с",
            "d": "д",
            "f": "ф",
            "g": "г",
            "h": "хь",
            "j": "ж",
            "k": "къ",
            "l": "л",
            "i": "и",
            "q": "кӀ",
            "w": "у",
            "e": "э",
            "r": "р",
            "t": "т",
            # "y": "й",
            "y": "и",
            "u": "у",
            "o": "о",
            "p": "п",
            "z": "з",
            "x": "х",
            "c": "дж",
            "v": "в",
            "b": "б",
            "n": "н",
            "m": "м",
            "á": "а",
            "ç": "ч",
            "ć": "кӀ",
            "é": "е",
            "ǵ": "г",
            "ğ": "гъ",
            "ḣ": "хъ",
            "ı": "ы",
            "ḱ": "к",
            "ĺ": "лъ",
            "ö": "о",
            "ṕ": "пӀ",
            "ş": "ш",
            "ś": "ц",
            "š": "цӀ",
            "ṫ": "тӀ",
            "ü": "u",
            "ź": "дз"
        }

        # Latin to Cyrillic regexps, 2 chars:
        self._latin_to_cyrillic_regexp_2_chars = {
            "aá": "Ӏа",
            "jü": "жъу",
            "jö": "жъо",
            "wı": "у",
            "we": "о",
            "ya": "я",
            "yu": "ю",
            "ye": "е",
            "oá": "уа",
            "çö": "цо",
            "çü": "цу",
            "ĺ'": "лӀ",
            "şü": "шъу",
            "şö": "шъо",
            "ş'": "шӀ"
            # "ı'": "Ӏ"
        }

        # Latin to Cyrillic regexps, 3 chars:
        self._latin_to_cyrillic_regexp_3_chars = {
            "ioá": "иӀуа",
        }

        # Latin to Cyrillic regexps, 4 chars:
        self._latin_to_cyrillic_regexp_4_chars = {
            "şü'e": "шӀо",
            "şü'ı": "шӀу"
        }

        # Latin to Cyrillic regexps, prefixes, 1 char:
        self._latin_to_cyrillic_regexp_prefixes_1_char = {
            "^ı": "ы",
            "^e": "Ӏэ",
            # "^e": "э",
            "^o": "Ӏо",
            "^u": "Ӏу"
            # "^a": "Ӏэ"
        }

        # Latin to Cyrillic regexps, prefixes, 2 chars:
        self._latin_to_cyrillic_regexp_prefixes_2_chars = {
            "^yi": "и",
            "^ye": "е",
            "^aá": "Ӏа"
        }

        # Latin to Cyrillic regexps, prefixes, 3 chars:
        self._latin_to_cyrillic_regexp_prefixes_3_chars = {
        }

        # Latin to Cyrillic regexps, prefixes, 4 chars:
        self._latin_to_cyrillic_regexp_prefixes_4_chars = {
            "^yioá": "иӀуа"
        }

        # Cyrillic Adyghe alphabet characters (letters only, no punctuation)
        self._cyrillic_adyghe_letters = "АБВГДЕЖЗИЙКЛМНОӀПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя"

        # === Pre-compiled lookup tables for optimized matching ===
        # Cyrillic-to-Latin: prefix tables (keys have ^ stripped for startswith)
        self._c2l_pfx3 = [(k.lstrip('^'), v) for k, v in
                          self._cyrillic_to_latin_regexp_prefixes_3_chars.items()]
        self._c2l_pfx4 = [(k.lstrip('^'), v) for k, v in
                          self._cyrillic_to_latin_regexp_prefixes_4_chars.items()]
        self._c2l_pfx2 = [(k.lstrip('^'), v) for k, v in
                          self._cyrillic_to_latin_regexp_prefixes_2_chars.items()]
        # Prefix 1-char: split plain vs regex (only "^у[^эаеи]" needs regex)
        self._c2l_pfx1_plain = []
        self._c2l_pfx1_regex = []
        for k, v in self._cyrillic_to_latin_regexp_prefixes_1_char.items():
            stripped = k.lstrip('^')
            if any(c in stripped for c in r'\[]().*+?{}|$'):
                self._c2l_pfx1_regex.append((re.compile(k + r'\S*'), v))
            else:
                self._c2l_pfx1_plain.append((stripped, v))

        # Cyrillic-to-Latin: non-prefix compound tables
        self._c2l_4 = list(self._cyrillic_to_latin_regexp_4_chars.items())
        self._c2l_3 = list(self._cyrillic_to_latin_regexp_3_chars.items())
        # 2-char: split plain vs regex (only "ыу\S" needs regex)
        self._c2l_2_plain = []
        self._c2l_2_regex = []
        for k, v in self._cyrillic_to_latin_regexp_2_chars.items():
            if any(c in k for c in r'\[]().*+?{}|$'):
                self._c2l_2_regex.append((re.compile(r'^' + k + r'\S*'), v))
            else:
                self._c2l_2_plain.append((k, v))

        # Latin-to-Cyrillic: all plain, no regex keys
        self._l2c_pfx3 = [(k.lstrip('^'), v) for k, v in
                          self._latin_to_cyrillic_regexp_prefixes_3_chars.items()]
        self._l2c_pfx4 = [(k.lstrip('^'), v) for k, v in
                          self._latin_to_cyrillic_regexp_prefixes_4_chars.items()]
        self._l2c_pfx2 = [(k.lstrip('^'), v) for k, v in
                          self._latin_to_cyrillic_regexp_prefixes_2_chars.items()]
        self._l2c_pfx1 = [(k.lstrip('^'), v) for k, v in
                          self._latin_to_cyrillic_regexp_prefixes_1_char.items()]
        self._l2c_4 = list(self._latin_to_cyrillic_regexp_4_chars.items())
        self._l2c_3 = list(self._latin_to_cyrillic_regexp_3_chars.items())
        self._l2c_2 = list(self._latin_to_cyrillic_regexp_2_chars.items())

    def is_cyrillic_adyghe(self, text: str, threshold: float = 0.5) -> bool:
        """
        Detects if the given text is written in the Cyrillic-based Adyghe alphabet.
        
        Args:
            text: The text to check
            threshold: The minimum ratio of Cyrillic Adyghe letters to total letters
                      required to consider the text as Cyrillic Adyghe (default 0.5 = 50%)
        
        Returns:
            True if the text contains mostly Cyrillic Adyghe characters, False otherwise
        """
        if text is None or text == '':
            return False
        
        cyrillic_count = 0
        letter_count = 0
        
        for char in text:
            # Only count alphabetic characters (skip punctuation, spaces, digits)
            if char.isalpha():
                letter_count += 1
                if char in self._cyrillic_adyghe_letters:
                    cyrillic_count += 1
        
        # If no letters found, return False
        if letter_count == 0:
            return False
        
        # Return True if the ratio of Cyrillic letters meets the threshold
        return (cyrillic_count / letter_count) >= threshold

    def _original_is_uppercase(self, original: str, is_latin: bool, is_cyrillic: bool) -> bool:
        if original is None or original == '':
            return False
        is_upper = True
        first_char = original[0]
        if first_char == self.to_lowercase(first_char, is_latin, is_cyrillic) or first_char == "I":
            is_upper = False
        return is_upper

    def sanitize_latin_text(self, text: str) -> str:
        if text is None or text == '':
            return text
        length = len(text)
        if length == 0:
            return text

        text = text.replace('\t', ' ')
        new_text = ''
        for i in range(length):
            current_char = text[i]
            if self.RECOGNIZED_LATIN_CHARS_PATTERN.match(current_char) is not None:
                continue
            new_text = new_text + current_char

        new_text = re.sub(r' +', ' ', new_text).strip()
        new_text = new_text.replace('"', ' ')
        new_text = new_text.replace(':', '.')
        new_text = new_text.replace(';', '.')
        return new_text

    def to_lowercase(self, text: str, is_latin: bool, is_cyrillic: bool) -> str:
        if text is None or text == '':
            return text
        if is_latin and is_cyrillic:
            print('-E- BUG to_lowercase(): is_latin == True && is_cyrillic == True')
        length = len(text)
        if length == 0:
            return text
        if not is_latin and not is_cyrillic:
            return text.lower()
        new_text = ''
        for i in range(length):
            current_char = text[i]
            if is_latin:
                if current_char == "i" or current_char == "İ":
                    current_char = "i"
                elif current_char == "ı" or current_char == "I":
                    current_char = "ı"
                    # Next one is to deal with the "`" character which may be used by mistake
                    # instead of the correct character "'"
                elif current_char == "'" or current_char == "`" or current_char == "’":
                    current_char = "'"
                else:
                    current_char = current_char.lower()
            else:
                if current_char == "I" or current_char == "i" or current_char == "Ӏ"\
                        or current_char == "ı" or current_char == "İ" or current_char == "l":
                    current_char = "Ӏ"
                    # Next one is to deal with the "`" character which may be used by mistake
                    # instead of the correct character "'"
                elif current_char == "'" or current_char == "`" or current_char == "’":
                    current_char = "'"
                else:
                    current_char = current_char.lower()
            new_text = new_text + current_char
        return new_text

    def to_uppercase(self, text: str, is_latin: bool, is_cyrillic: bool) -> str:
        if text is None or text == '':
            return text
        if is_latin and is_cyrillic:
            print('-E- BUG to_uppercase(): is_latin == True && is_cyrillic == True')
        length = len(text)
        if length == 0:
            return text
        if not is_latin and not is_cyrillic:
            return text.upper()
        new_text = ''
        for i in range(length):
            current_char = text[i]
            if is_latin:
                if current_char == "i" or current_char == "İ":
                    current_char = "İ"
                elif current_char == "ı" or current_char == "I":
                    current_char = "I"
                    # Next one is to deal with the "`" character which may be used by mistake
                    # instead of the correct character "'"
                elif current_char == "'" or current_char == "`" or current_char == "’":
                    current_char = "'"
                else:
                    current_char = current_char.upper()
            elif is_cyrillic:
                if current_char == "I" or current_char == "i" or current_char == "Ӏ"\
                        or current_char == "ı" or current_char == "İ" or current_char == "l":
                    current_char = "Ӏ"
                    # Next one is to deal with the "`" character which may be used by mistake
                    # instead of the correct character "'"
                elif current_char == "'" or current_char == "`" or current_char == "’":
                    current_char = "'"
                else:
                    current_char = current_char.upper()
            new_text = new_text + current_char
        return new_text

    def _special_char_to_english_char(self, text: str) -> str:
        if text is None or text == '':
            return text
        text_lc = text.lower()
        converted_text = self._special_to_english.get(text_lc)
        if converted_text is None:
            return text_lc
        else:
            return converted_text

    def special_chars_to_english_chars(self, text: str) -> str:
        if text is None or text == '':
            return text
        converted_parts = []
        length = len(text)
        for i in range(length):
            current_char = text[i]
            converted_parts.append(self._special_char_to_english_char(current_char))
        return ''.join(converted_parts)

    def _cyrillic_extra_char_to_basic_char(self, text: str) -> str:
        if text is None or text == '':
            return text
        converted_text = self._cyrillic_extra_to_basic.get(text)
        if converted_text is None:
            return text
        else:
            return converted_text

    def cyrillic_extra_chars_to_basic_chars(self, text: str) -> str:
        if text is None or text == '':
            return text
        converted_parts = []
        length = len(text)
        for i in range(length):
            current_char = text[i]
            # Special handling for digit '1': only treat as palochka substitute
            # when the preceding char is Cyrillic. Otherwise keep it as digit.
            if current_char == '1':
                prev_char = text[i - 1] if i > 0 else ''
                if '\u0400' <= prev_char <= '\u04FF':
                    converted_parts.append('Ӏ')
                else:
                    converted_parts.append('1')
                continue
            converted_parts.append(self._cyrillic_extra_char_to_basic_char(current_char))
        return ''.join(converted_parts)

    def capitalize(self, text: str, is_latin: bool, is_cyrillic: bool) -> str:
        if text is None or text == '':
            return text
        return self.to_uppercase(text[0], is_latin, is_cyrillic)\
            + self.to_lowercase(text[1:], is_latin, is_cyrillic)

    def cyrillic_to_latin(self, text: str) -> str:
        if text is None or text == '':
            return text
        tokens_and_spaces = []
        current_token = ''
        spaces = True
        for index in range(len(text)):
            single_char = text[index]
            if single_char == "":
                continue
            if len(single_char.strip()) == 0:
                if spaces:
                    current_token = current_token + single_char
                else:
                    spaces = True
                    if current_token != '':
                        tokens_and_spaces.append(current_token)
                    current_token = single_char
            else:
                if spaces:
                    spaces = False
                    if current_token != '':
                        tokens_and_spaces.append(current_token)
                    current_token = single_char
                else:
                    current_token = current_token + single_char
        if current_token != '':
            tokens_and_spaces.append(current_token)

        result_parts = []
        # Strip any run of leading non-alphabetic chars (quotes, parens, etc.)
        # so word-start prefix rules still apply to tokens like `"ИIэм` or `(уи...`.
        # The hyphen `-` is kept out of the strip set so hyphenated compounds
        # (e.g. `II-рэ`) still split below.
        leading_punct = set('("\'«»\u201c\u201d\u2018\u2019[{')
        for token in tokens_and_spaces:
            removed_prefix = ''
            while len(token) > 1 and token[0] in leading_punct:
                removed_prefix += token[0]
                token = token[1:]
            # Legacy single-char strip for '-' (keeps pre-existing behavior for
            # tokens like `-рэ` where the '-' is purely decorative).
            if token and token[0] == '-' and len(token) > 1:
                removed_prefix += token[0]
                token = token[1:]
            # Split on hyphens so each part gets word-start prefix handling
            if '-' in token:
                parts = token.split('-')
                converted_parts = [self._convert_cyrillic_part(part) for part in parts]
                result_parts.append(removed_prefix + '-'.join(converted_parts))
            else:
                result_parts.append(removed_prefix + self._convert_cyrillic_part(token))
        return ''.join(result_parts)

    # Roman numerals written with Latin capitals. Tokens consisting entirely of
    # these chars are preserved as-is instead of being treated as palochka
    # substitutes.
    _ROMAN_NUMERAL_CHARS = frozenset('IVXLCDM')

    def _convert_cyrillic_part(self, part: str) -> str:
        """Convert a single hyphen-delimited sub-token, preserving Roman
        numerals that would otherwise be misread as palochkas."""
        if part and all(c in self._ROMAN_NUMERAL_CHARS for c in part):
            return part
        return self._cyrillic_to_latin_single_word(part)

    def _cyrillic_to_latin_single_word(self, word: str) -> str:
        if word is None or word == '':
            return word
        len_cyrillic = len(word)
        if len_cyrillic == 0:
            return ''
        orig_word = word
        word = self.to_lowercase(word, False, True)
        word = self.cyrillic_extra_chars_to_basic_chars(word)
        new_word_parts = []
        i = 0
        # Note: using a separate index 'i' instead of using j from the 'for' loop
        # because 'i' needs to be updated in increments which are not always '1'
        # and that does not work well with the "i in range()' method
        for j in range(len_cyrillic):
            current_char = word[i:]
            current_char_orig = orig_word[i:]
            next_char = ''
            if len_cyrillic > 1:
                next_char = orig_word[i+1:]
            is_upper = self._original_is_uppercase(current_char_orig, False, True)
            next_char_is_upper = self._original_is_uppercase(next_char, False, True)
            matched = False
            if i == 0:
                # 4 char prefixes
                for key, value in self._c2l_pfx4:
                    if current_char.startswith(key):
                        i = i + 4
                        matched = True
                        converted_char = value
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, True, False)
                            else:
                                converted_char = self.capitalize(converted_char, True, False)
                        new_word_parts.append(converted_char)
                        break
                if i >= len_cyrillic:
                    break
                if matched:
                    continue
                # 3 char prefixes
                for key, value in self._c2l_pfx3:
                    if current_char.startswith(key):
                        i = i + 3
                        matched = True
                        converted_char = value
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, True, False)
                            else:
                                converted_char = self.capitalize(converted_char, True, False)
                        new_word_parts.append(converted_char)
                        break
                if i >= len_cyrillic:
                    break
                if matched:
                    continue
                # 2 char prefixes
                for key, value in self._c2l_pfx2:
                    if current_char.startswith(key):
                        i = i + 2
                        matched = True
                        converted_char = value
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, True, False)
                            else:
                                converted_char = self.capitalize(converted_char, True, False)
                        new_word_parts.append(converted_char)
                        break
                if i >= len_cyrillic:
                    break
                if matched:
                    continue
                # 1 char prefix
                for key, value in self._c2l_pfx1_plain:
                    if current_char.startswith(key):
                        i = i + 1
                        matched = True
                        converted_char = value
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, True, False)
                            else:
                                converted_char = self.capitalize(converted_char, True, False)
                        new_word_parts.append(converted_char)
                        break
                if not matched:
                    for pattern, value in self._c2l_pfx1_regex:
                        if pattern.match(current_char):
                            i = i + 1
                            matched = True
                            converted_char = value
                            if is_upper:
                                if next_char_is_upper:
                                    converted_char = self.to_uppercase(converted_char, True, False)
                                else:
                                    converted_char = self.capitalize(converted_char, True, False)
                            new_word_parts.append(converted_char)
                            break
                if i >= len_cyrillic:
                    break
                if matched:
                    continue
            # 4-chararcter compounds
            for key, value in self._c2l_4:
                if current_char.startswith(key):
                    i = i + 4
                    matched = True
                    converted_char = value
                    if is_upper:
                        if next_char_is_upper:
                            converted_char = self.to_uppercase(converted_char, True, False)
                        else:
                            converted_char = self.capitalize(converted_char, True, False)
                    new_word_parts.append(converted_char)
                    break
            if i >= len_cyrillic:
                break
            if matched:
                continue
            # 3-chararcter compounds
            for key, value in self._c2l_3:
                if current_char.startswith(key):
                    i = i + 3
                    matched = True
                    converted_char = value
                    if is_upper:
                        if next_char_is_upper:
                            converted_char = self.to_uppercase(converted_char, True, False)
                        else:
                            converted_char = self.capitalize(converted_char, True, False)
                    new_word_parts.append(converted_char)
                    break
            if i >= len_cyrillic:
                break
            if matched:
                continue
            # 2-chararcter compounds
            for key, value in self._c2l_2_plain:
                if current_char.startswith(key):
                    i = i + 2
                    matched = True
                    converted_char = value
                    # Drop leading apostrophe when previous Latin char is a vowel
                    if converted_char.startswith("'") and new_word_parts and new_word_parts[-1][-1] in 'aeiouyıáéöü':
                        converted_char = converted_char[1:]
                    if is_upper:
                        if next_char_is_upper:
                            converted_char = self.to_uppercase(converted_char, True, False)
                        else:
                            converted_char = self.capitalize(converted_char, True, False)
                    new_word_parts.append(converted_char)
                    break
            if not matched:
                for pattern, value in self._c2l_2_regex:
                    if pattern.match(current_char):
                        i = i + 2
                        matched = True
                        converted_char = value
                        if converted_char.startswith("'") and new_word_parts and new_word_parts[-1][-1] in 'aeiouyıáéöü':
                            converted_char = converted_char[1:]
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, True, False)
                            else:
                                converted_char = self.capitalize(converted_char, True, False)
                        new_word_parts.append(converted_char)
                        break
            if i >= len_cyrillic:
                break
            if matched:
                continue
            current_char = word[i]
            current_char_orig = orig_word[i]
            is_upper = self._original_is_uppercase(current_char_orig, False, True)
            # 1-chararcter
            converted_char = self._cyrillic_to_latin_single_char.get(current_char)
            if converted_char is not None:
                matched = True
                if i > 0:
                    with_prev_char = word[i - 1: i + 1]
                    if with_prev_char == 'оо':
                        converted_char = 'we'
                    elif with_prev_char == 'уо':
                        converted_char = 'we'
                    elif with_prev_char == 'оу':
                        converted_char = 'w'
                    elif with_prev_char == 'уу':
                        converted_char = 'w'
                    elif with_prev_char == 'еу':
                        converted_char = 'w'
                    elif with_prev_char == 'ыу':
                        converted_char = 'w'
                    elif with_prev_char == 'иу':
                        converted_char = 'w'
                    elif with_prev_char == 'эу':
                        converted_char = 'w'
                    # elif with_prev_char == 'уа':
                    #     converted_char = 'á'
                    elif with_prev_char == 'аи':
                        # converted_char = 'yı'
                        converted_char = 'y'
                        if (i + 1) == len_cyrillic:
                            converted_char = 'y'
                    elif current_char == 'е' and word[i - 1] in 'аеиоуэы':
                        converted_char = 'ye'
                    elif current_char == 'у':
                        if (i + 1) == len_cyrillic:
                            converted_char = "u'"
                        # elif word[i: i + 2] == 'уа':
                        #     converted_char = 'oá'
                i = i + 1
                if is_upper:
                    if next_char_is_upper:
                        converted_char = self.to_uppercase(converted_char, True, False)
                    else:
                        converted_char = self.capitalize(converted_char, True, False)
                new_word_parts.append(converted_char)
            if i >= len_cyrillic:
                break
            if matched:
                continue
            # no match
            new_word_parts.append(current_char_orig)
            i = i + len(current_char_orig)
        return ''.join(new_word_parts)

    def latin_to_cyrillic(self, text: str) -> str:
        if text is None or text == '':
            return text
        tokens_and_spaces = []
        current_token = ''
        spaces = True
        for index in range(len(text)):
            single_char = text[index]
            if single_char == '':
                continue
            if len(single_char.strip()) == 0:
                if spaces:
                    current_token = current_token + single_char
                else:
                    spaces = True
                    if current_token != '':
                        tokens_and_spaces.append(current_token)
                    current_token = single_char
            else:
                if spaces:
                    spaces = False
                    if current_token != '':
                        tokens_and_spaces.append(current_token)
                    current_token = single_char
                else:
                    current_token = current_token + single_char
        if current_token != '':
            tokens_and_spaces.append(current_token)

        result_parts = []
        for token in tokens_and_spaces:
            # TODO currently handles only words that start with '(',
            #  need to support any non-alphabet chars of any length as a prefix
            removed_prefix = ''
            if token[0] in '(-' and len(token) > 1:
                removed_prefix = token[0]
                token = token[1:]
            result_parts.append(removed_prefix + self._latin_to_cyrillic_single_word(token))
        return ''.join(result_parts)

    def _latin_to_cyrillic_single_word(self, word: str) -> str:
        if word is None or word == '':
            return word
        len_latin = len(word)
        if len_latin == 0:
            return ''
        orig_word = word
        word = self.to_lowercase(word, True, False)
        new_word_parts = []
        i = 0
        # Note: using a separate index 'i' instead of using j from the 'for' loop
        # because 'i' needs to be updated in increments which are not always '1'
        # and that does not work well with the "i in range()' method
        for j in range(len_latin):
            current_char = word[i:]
            current_char_orig = orig_word[i:]
            is_upper = self._original_is_uppercase(current_char_orig, True, False)
            # Look at the next Latin char so we can distinguish word-initial
            # capitalization (e.g. `Cıri` -> `Джыри`) from an all-caps run
            # (e.g. `CIRI` -> `ДЖИРИ`). Mirrors the C2L logic.
            next_char_orig = orig_word[i + 1:] if (i + 1) < len_latin else ''
            next_char_is_upper = self._original_is_uppercase(
                next_char_orig, True, False
            )
            matched = False
            if i == 0:
                # TODO remove all unneeded hash maps (3-chars and maybe others)
                # 4 char prefixes
                for key, value in self._l2c_pfx4:
                    if current_char.startswith(key):
                        i = i + 4
                        matched = True
                        converted_char = value
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, False, True)
                            else:
                                converted_char = self.capitalize(converted_char, False, True)
                        new_word_parts.append(converted_char)
                        break
                if i >= len_latin:
                    break
                if matched:
                    continue
                # 3 char prefixes
                for key, value in self._l2c_pfx3:
                    if current_char.startswith(key):
                        i = i + 3
                        matched = True
                        converted_char = value
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, False, True)
                            else:
                                converted_char = self.capitalize(converted_char, False, True)
                        new_word_parts.append(converted_char)
                        break
                if i >= len_latin:
                    break
                if matched:
                    continue
                # 2 char prefixes
                for key, value in self._l2c_pfx2:
                    if current_char.startswith(key):
                        # i = i + regex.length() - 1
                        i = i + 2
                        matched = True
                        converted_char = value
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, False, True)
                            else:
                                converted_char = self.capitalize(converted_char, False, True)
                        new_word_parts.append(converted_char)
                        break
                if i >= len_latin:
                    break
                if matched:
                    continue
                # 1 char prefixes
                for key, value in self._l2c_pfx1:
                    if current_char.startswith(key):
                        i = i + 1
                        matched = True
                        converted_char = value
                        if is_upper:
                            if next_char_is_upper:
                                converted_char = self.to_uppercase(converted_char, False, True)
                            else:
                                converted_char = self.capitalize(converted_char, False, True)
                        new_word_parts.append(converted_char)
                        break
                if i >= len_latin:
                    break
                if matched:
                    continue
            # 4-chararcter compounds
            for key, value in self._l2c_4:
                if current_char.startswith(key):
                    i = i + 4
                    matched = True
                    converted_char = value
                    if is_upper:
                        if next_char_is_upper:
                            converted_char = self.to_uppercase(converted_char, False, True)
                        else:
                            converted_char = self.capitalize(converted_char, False, True)
                    new_word_parts.append(converted_char)
                    break
            if i >= len_latin:
                break
            if matched:
                continue
            # 3-chararcter compounds
            for key, value in self._l2c_3:
                if current_char.startswith(key):
                    i = i + 3
                    matched = True
                    converted_char = value
                    if is_upper:
                        if next_char_is_upper:
                            converted_char = self.to_uppercase(converted_char, False, True)
                        else:
                            converted_char = self.capitalize(converted_char, False, True)
                    new_word_parts.append(converted_char)
                    break
            if i >= len_latin:
                break
            if matched:
                continue
            # 2-chararcter compounds
            for key, value in self._l2c_2:
                if current_char.startswith(key):
                    i = i + 2
                    matched = True
                    converted_char = value
                    if is_upper:
                        if next_char_is_upper:
                            converted_char = self.to_uppercase(converted_char, False, True)
                        else:
                            converted_char = self.capitalize(converted_char, False, True)
                    new_word_parts.append(converted_char)
                    break
            if i >= len_latin:
                break
            if matched:
                continue

            current_char = word[i]
            current_char_orig = orig_word[i]
            is_upper = self._original_is_uppercase(current_char_orig, True, False)
            # 1-chararcters
            converted_char = self._latin_to_cyrillic_single_char.get(current_char)
            if converted_char is not None:
                matched = True
                if i > 0:
                    with_prev_char = word[i - 1: i + 1]
                    prev_char = word[i - 1: i]
                    if with_prev_char == 'eu':
                        converted_char = 'Ӏу'
                    elif with_prev_char == 'ie':
                        converted_char = 'Ӏэ'
                    # elif with_prev_char == "ı'":  # TODO doesn't seem to work??
                    #     converted_char = 'Ӏ'
                    elif with_prev_char == 'eo':
                        converted_char = 'Ӏо'
                    elif with_prev_char == "u'" and i == (len_latin-1):  # TODO doesn't seem to work??
                        converted_char = ''
                    # elif current_char == 'a' and prev_char in "ouei'ı":
                    elif current_char == 'a' and prev_char in "aoueiı":
                        # converted_char = 'Ӏа'
                        converted_char = 'а'
                    elif current_char == 'e' and prev_char in "aoueiı":
                        converted_char = 'Ӏэ'
                    elif current_char == 'u' and prev_char in "aoueiı":
                        converted_char = 'Ӏу'
                    elif current_char == 'o' and prev_char in "aoueiı":
                        converted_char = 'Ӏо'
                    elif current_char == 'y' and prev_char in "aoueiı":
                        converted_char = 'й'
                i = i + 1
                if is_upper:
                    if next_char_is_upper:
                        converted_char = self.to_uppercase(converted_char, False, True)
                    else:
                        converted_char = self.capitalize(converted_char, False, True)
                new_word_parts.append(converted_char)
            if i >= len_latin:
                break
            if matched:
                continue
            # no match
            new_word_parts.append(current_char_orig)
            i = i + len(current_char_orig)
        # TODO is next one needed?
        # new_word.replace('ı', 'Ӏ')  # was a no-op
        return ''.join(new_word_parts)


"""
áçćéǵğḣıḱĺöṕşśšṫüź
ÁÇĆÉǴĞḢİḰĹÖṔŞŚŠṪÜŹ

áçćéǵğḣıḱĺöṕşśšṫüź abcdefghijklmnopqrstuvwxyz
á|ç|ć|é|ǵ|ğ|ḣ|ı|ḱ|ĺ|ö|ṕ|ş|ś|š|ṫ|ü|ź|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z


А Б В Г Д Е Ё Ж З И Й К Л М Н О Ӏ П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я
а б в г д е ё ж з и й к л м н о   п р с т у ф х ц ч ш щ ъ ы ь э ю я

АДЫГЭ
аtын

Гъу Жъу КӀу Шъу ШӀу ПӀу Хъу Къу ТӀу Дзу
Гу Гъ Дж Дз Жь КӀ Ку Къ ЛӀ Лъ Шъ ПӀ ТӀ Хъ Хь ЦӀ Жъ Цу ЧӀ ЧЪ ШӀ Ӏу
А Б В Г Д Е Ё Ж З И Й К Л М Н О Ӏ П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я
"""

def _convert_batch(args_tuple):
    """Worker function for multiprocessing. Converts a batch of lines."""
    direction, lines_batch = args_tuple
    utils = AdigaCharacterUtils()
    convert = utils.cyrillic_to_latin if direction == 'c2l' \
        else utils.latin_to_cyrillic
    return [convert(line) for line in lines_batch]


def main():
    parser = argparse.ArgumentParser(
        description='Convert text between Cyrillic and Latin Adyghe scripts.'
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-i', '--input',
                             help='Path to the input text file')
    input_group.add_argument('-t', '--text',
                             help='Input text string to convert')
    parser.add_argument('-o', '--output', default=None,
                        help='Path to the output text file (default: stdout)')
    parser.add_argument('-d', '--direction', required=True,
                        choices=['c2l', 'l2c'],
                        help='Conversion direction: c2l (Cyrillic to Latin) '
                             'or l2c (Latin to Cyrillic)')
    args = parser.parse_args()

    direction_label = 'Cyrillic → Latin' if args.direction == 'c2l' \
        else 'Latin → Cyrillic'
    char_utils = AdigaCharacterUtils()
    convert = char_utils.cyrillic_to_latin if args.direction == 'c2l' \
        else char_utils.latin_to_cyrillic

    if args.input:
        with open(args.input, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        total_lines = len(lines)
        total_chars = sum(len(line) for line in lines)
        num_workers = min(os.cpu_count() or 1, max(1, total_lines // 100))
        source_label = args.input

        print(f'Direction:  {direction_label}', file=sys.stderr)
        print(f'Input:      {source_label}', file=sys.stderr)
        print(f'Output:     {args.output if args.output else "<stdout>"}',
              file=sys.stderr)
        print(f'Lines:      {total_lines}', file=sys.stderr)
        print(f'Characters: {total_chars}', file=sys.stderr)
        print(f'Workers:    {num_workers}', file=sys.stderr)
        print(file=sys.stderr)

        start_time = time.time()
        bar_width = 40

        if num_workers <= 1:
            # Single-process path: small files or single-core machines
            converted_lines = []
            for idx, line in enumerate(lines, 1):
                converted_lines.append(convert(line))
                progress = idx / total_lines
                filled = int(bar_width * progress)
                bar = '█' * filled + '░' * (bar_width - filled)
                print(f'\r  [{bar}] {idx}/{total_lines} lines ({progress:.0%})',
                      end='', file=sys.stderr)
        else:
            # Multi-process path: split lines into batches, one per worker
            batch_size = (total_lines + num_workers - 1) // num_workers
            batches = []
            for start in range(0, total_lines, batch_size):
                batches.append(
                    (args.direction, lines[start:start + batch_size])
                )

            converted_lines = []
            done_lines = 0
            with multiprocessing.Pool(processes=num_workers) as pool:
                for batch_result in pool.imap(_convert_batch, batches):
                    converted_lines.extend(batch_result)
                    done_lines += len(batch_result)
                    progress = done_lines / total_lines
                    filled = int(bar_width * progress)
                    bar = '█' * filled + '░' * (bar_width - filled)
                    print(
                        f'\r  [{bar}] {done_lines}/{total_lines} lines '
                        f'({progress:.0%})',
                        end='', file=sys.stderr)

        elapsed = time.time() - start_time
        print(file=sys.stderr)  # newline after progress bar
        result = ''.join(converted_lines)
        words = sum(len(line.split()) for line in lines)
    else:
        text = args.text or ''
        total_chars = len(text)
        total_lines = len(text.splitlines()) if text else 0
        source_label = '<text>'

        print(f'Direction:  {direction_label}', file=sys.stderr)
        print(f'Input:      {source_label}', file=sys.stderr)
        print(f'Output:     {args.output if args.output else "<stdout>"}',
              file=sys.stderr)
        print(f'Lines:      {total_lines}', file=sys.stderr)
        print(f'Characters: {total_chars}', file=sys.stderr)
        print('Workers:    1', file=sys.stderr)
        print(file=sys.stderr)

        start_time = time.time()
        result = convert(text)
        elapsed = time.time() - start_time
        words = len(text.split())

    is_text_input = args.text is not None and not args.input

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as outfile:
            outfile.write(result)
    else:
        sys.stdout.write(result)
        if is_text_input and not result.endswith('\n'):
            sys.stdout.write('\n')

    # Speed statistics
    chars_per_sec = total_chars / elapsed if elapsed > 0 else 0
    words_per_sec = words / elapsed if elapsed > 0 else 0
    print(file=sys.stderr)
    if args.input:
        print(f'Completed in {elapsed:.3f}s ({num_workers} workers)',
              file=sys.stderr)
    else:
        print(f'Completed in {elapsed:.3f}s (1 worker)', file=sys.stderr)
    print(f'Speed: {chars_per_sec:,.0f} chars/s | {words_per_sec:,.0f} words/s',
          file=sys.stderr)


if __name__ == '__main__':
    main()
