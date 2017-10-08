

class ResultValidator:
    def __init__(self):
        pass

    def evaluate(self, response, response_infos, log_unexpected_errors_only):
        result_log = dict()

        result_log['status_code'] = response.status_code
        result_log['body'] = response.text
        result_log['documented_reason'] = None

        # response is documented in open api for operation
        if str(response.status_code) in response_infos:
            result_log['documented_reason'] = response_infos[str(response.status_code)]['description']

        return result_log
