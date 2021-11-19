from django.shortcuts import render

# Create your views here.


def interest_request(request):
    return render(request, 'interest.html')
