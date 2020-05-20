import termcolor
import sys


class StrUtils:

    def __init__(self):
        pass

    @staticmethod
    def print_log_row(op_code, url, status_code, documented_reason, body, curlcommand):
        if type(curlcommand) == str:
            curlstr = curlcommand
        else:
            curlstr = curlcommand.get()
        print(termcolor.colored(StrUtils.fill_string_up_with_blanks(op_code, 7), color='red') + ' | ' +
              termcolor.colored(StrUtils.fill_string_up_with_blanks(url, 100), color='green') + ' |-| ' +
              StrUtils.fill_string_up_with_blanks(status_code, 3) + ' | ' +
              StrUtils.fill_string_up_with_blanks(documented_reason, 20) + ' | ' +
              body + ' | ' + curlstr)

    @staticmethod
    def fill_string_up_with_blanks(fillup_string, num_chars):
        if fillup_string is None:
            return 'None   '
        if len(fillup_string) > num_chars:
            return fillup_string
        else:
            num_blanks = num_chars - len(fillup_string)
            for x in range(0, num_blanks):
                fillup_string = fillup_string + ' '

            return fillup_string
