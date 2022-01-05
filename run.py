# import requests
# from requests_ntlm import HttpNtlmAuth

# username = "fke-admin"
# password = "Administrator#2021!"

# site_url = "http://102.37.117.22:1448/ADMINBC/ODataV4/Company('FKETEST')/UpcomingEvents"

# r = requests.get(site_url, auth=HttpNtlmAuth(username, password))

# print(r.status_code)

import requests
from requests_ntlm import HttpNtlmAuth

username = "NAVADMIN"
password = "N@vAdm$n2030!!"

site_url = "http://13.68.215.64:1248/BC140/ODataV4/Company(%27KMPDC%27)/ProspectiveSuppliercard"

r = requests.get(site_url, auth=HttpNtlmAuth(username, password))

print(r.content)

# import requests
# from requests_ntlm import HttpNtlmAuth

# username = "NAVADMIN"
# password = "N@vAdm$n2030!!"

# site_url = "http://13.68.215.64:1248/BC140/ODataV4/Company(%27KMPDC%27)/ProspectiveSuppliercard"

# r = requests.get(site_url, auth=HttpNtlmAuth(username, password))

# print(r.status_code)


# import requests
# from requests import Session
# from requests_ntlm import HttpNtlmAuth
# from zeep import Client
# from zeep.transports import Transport


# AUTHS = Session()

# WEB_SERVICE_PWD = 'Akinyi2013'
# BASE_URL = 'http://13.68.215.64:1347/KMPDC/WS/KMPDC/Page/RFQ_Prospective_Supplier_card'

# AUTHS.auth = HttpNtlmAuth('domain\\Winnie', WEB_SERVICE_PWD)
# CLIENT = Client(BASE_URL, transport=Transport(session=AUTHS))


# result = CLIENT.service.Prospective_Supplier_Tenders(111111, 1111111, 222222)
# print(result)

# def details(request, pk):
#     session = requests.Session()
#     session.auth = config.AUTHS

#     Access_Point = config.O_DATA.format("/ProspectiveSuppliercard")
#     response = session.get(Access_Point).json()

#     for tender in response['value']:
#         if tender['No'] == pk:
#             res = tender
#             type = tender['City']
#     todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
#     ctx = {"today": todays_date, "res": res, 'type': type}
#     return render(request, "main/details.html", ctx)
