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
        for tender in response['value']:
            if tender['Process_Type'] == 'RFP':
                output_json = json.dumps(tender)
                rfp.append(json.loads(output_json))
                res = rfp

            elif tender['Process_Type'] == 'Tender':
                output_json = json.dumps(tender)
                open.append(json.loads(output_json))
        rfp_counter = len(rfp)
        open_counter = len(open)
    except Exception as e:
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    photo = Photo.objects.all()
    ctx = {"photo": photo, "today": todays_date,
           "res": res, "open": open_counter}
    return render(request, 'main/dashboard.html', ctx)
