from django.urls import path
from . import views

urlpatterns = [
    path('dash', views.dashboard, name="dashboard"),
    path('canvas', views.canvas, name="canvas"),
    path('details/<str:pk>', views.RFP_Details, name="r-details")

]
