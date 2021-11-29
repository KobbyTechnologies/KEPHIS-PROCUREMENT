from django.http import response
from django.shortcuts import render, HttpResponse
from django.conf import settings as config
import json
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth

# Create your views here.


def profile_request(request):

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
            notify = "Successfully Added"
        else:
            raise ValueError('Incorrect input!')
    except Exception as e:
        notify = e
    ctx = {"note": notify}
    return render(request, 'auth.html', ctx)
