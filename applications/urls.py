from django.urls import path
from . import views

urlpatterns = [
    path('SubOpenTenders', views.submittedOpenTenders, name="sub_open"),
]
