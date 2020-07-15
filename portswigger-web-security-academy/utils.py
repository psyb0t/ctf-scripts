import re


def csrf_from_response_text(response_text):
    csrf_regex_search = re.search(r'name="csrf" value="(.*?)"',
                                  response_text, re.IGNORECASE | re.DOTALL | re.MULTILINE)

    if not csrf_regex_search:
        exit('get csrf err')

    return csrf_regex_search[1]
