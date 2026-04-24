from adyghe_latin_utils.character_utils import AdigaCharacterUtils


class TestSanitizeLatinText:
    def test_none_and_empty_passthrough(self):
        utils = AdigaCharacterUtils()

        assert utils.sanitize_latin_text(None) is None
        assert utils.sanitize_latin_text('') == ''

    def test_replaces_tabs_and_collapses_spaces(self):
        utils = AdigaCharacterUtils()

        assert utils.sanitize_latin_text('  a\t\tb   c  ') == 'a b c'

    def test_removes_unsupported_characters(self):
        utils = AdigaCharacterUtils()

        assert utils.sanitize_latin_text('adıǵe🙂#123') == 'adıǵe'

    def test_normalizes_quotes_colons_and_semicolons(self):
        utils = AdigaCharacterUtils()

        assert utils.sanitize_latin_text('a"b:c;d') == 'ab.c.d'
