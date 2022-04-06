import base64
import threading
from django.http import response
from django.shortcuts import redirect, render, HttpResponse
from django.conf import settings as config
import json
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import datetime
from django.urls import reverse
from datetime import date
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from . models import Users
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str, DjangoUnicodeDecodeError
import secrets
import string
from cryptography.fernet import Fernet
# Create your views here.


def profile_request(request):

    return render(request, 'profile.html')


def login_request(request):
    todays_date = date.today()
    year = todays_date.year
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/VendorDetails")
    Access = config.O_DATA.format("/ProspectiveSupplier")
    decoded_text = ''
    vendorNo = ""
    state = ""
    ProspectNo = ""
    request.session['years'] = year
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
        except ValueError:
            print("Invalid credentials, try again")
            return redirect('login')
        try:
            response = session.get(Access_Point, timeout=10).json()
            res = session.get(Access, timeout=10).json()
            for applicant in response['value']:
                if applicant['EMail'] == email:
                    Portal_Password = base64.urlsafe_b64decode(
                        applicant['SerialID'])
                    request.session['vendorNo'] = applicant['No']
                    vendorNo = request.session['vendorNo']

                    state = "Vendor"
                    cipher_suite = Fernet(config.ENCRYPT_KEY)
                    try:
                        decoded_text = cipher_suite.decrypt(
                            Portal_Password).decode("ascii")
                    except Exception as e:
                        print(e)
                    if decoded_text == password:
                        request.session['state'] = state
                        states = request.session['state']
                        return redirect('dashboard')
                    else:
                        messages.error(
                            request, "Invalid Credentials. Please reset your password else create a new account")
                        return redirect('login')
            for applicant in res['value']:
                if applicant['Verification_Token'] and applicant['Email'] == email:
                    Portal_Password = base64.urlsafe_b64decode(
                        applicant['SerialID'])
                    request.session['ProspectNo'] = applicant['No']
                    ProspectNo = request.session['ProspectNo']
                    state = "Prospect"
                    cipher_suite = Fernet(config.ENCRYPT_KEY)
                    try:
                        decoded_text = cipher_suite.decrypt(
                            Portal_Password).decode("ascii")
                    except Exception as e:
                        print(e)
                    if decoded_text == password:
                        request.session['state'] = state
                        states = request.session['state']
                        return redirect('dashboard')
                    else:
                        messages.error(
                            request, "Invalid Credentials. Please reset your password else create a new account")
                        return redirect('login')

        except requests.exceptions.ConnectionError as e:
            messages.error(
                request, "If you are a vendor please reset your password else create a new account")
            print(e)

    ctx = {"year": year}
    return render(request, 'login.html', ctx)


