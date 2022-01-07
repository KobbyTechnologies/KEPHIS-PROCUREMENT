from django.urls import path
from . import views

urlpatterns = [
    path('interest', views.interest_request, name='interest'),
    path('EOI/<str:pk>', views.EOI_Details, name="EOI"),
]
