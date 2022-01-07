from django.shortcuts import render, redirect
from . models import Photo
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime

# Create your views here.


def canvas(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for image in images:
            photo = Photo.objects.create(
                image=image,
            )
        return redirect('main')
    return render(request, 'offcanvas.html')


def dashboard(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")

    try:
        response = session.get(Access_Point).json()
        rfp = []
        open = []
        restricted = []
        rfq = []
        EOI = []
        for tender in response['value']:
            if tender['Process_Type'] == 'RFP':
                output_json = json.dumps(tender)
                rfp.append(json.loads(output_json))
                res = rfp

            elif tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender':
                output_json = json.dumps(tender)
                open.append(json.loads(output_json))
            elif tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Restricted Tender':
                output_json = json.dumps(tender)
                restricted.append(json.loads(output_json))
            elif tender['Process_Type'] == 'RFQ':
                output_json = json.dumps(tender)
                rfq.append(json.loads(output_json))
            elif tender['Process_Type'] == 'EOI':
                output_json = json.dumps(tender)
                EOI.append(json.loads(output_json))

        rfp_counter = len(rfp)
        open_counter = len(open)
        restricted_counter = len(restricted)
        rfq_counter = len(rfq)
        eoi_counter = len(EOI)

    except Exception as e:
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    photo = Photo.objects.all()
    ctx = {"photo": photo, "today": todays_date,
           "res": res, "open": open_counter, "restrict": restricted_counter, "rfq": rfq_counter, "EOI": eoi_counter, "RFP": rfp_counter}
    return render(request, 'main/dashboard.html', ctx)


def RFP_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")
    try:
        r = session.get(Access2).json()
        response = session.get(Access_Point).json()
        RFP = []
        Doc = []
        for tender in response['value']:
            if tender['Process_Type'] == 'RFP':
                output_json = json.dumps(tender)
                RFP.append(json.loads(output_json))
                responses = RFP
                for my_tender in responses:
                    if my_tender['No'] == pk:
                        res = tender
        for docs in r['value']:
            if docs['QuoteNo'] == pk:
                output_json = json.dumps(docs)
                Doc.append(json.loads(output_json))
                my_doc = Doc
    except Exception as e:
        print(e)

    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": res, "docs": my_doc}
    return render(request, "main/r-details.html", ctx)
