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

    return render(request, 'auth.html')
