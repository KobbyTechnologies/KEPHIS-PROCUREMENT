from django.shortcuts import render, redirect
from . models import Photo
from datetime import date

# Create your views here.


def canvas(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for image in images:
            photo = Photo.objects.create(
                image=image,
            )
        return redirect('main')
    return render(request, 'offcanvas.html')


def dashboard(request):

    # creating date object
    todays_date = date.today().year
    photo = Photo.objects.all()
    ctx = {"photo": photo, "today": todays_date}
    return render(request, 'main/dashboard.html', ctx)
