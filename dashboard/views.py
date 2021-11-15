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
        return redirect('main')
    return render(request, 'main/dash.html')


def main_request(request):
    photo = Photo.objects.all()
    ctx = {"photo": photo}
    return render(request, 'main/main.html', ctx)
