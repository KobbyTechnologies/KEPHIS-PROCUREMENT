from django.shortcuts import render, redirect
from . models import Photo
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config

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

    Access_Point = config.O_DATA.format("/UpcomingEvents")
    response = session.get(Access_Point).json()

    res = response['value']
    # creating date object
    todays_date = date.today().year
    photo = Photo.objects.all()
    ctx = {"photo": photo, "today": todays_date, "res": res}
    return render(request, 'main/dashboard.html', ctx)
