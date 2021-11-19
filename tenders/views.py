from django.shortcuts import render

# Create your views here.


def open_tenders(request):
    return render(request, 'openTenders.html')