def FnResetPassword(request):
    alphabet = string.ascii_letters + string.digits
    SecretCode = ''.join(secrets.choice(alphabet) for i in range(5))
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/VendorDetails")
    Access = config.O_DATA.format("/ProspectiveSupplier")

    emailAddress = ""
    password = ""
    confirm_password = ''
    verificationToken = SecretCode
    if request.method == 'POST':
        try:
            emailAddress = request.POST.get('emailAddress')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
        except ValueError:
            print("Invalid credentials, try again")
            return redirect('login')
        if len(password) < 6:
            messages.error(request, "Password should be at least 6 characters")
            return redirect('login')
        if password != confirm_password:
            messages.error(request, "Password mismatch")
            return redirect('login')
        try:
            response = session.get(Access_Point, timeout=10).json()
            res = session.get(Access, timeout=10).json()
            for applicant in response['value']:
                if applicant['EMail'] == emailAddress:
                    cipher_suite = Fernet(config.ENCRYPT_KEY)
                    try:
                        encrypted_text = cipher_suite.encrypt(
                            password.encode('ascii'))
                        password = base64.urlsafe_b64encode(
                            encrypted_text).decode("ascii")
                        response = config.CLIENT.service.FnResetPassword(
                            emailAddress, password, verificationToken)
                        print(response)
                        messages.success(
                            request, "Reset was successful, now login")
                        return redirect('login')
                    except Exception as e:
                        messages.error(request, e)
                        return redirect('login')
            for applicant in res['value']:
                if applicant['Email'] == emailAddress:
                    cipher_suite = Fernet(config.ENCRYPT_KEY)
                    try:
                        encrypted_text = cipher_suite.encrypt(
                            password.encode('ascii'))
                        password = base64.urlsafe_b64encode(
                            encrypted_text).decode("ascii")
                        response = config.CLIENT.service.FnResetPassword(
                            emailAddress, password, verificationToken)
                        print(response)
                        messages.success(
                            request, "Reset was successful, now login")
                        return redirect('login')
                    except Exception as e:
                        messages.error(request, e)
                        return redirect('login')
        except requests.exceptions.ConnectionError as e:
            messages.error(
                request, "If you are a vendor please reset your password else create a new account")
            print(e)
    return redirect('login')


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def activate_user(request, uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = "Enock"
    except Exception as e:
        user = None
    if user:
        messages.success(
            request, "Email verified, you can now login")
        return redirect(reverse('login'))
    return render(request, 'activate-failed.html')


def register_request(request):
    todays_date = date.today()
    year = todays_date.year
    session = requests.Session()
    session.auth = config.AUTHS

    citizenship = config.O_DATA.format("/CountryRegion")
    try:
        response = session.get(citizenship, timeout=10).json()
        country = response['value']
    except requests.exceptions.ConnectionError as e:
        print(e)
    alphabet = string.ascii_letters + string.digits
    SecretCode = ''.join(secrets.choice(alphabet) for i in range(5))

    prospNo = ""
    supplierName = " "
    supplierMail = ""
    countryRegionCode = ""
    postalAddress = ""
    postCode = ""
    city = ""
    contactPersonName = ""
    contactPhoneNo = ""
    contactMail = ""
    myPassword = ""
    confirm_password = ''
    verificationToken = SecretCode
    myAction = "insert"

    if request.method == "POST":
        try:
            supplierName = request.POST.get('supplierName')
            supplierMail = request.POST.get('supplierMail')
            countryRegionCode = request.POST.get('countryRegionCode')
            postalAddress = request.POST.get('postalAddress')
            postCode = request.POST.get('postCode')
            city = request.POST.get('city')
            contactPersonName = request.POST.get('contactPersonName')
            contactPhoneNo = request.POST.get('contactPhoneNo')
            contactMail = request.POST.get('contactMail')
            Password = str(request.POST.get('myPassword'))
            confirm_password = str(request.POST.get('confirm_password'))
        except ValueError:
            messages.error(request, "Invalid credentials, try again")
            return redirect('register')
        if len(Password) < 6:
            messages.error(request, "Password should be at least 6 characters")
            return redirect('register')
        if Password != confirm_password:
            messages.error(request, "Password mismatch")
            return redirect('register')
        cipher_suite = Fernet(config.ENCRYPT_KEY)

        encrypted_text = cipher_suite.encrypt(Password.encode('ascii'))
        myPassword = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        try:
            response = config.CLIENT.service.FnProspectiveSupplierSignup(
                prospNo, supplierName, supplierMail, countryRegionCode, postalAddress, postCode, city, contactPersonName, contactPhoneNo, contactMail, myPassword, verificationToken, myAction)
            print(response)
            if response == True:
                current_site = get_current_site(request)
                email_subject = 'Activate your account'
                email_body = render_to_string('activate.html', {
                    "user": supplierName,
                    "domain": current_site,
                    'uid': urlsafe_base64_encode(force_bytes(supplierName)),
                })
                email = EmailMessage(subject=email_subject, body=email_body,
                                     from_email=config.EMAIL_HOST_USER, to=[supplierMail])
                EmailThread(email).start()
                messages.success(
                    request, "We sent you an email to verify your account")
                return redirect('login')
            else:
                messages.error(
                    request, "Email not sent")
                return redirect('register')
        except Exception as e:
            print(e)
    ctx = {"year": year, "country": country, }
    return render(request, "register.html", ctx)
