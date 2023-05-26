
from django.shortcuts import redirect, render
from django.conf import settings as config
import requests
from django.contrib import messages
from myRequest.views import UserObjectMixin
from django.views import View
# Create your views here.


class Profile(UserObjectMixin, View):
    def get(self, request):
        UserId = request.session['UserId']
        name = request.session['FullName']
        states = request.session['state']
        email=request.session['Email']
        ctx = {
            'UserId': UserId,
            'fullname': name,
            'email':email,
        }
        return render(request, 'profile.html', ctx)


def profile_request(request):
    return render(request, 'profile.html')


class login_request(UserObjectMixin, View):
    def get(self, request):

        ctx = {

        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        if request.method == 'POST':
            try:
                email = request.POST.get('email')
                password = request.POST.get('password')

                vendors = self.one_filter(
                    "/VendorDetails", "EMail", "eq", email)

                for vendor in vendors[1]:
                    if vendor['EMail'] == email:
                        print("Vendor")
                        if self.pass_decrypt(vendor['Password']) == password:
                            request.session['UserId'] = vendor['No']
                            request.session['FullName'] = vendor['Name']
                            request.session['Email'] = vendor['EMail']
                            print(request.session['Email'])
                            request.session['state'] = "Vendor"
                            return redirect('dashboard')
                        messages.success(request, 'Logged in Succesfully')

                        messages.error(
                            request, "Invalid Credentials. Please reset your password else create a new account")
                        return redirect('login')

                prospect = self.one_filter(
                    "/ProspectiveSupplier", "Email", "eq", email)

                for prospect in prospect[1]:
                    if prospect['Email'] == email and prospect['Verified'] == True:
                        print("Prospect")
                        if self.pass_decrypt(prospect['Password']) == password:
                            request.session['UserId'] = prospect['No']
                            request.session['FullName'] = prospect['Name']
                            request.session['Email'] = prospect['Email']
                            print(request.session['Email'])
                            request.session['state'] = "Prospect"
                            return redirect('dashboard')
                        messages.error(
                            request, "Invalid Credentials. Please reset your password else create a new account")
                        return redirect('login')
                messages.error(request, "User not Registered")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"{e}")
                print(e)
                return redirect('login')
        return redirect('login')


class FnResetPassword(UserObjectMixin, View):
    def post(self, request):
        if request.method == 'POST':
            try:
                emailAddress = request.POST.get('emailAddress')
                vendors = self.one_filter(
                    "/VendorDetails", "EMail", "eq", emailAddress)
                print(vendors)
                for users in vendors[1]:
                    if users['EMail'] == emailAddress:
                        request.session['resetMail'] = users['EMail']
                        email_subject = 'Password Reset'
                        email_template = 'resetMail.html'
                        recipient = users['Name']
                        recipient_email = users['EMail']
                        token = self.get_secret_code()
                        send_rest_mail = self.send_mail(request, email_subject, email_template,
                                                        recipient, recipient_email, token)
                        if send_rest_mail == True:
                            messages.success(
                                request, "We sent you an email to reset your password'")
                            return redirect('login')
                        messages.error(request, 'Reset failed contact admin')
                        return redirect('login')
                prospects = self.one_filter(
                    "/ProspectiveSupplier", "Email", "eq", emailAddress)
                print(prospects)
                for applicant in prospects[1]:
                    if applicant['Verified'] == True:
                        request.session['resetMail'] = applicant['Email']
                        email_subject = 'Password Reset'
                        email_template = 'resetMail.html'
                        recipient = applicant['Name']
                        recipient_email = applicant['Email']
                        token = self.get_secret_code()
                        send_reset_mail = self.send_mail(request, email_subject, email_template,
                                                         recipient, recipient_email, token)
                        if send_reset_mail == True:
                            messages.success(
                                request, 'We sent you an email to reset your password')
                            return redirect('login')
                        messages.error(request, 'Reset failed contact admin')
                        return redirect('login')
                    messages.error(request, 'Reset failed, email not verified')
                    return redirect('login')
                messages.error(request, 'Reset failed, email not registered')
                return redirect('login')
            except Exception as e:
                print(e)
                messages.error(request, f'{e}')
        return redirect('login')


