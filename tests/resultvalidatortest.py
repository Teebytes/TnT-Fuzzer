from unittest import TestCase

from mock import MagicMock

from tntfuzzer.resultvalidatior import ResultValidator


class ResultValidatorTest(TestCase):
    SAMPLE_RESPONSES = {
               "405": {
                  "description": "Invalid input"
               }
            }

    def setUp(self):
        self.validator = ResultValidator()
        self.response = MagicMock()
        self.response.status_code = 405
        self.response.documented_reason = 'doc reason'
        self.response.text = 'Error text from server'

    def test_evaluate_returns_none_when_resp_status_code_in_expected_responses(self):
        result = self.validator.evaluate(self.response, self.SAMPLE_RESPONSES, True)
        self.assertEqual(result, {'body': 'Error text from server', 'status_code': 405,
                                  'documented_reason': 'Invalid input'})

    def test_evaluate_returns_result_log_when_resp_status_code_not_expected_responses_and_logging_not_forced(self):
        self.response.status_code = 500
        self.response.text = 'Internal Error'
        result = self.validator.evaluate(self.response, self.SAMPLE_RESPONSES, True)
        self.assertEqual(result, {"status_code": 500, "body": 'Internal Error', "documented_reason": None})

    def test_evaluate_returns_log_when_resp_status_code_in_expected_responses_and_forced_for_all_codes(self):
        result = self.validator.evaluate(self.response, self.SAMPLE_RESPONSES, False)
        self.assertEqual(result, {"status_code": 405,
                                  "body": 'Error text from server',
                                  "documented_reason": 'Invalid input'})

    def test_evaluate_returns_log_when_resp_status_code_not_in_expected_responses_and_forced_for_all_codes(self):
        self.response.status_code = 500
        self.response.text = 'Internal Error'
        result = self.validator.evaluate(self.response, self.SAMPLE_RESPONSES, False)
        self.assertEqual(result, {"status_code": 500, "body": 'Internal Error', "documented_reason": None})
