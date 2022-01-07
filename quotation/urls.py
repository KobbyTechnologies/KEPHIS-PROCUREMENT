from django.urls import path
from . import views


urlpatterns = [
    path('quotation', views.requestQuote, name='quote'),
    path('Quote/<str:pk>', views.Quote_Details, name="QDetails"),

]
