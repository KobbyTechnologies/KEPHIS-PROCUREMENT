from django.http import response
from django.shortcuts import render, HttpResponse
from django.conf import settings as config
import json
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth

# Create your views here.


def profile_request(request):

    session = requests.Session()
    session.auth = HttpNtlmAuth('domain\\fke-admin', 'Administrator#2021!')
    response = session.get(
        "http://102.37.117.22:1448/ADMINBC/ODataV4/Company('FKETEST')/UpcomingEvents").json()

    print(response)
    return render(request, 'profile.html')


def login_request(request):
    '''
    In order to catch exception well, make sure to know what every attribute contains
    '''
    customerNo = '01-00334545'
    eventNo = 'ev00030344'
    RegNo = 'null'
    try:
        if customerNo != '' and eventNo != '':
            result = config.CLIENT.service.RegisterEvent(
                customerNo, eventNo, RegNo)
            print(result)
        else:
            raise ValueError('Incorrect input!')
    except Exception:
        return HttpResponse("You have already registered for this event! View the details under the My Events Section.")
    return render(request, 'auth.html')
