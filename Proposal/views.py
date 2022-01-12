from django.shortcuts import render, redirect
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime

# Create your views here.


def proposal_request(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        RFP = []
        for tender in response['value']:
            if tender['Process_Type'] == 'RFP' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                RFP.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": RFP}
    return render(request, 'proposal.html', ctx)


def RFP_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")

    # Responding to Tender
    vendNo = '01254796'
    procurementMethod = 1
    docNo = pk
    notify = ''
    unitPrice = ''
    if request.method == "POST":
        unitPrice = int(request.POST.get('amount'))
    try:
        r = session.get(Access2).json()
        response = session.get(Access_Point, timeout=9).json()
        RFP = []
        Doc = []
        for tender in response['value']:
            if tender['Process_Type'] == 'RFP':
                output_json = json.dumps(tender)
                RFP.append(json.loads(output_json))
                for my_tender in RFP:
                    if my_tender['No'] == pk:
                        res = my_tender
        for docs in r['value']:
            if docs['QuoteNo'] == pk:
                output_json = json.dumps(docs)
                Doc.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)
    try:
        if vendNo != '' and unitPrice != '':
            result = config.CLIENT.service.FnCreateProspectiveSupplier(
                vendNo, procurementMethod, docNo, unitPrice)
            notify = f"You have successfully Applied for RFQ {docNo}"

        else:
            raise ValueError('Incorrect input!')
    except Exception as e:
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res,
           "docs": Doc, "note": notify}
    return render(request, "PDetails.html", ctx)
