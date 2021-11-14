from django.shortcuts import render, redirect
from . models import Photo

# Create your views here.


def dashboard(request):

    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for image in images:
            photo = Photo.objects.create(
                image=image,
            )
    photo = Photo.objects.all()
    ctx = {"photo": photo}

    return render(request, 'main/dash.html', ctx)


def main_request(request):
    return render(request, 'main/main.html')
