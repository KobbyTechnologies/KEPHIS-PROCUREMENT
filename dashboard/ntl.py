import requests
from requests_ntlm import HttpNtlmAuth
import json
import random
import xmltodict

session = requests.Session()
session.auth = HttpNtlmAuth('domain\\fke-admin', 'Administrator#2021!')
response = session.get(
    'http://102.37.117.22:1447/ADMINBC/WS/FKETEST/Codeunit/MemberPortal')


dictionary = xmltodict.parse(response.text)
json_obj = json.dumps(dictionary)
print(response.text)
