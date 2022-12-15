from django.shortcuts import render
import requests
from django.conf import settings as config
from requests.auth import HTTPBasicAuth
from requests import Session
from zeep.client import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import secrets
import string
from cryptography.fernet import Fernet
import base64
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import date
from django.core.mail import EmailMessage
import datetime as dt
import threading

# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    cipher_suite = Fernet(config.ENCRYPT_KEY)
    todays_date = dt.datetime.now().strftime("%b. %d, %Y %A")
    

    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response
    
    def one_filter(self,endpoint,property,filter,field_name):

        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property}%20{filter}%20%27{field_name}%27")
        response = self.get_object(Access_Point)['value']
        count=len(response)
        return count,response
   
    def double_filtered_data(self,endpoint,property_x,filter_x,filed_name_x,operater_1,property_y,filter_y,field_name_y):

        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{filed_name_x}%27%20{operater_1}%20{property_y}%20{filter_y}%20%27{field_name_y}%27")
        response = self.get_object(Access_Point)['value']
        count=len(response)
        return count,response

    def zeep_client(self):
        AUTHS = Session()
        AUTHS.auth = HTTPBasicAuth(config.WEB_SERVICE_USER, config.WEB_SERVICE_PWD)
        CLIENT = Client(config.BASE_URL, transport=Transport(session=AUTHS))
        return CLIENT

    def comparison_double_filter(self,endpoint,property_x,filter_x,field_name,operater_1,property_y,filter_y,property_z):
        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property_x}%20{filter_x}%20%27{field_name}%27%20{operater_1}%20{property_y}%20{filter_y}%20{property_z}")
        response = self.get_object(Access_Point)['value'] 
        count=len(response)
        return count,response
    def logical_triple_filter(self,endpoint,property1,filter1,field_name1):
        Access_Point = config.O_DATA.format(f"{endpoint}?$filter={property1}%20{filter1}%20%27{field_name1}%27%20and%20SubmittedToPortal%20eq%20false")
        response = self.get_object(Access_Point)['value'] 
        count=len(response)
        return count,response

    def get_secret_code(self):
        alphabet = string.ascii_letters + string.digits
        SecretCode = ''.join(secrets.choice(alphabet) for i in range(5))
        return SecretCode
    def pass_encrypt(self,password):
        encrypted_text = self.cipher_suite.encrypt(password.encode('ascii'))
        encrypted_password = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_password
    def pass_decrypt(self,password):
        Portal_Password = base64.urlsafe_b64decode(password)
        decoded_text = self.cipher_suite.decrypt(Portal_Password).decode("ascii")
        return decoded_text

    def send_mail(self,request,subject,template,recipient,recipient_email,token):
        current_site = get_current_site(request)
        email_body = render_to_string(template, {
                    "user": recipient,
                    "domain": current_site,
                    'Secret': token,
                })
        email = EmailMessage(subject=subject, body=email_body,
                                     from_email=config.EMAIL_HOST_USER, to=[recipient_email])
        EmailThread(email).start()
        return True

    