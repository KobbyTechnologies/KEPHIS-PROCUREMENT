from django.shortcuts import render

# Create your views here.


def submittedOpenTenders(request):
    return render(request, 'SubOpenTender.html')


def submittedResTenders(request):
    return render(request, 'SubResTender.html')
