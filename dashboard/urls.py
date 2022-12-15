from django.urls import path
from . import views

urlpatterns = [
    path('dash', views.dashboard.as_view(), name="dashboard"),
    path('canvas', views.canvas, name="canvas"),
]
