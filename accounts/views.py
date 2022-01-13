from django.http import response
from django.shortcuts import render, HttpResponse
from django.conf import settings as config
import json
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import datetime
# Create your views here.


def profile_request(request):

    return render(request, 'profile.html')


def login_request(request):
    '''
    In order to catch exception well, make sure to know what every attribute contains
    '''
    vendNo = '01254796'
    procurementMethod = 1
    docNo = 'TDR-0000012'
    unitPrice = 6000
    try:
        if vendNo != '' and unitPrice != '':
            result = config.CLIENT.service.FnCreateProspectiveSupplier(
                vendNo, procurementMethod, docNo, unitPrice)
            print(result)
            notify = "Successfully Added"
        else:
            raise ValueError('Incorrect input!')
    except Exception as e:
        notify = e
    ctx = {"note": notify}
    return render(request, 'auth.html', ctx)
