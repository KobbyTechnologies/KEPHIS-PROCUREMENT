from django.urls import path

from . import views

urlpatterns = [
    path('openTenders', views.open_tenders, name="open"),
    path('restrictedTenders', views.Restricted_tenders, name='restricted'),
    path('details/<str:pk>', views.details, name="details")
]
