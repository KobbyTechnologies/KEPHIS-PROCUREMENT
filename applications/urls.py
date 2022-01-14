from django.urls import path
from . import views

urlpatterns = [
    path('SubOpenTenders', views.submittedOpenTenders, name="sub_open"),
    path('SubResTenders', views.submittedResTenders, name="sub_res"),
    path('SubRFQ', views.submittedRFQ, name="sub_rfq"),
    path('SubInterest', views.submittedInterest, name="sub_int"),
    path('SubRFP', views.submittedRFP, name="sub_rfp"),
    path('APPDETAILS/<str:pk>', views.APP_Details, name="APP"),
]
