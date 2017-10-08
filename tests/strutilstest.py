from unittest import TestCase

from tntfuzzer.strutils import StrUtils


class StrUtilsTest(TestCase):

    def test_fill_string_up_with_blanks_appends_number_blanks_to_string_smaller_than_max(self):
        result = StrUtils.fill_string_up_with_blanks('this is test', 15)
        self.assertEqual('this is test   ', result)

    def test_fill_string_up_with_blanks_wont_append_blanks_to_string_bigger_than_max(self):
        result = StrUtils.fill_string_up_with_blanks('this is test', 8)
        self.assertEqual('this is test', result)

    def test_fill_string_up_with_blanks_wont_append_blanks_to_string_bigger_exact_max(self):
        result = StrUtils.fill_string_up_with_blanks('this is test', 12)
        self.assertEqual('this is test', result)
