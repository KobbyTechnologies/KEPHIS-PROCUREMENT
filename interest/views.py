from django.shortcuts import render, redirect
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime

# Create your views here.


def interest_request(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        EOI = []
        for tender in response['value']:
            if tender['Process_Type'] == 'EOI':
                output_json = json.dumps(tender)
                EOI.append(json.loads(output_json))
                res = EOI
    except requests.exceptions.ConnectionError as e:
        print(e)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res}
    return render(request, 'interest.html', ctx)


def EOI_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")
    try:
        r = session.get(Access2, timeout=7).json()
        response = session.get(Access_Point, timeout=9).json()
        EOI = []
        Doc = []
        for tender in response['value']:
            if tender['Process_Type'] == 'EOI':
                output_json = json.dumps(tender)
                EOI.append(json.loads(output_json))
                responses = EOI
                for my_tender in responses:
                    if my_tender['No'] == pk:
                        res = tender
        for docs in r['value']:
            if docs['QuoteNo'] == pk:
                output_json = json.dumps(docs)
                Doc.append(json.loads(output_json))
                my_doc = Doc
    except requests.exceptions.ConnectionError as e:
        print(e)

    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res, "docs": my_doc}
    return render(request, "EDetails.html", ctx)
