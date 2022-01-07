from django.shortcuts import render, redirect
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime

# Create your views here.


def submittedOpenTenders(request):

    return render(request, 'Open/SubOpenTender.html')


def submittedResTenders(request):

    return render(request, 'SubResTender.html')


def submittedRFQ(request):

    return render(request, 'Sub-RFQ.html')


def submittedInterest(request):

    return render(request, 'SubInterest.html')
