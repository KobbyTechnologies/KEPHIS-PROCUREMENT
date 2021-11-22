from django.shortcuts import render

# Create your views here.


def profile_request(request):
    return render(request, 'profile.html')


def login_request(request):
    return render(request, 'auth.html')
