import requests

from requests import Session

from requests_ntlm import HttpNtlmAuth

from zeep import Client

from zeep.transports import Transport

from requests.auth import HTTPBasicAuth

from datetime import datetime



AUTHS = Session()



WEB_SERVICE_PWD = "W3C0d3@llD@y"



BASE_URL = 'http://20.231.15.166:7047/BC140/WS/CRONUS%20International%20Ltd./Codeunit/Webportal'



AUTHS.auth = HTTPBasicAuth('COKUNE', WEB_SERVICE_PWD)

CLIENT = Client(BASE_URL, transport=Transport(session=AUTHS))





result = CLIENT.service.FnResetVendorPassword(

    'cokune@kobby.co.ke',"123456", 'xyz')
    

print(result)