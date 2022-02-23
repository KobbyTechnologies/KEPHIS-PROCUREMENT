from django.shortcuts import render, redirect
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime
from django.contrib import messages


# Create your views here.


def requestQuote(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        OpenRFQ = []
        Submitted = []
        for tender in response['value']:
            if tender['Process_Type'] == 'RFQ' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                OpenRFQ.append(json.loads(output_json))
            if tender['Process_Type'] == 'RFQ' and tender['Status'] == 'Archived':
                output_json = json.dumps(tender)
                Submitted.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)

    count = len(OpenRFQ)
    counter = len(Submitted)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": OpenRFQ,
           "count": count, "counter": counter, "sub": Submitted}
    return render(request, 'requestQuote.html', ctx)


def Quote_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")

    # Responding to Tender
    vendNo = '01254796'
    procurementMethod = 2
    docNo = pk
    unitPrice = ''
    if request.method == "POST":
        try:
            unitPrice = float(request.POST.get('amount'))
            messages.success(
                request, f"You have successfully Applied for RFQ {docNo}")
        except ValueError:
            messages.error(request, "Invalid Amount, Try Again!!")
            return redirect('QDetails', pk=docNo)
    try:
        r = session.get(Access2, timeout=7).json()
        response = session.get(Access_Point, timeout=9).json()
        RFQ = []
        Doc = []
        for tender in response['value']:
            if tender['Process_Type'] == 'RFQ' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                RFQ.append(json.loads(output_json))
                for my_tender in RFQ:
                    if my_tender['No'] == pk:
                        res = my_tender
        for docs in r['value']:
            if docs['QuoteNo'] == pk:
                output_json = json.dumps(docs)
                Doc.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)
    try:
        if vendNo != '':
            result = config.CLIENT.service.FnCreateProspectiveSupplier(
                vendNo, procurementMethod, docNo, unitPrice)
            print(result)
            return redirect('QDetails', pk=docNo)
    except Exception as e:
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res,
           "docs": Doc}
    return render(request, "QDetails.html", ctx)
