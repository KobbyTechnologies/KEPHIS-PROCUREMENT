from django.urls import path

from . import views

urlpatterns = [
     path('openTenders', views.OpenTenders.as_view(), name="open"),
     path('openTenders-supplier/<str:pk>', views.EvaluationDetails.as_view(), name="evaluation"),
     path('restrictedTenders', views.Restricted_tenders, name='restricted'),
     path('Odetails/<str:pk>', views.Open_Details, name="Odetails"),
     path('DocResponse/<str:pk>', views.DocResponse, name="DocResponse"),

     path('submitted/<str:pk>', views.submitted, name="submit"),

     path('fnInsertSuppliersToProcurementMethod/<str:pk>', 
         views.fnInsertSuppliersToProcurementMethod, name='fnInsertSuppliersToProcurementMethod'),
    
     path('fnCreateprospectiveSupplierTender/<str:pk>', 
         views.fnCreateprospectiveSupplierTender, name='fnCreateprospectiveSupplierTender'),

     path('FnUploadProspectiveLineAttachedDocument/<str:pk>', 
         views.FnUploadProspectiveLineAttachedDocument, name='FnUploadProspectiveLineAttachedDocument'),

    path('DeleteDocumentttachment/<str:pk>', views.DeleteDocumentttachment, name='DeleteDocumentttachment'),

     path('fnCreateProspectiveTenderLine/<str:pk>', views.fnCreateProspectiveTenderLine, name='fnCreateProspectiveTenderLine'),
     path('fnModifyProspectiveTenderLine/<str:pk>', views.fnModifyProspectiveTenderLine, name='fnModifyProspectiveTenderLine'),
]
