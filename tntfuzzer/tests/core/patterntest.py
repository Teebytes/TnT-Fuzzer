from unittest import TestCase

from core.pattern import Pattern, MaxLengthException, WasNotFoundException


class PatternTest(TestCase):

    def test_gen_returns_pattern_with_demanded_length(self):
        result = Pattern.gen(50)

        self.assertEqual(50, len(result))

    def test_gen_always_returns_same_pattern_with_same_param_length(self):
        result = Pattern.gen(50)

        self.assertEqual('Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab', result)

    def test_gen_throws_exception_when_param_length_exceeds_limit(self):
        self.assertRaises(MaxLengthException, Pattern.gen, Pattern.MAX_LENGTH + 50)

    def test_search_finds_pattern_position(self):
        result = Pattern.search('1Ab2Ab3Ab4')

        self.assertEqual(35, result)

    def test_search_throws_exception_when_pattern_not_found(self):
        self.assertRaises(WasNotFoundException, Pattern.search, "IamNotInDaPattern")
