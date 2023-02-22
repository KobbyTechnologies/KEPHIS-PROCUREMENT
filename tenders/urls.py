from django.urls import path

from . import views

urlpatterns = [
    path('openTenders', views.open_tenders, name="open"),
    path('restrictedTenders', views.Restricted_tenders, name='restricted'),
    path('Odetails/<str:pk>', views.Open_Details, name="Odetails"),
    path('DocResponse/<str:pk>', views.DocResponse, name="DocResponse"),
    path('UploadAttachedDocument/<str:pk>',
         views.UploadAttachedDocument, name="UploadAttachedDocument"),

    path('submitted/<str:pk>', views.submitted, name="submit"),

    path('fnInsertSuppliersToProcurementMethod/<str:pk>', 
         views.fnInsertSuppliersToProcurementMethod, name='fnInsertSuppliersToProcurementMethod'),
]
