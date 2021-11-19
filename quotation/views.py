from django.shortcuts import render

# Create your views here.


def requestQuote(request):
    return render(request, 'requestQuote.html')
