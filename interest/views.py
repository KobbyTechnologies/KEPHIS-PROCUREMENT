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


def interest_request(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        OpenEOI = []
        Submitted = []
        for tender in response['value']:
            if tender['Process_Type'] == 'EOI' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                OpenEOI.append(json.loads(output_json))
            if tender['Process_Type'] == 'EOI' and tender['Status'] == 'Archived':
                output_json = json.dumps(tender)
                Submitted.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)

    count = len(OpenEOI)
    counter = len(Submitted)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": OpenEOI,
           "count": count, "sub": Submitted, "counter": counter}
    return render(request, 'interest.html', ctx)


def EOI_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")

    # Responding to Tender
    vendNo = '01254796'
    procurementMethod = 4
    docNo = pk
    unitPrice = ''
    if request.method == "POST":
        try:
            unitPrice = float(request.POST.get('amount'))
            messages.success(
                request, f"You have successfully Applied for EOI {docNo}")
        except ValueError:
            messages.error(request, "Invalid Amount, Try Again!!")
            return redirect('EOI', pk=docNo)

    try:
        r = session.get(Access2, timeout=7).json()
        response = session.get(Access_Point, timeout=9).json()
        EOI = []
        Doc = []
        for tender in response['value']:
            if tender['Process_Type'] == 'EOI' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                EOI.append(json.loads(output_json))
                for my_tender in EOI:
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
            return redirect('EOI', pk=docNo)
    except Exception as e:
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res,
           "docs": Doc}
    return render(request, "EDetails.html", ctx)