class reset_request(UserObjectMixin, View):
    def get(self, request):
        return render(request, 'reset.html')

    def post(self, request):
        if request.method == 'POST':
            try:
                email = request.session['resetMail']
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

                if len(password) < 6:
                    messages.error(
                        request, "Password should be at least 6 characters")
                    return redirect('reset_request')
                if password != password2:
                    messages.error(request, "Password mismatch")
                    return redirect('reset_request')

                myPassword = self.pass_encrypt(password)

                response = self.zeep_client().service.FnResetVendorPassword(
                    email, myPassword, self.get_secret_code())
                if response == True:
                    messages.success(request, "Reset successful")
                    del request.session['resetMail']
                    return redirect('login')
                messages.error(request, f"{response}")
                return redirect('reset_request')

            except Exception as e:
                messages.info(request, f'{e}')
                print(e)
                return redirect('reset_request')
        return redirect('reset_request')


class verify_user(UserObjectMixin, View):
    def get(self, request):
        return render(request, 'verify.html')

    def post(self, request):
        if request.method == 'POST':
            try:
                email = request.POST.get('email')
                secret = request.POST.get('secret')
                verified = True
                prospect_users = self.one_filter("/ProspectiveSupplier",
                                                 "Email", "eq", email)
                for user in prospect_users[1]:
                    if user['Verification_Token'] == secret:
                        response = self.zeep_client().service.FnVerifiedProspectiveSupplier(verified, email)
                        if response == True:
                            messages.success(
                                request, "Verification Successful")
                            return redirect('login')
                        messages.error(request, "Verification Failed")
                        return redirect('verify')
                    messages.error(request, "Wrong Secret Code")
                    return redirect('verify')
                messages.error(request, "Wrong Email")
                return redirect('verify')
            except Exception as e:
                print(e)
                messages.error(request, f"{e}")
                return redirect('verify')
        return redirect('verify')


class register_request(UserObjectMixin, View):
    def get(self, request):
        try:
            session = requests.Session()
            session.auth = config.AUTHS
            citizenship = config.O_DATA.format("/CountryRegion")
            response = self.get_object(citizenship)
            country = response['value']
            ctx = {"country": country}
        except Exception as e:
            print(e)
            messages.error(request, f"{e}")
            return redirect('register')
        return render(request, "register.html", ctx)

    def post(self, request):
        if request.method == 'POST':
            try:
                prospNo = request.POST.get('prospNo')
                supplierName = request.POST.get('supplierName')
                supplierMail = request.POST.get('supplierMail')
                countryRegionCode = request.POST.get('countryRegionCode')
                postalAddress = request.POST.get('postalAddress')
                postCode = request.POST.get('postCode')
                city = request.POST.get('city')
                contactPersonName = request.POST.get('contactPersonName')
                contactPhoneNo = request.POST.get('contactPhoneNo')
                contactMail = request.POST.get('contactMail')
                Password = request.POST.get('myPassword')
                confirm_password = request.POST.get('confirm_password')
                myAction = request.POST.get('myAction')

                if len(Password) < 6:
                    messages.error(
                        request, "Password should be at least 6 characters")
                    return redirect('register')
                if Password != confirm_password:
                    messages.error(request, "Password mismatch")
                    return redirect('register')
                token = self.get_secret_code()
                response = self.zeep_client().service.FnProspectiveSupplierSignup(
                    prospNo, supplierName, supplierMail, countryRegionCode, postalAddress,
                    postCode, city, contactPersonName, contactPhoneNo, contactMail,
                    self.pass_encrypt(Password), token, myAction
                )
                if response == True:
                    email_subject = 'Activate your account'
                    email_template = 'activate.html'
                    recipient = supplierName
                    recipient_email = supplierMail
                    token = token
                    send_verification_mail = self.send_mail(
                        request, email_subject, email_template,
                        recipient, recipient_email, token
                    )
                    if send_verification_mail == True:
                        messages.success(
                            request, "We sent you an email to verify your account")
                        return redirect('login')
            except Exception as e:
                print(e)
                messages.error(request, f'{e}')
                return redirect('register')


def logout(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('login')
