from django.urls import path
from . import views

urlpatterns = [
    path('Proposal', views.proposal_request, name="proposal"),
    path('RFP/<str:pk>', views.RFP_Details, name="RFP"),
]
