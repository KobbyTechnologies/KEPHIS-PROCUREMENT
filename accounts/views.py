from django.http import response
from django.shortcuts import render, HttpResponse
from django.conf import settings as config
import json
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import datetime
from datetime import date
# Create your views here.


def profile_request(request):

    return render(request, 'profile.html')


def login_request(request):
    todays_date = date.today()
    year = todays_date.year
    request.session['years'] = year
    print(request.session['years'])
    ctx = {"year": year}
    return render(request, 'auth.html', ctx)
