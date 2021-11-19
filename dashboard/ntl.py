import requests
from requests_ntlm import HttpNtlmAuth

username = "fke-admin"
password = "Administrator#2021!"
site_url = "http://102.37.117.22:1447/ADMINBC/WS/FKETEST/Codeunit/MemberPortal/"
r = requests.get(site_url, auth=HttpNtlmAuth(
    'domain\\fke-admin', 'Administrator#2021!'))

print(r.status_code)
