from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile_request, name="profile"),
    path('', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('activate/<str:uidb64>', views.activate_user, name='activate'),
    path('FnResetPassword', views.FnResetPassword, name='FnResetPassword'),
]
