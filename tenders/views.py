from django.shortcuts import render, redirect
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime
from requests.adapters import HTTPAdapter

# Create your views here.


def open_tenders(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        open = []
        for tender in response['value']:
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                open.append(json.loads(output_json))
                res = open

    except requests.exceptions.ConnectionError as e:
        print(e)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res}
    return render(request, 'openTenders.html', ctx)


def Open_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")

    # Responding to Tender
    vendNo = '01254796'
    procurementMethod = 1
    docNo = pk
    notify = ''
    warn = ''
    Price = int()
    if request.method == "POST":
        Price = int(request.POST.get('amount'))
    unitPrice = float(Price)
    try:
        r = session.get(Access2, timeout=7).json()
        response = session.get(Access_Point, timeout=8).json()
        Open = []
        Doc = []
        for tender in response['value']:
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender' and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                Open.append(json.loads(output_json))
                responses = Open
                for my_tender in responses:
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
            notify = f"You have successfully Applied for tender number {docNo}"

        else:
            raise ValueError('Incorrect input!')
    except Exception as e:
        warn = e
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res,
           "docs": Doc, "warn": warn, "note": notify}
    return render(request, "details/open.html", ctx)


def Restricted_tenders(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=10).json()
        Restrict = []
        for tender in response['value']:
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == "Restricted Tender" and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                Restrict.append(json.loads(output_json))
                res = Restrict
    except requests.exceptions.ConnectionError as e:
        print(e)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res}
    return render(request, 'restrictedTenders.html', ctx)


def Restrict_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")

    # Responding to Tender
    vendNo = '01254796'
    procurementMethod = 1
    docNo = pk
    notify = ''
    if request.method == "POST":
        unitPrice = int(request.POST.get('amount'))

    try:
        r = session.get(Access2, timeout=7).json()
        response = session.get(Access_Point, timeout=9).json()
        Restrict = []
        Doc = []
        for tender in response['value']:
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == "Restricted Tender" and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                Restrict.append(json.loads(output_json))
                for my_tender in Restrict:
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
            notify = f"You have successfully Applied for tender number {docNo}"

        else:
            raise ValueError('Incorrect input!')
    except Exception as e:
        warn = f'You have already applied for tender number  {docNo}'
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res,
           "docs": Doc, "warn": warn, "note": notify}
    return render(request, "details/RES.html", ctx)
