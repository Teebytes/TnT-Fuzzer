

class ResultValidator:
    def __init__(self):
        pass

    def evaluate(self, response, response_infos, log_unexpected_errors_only):
        result_log = dict()

        result_log['status_code'] = response.status_code
        result_log['body'] = response.text
        result_log['documented_reason'] = ''

        # response is documented in open api
        if str(response.status_code) in response_infos:
            result_log['documented_reason'] = response_infos[str(response.status_code)]['description']

            if log_unexpected_errors_only:
                return None

        return result_log
