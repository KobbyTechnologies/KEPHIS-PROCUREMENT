from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.Profile.as_view(), name="profile"),
    path('', views.login_request.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register_request.as_view(), name='register'),
    path('verify', views.verify_user.as_view(), name='verify'),
    path('FnResetPassword', views.FnResetPassword.as_view(), name='FnResetPassword'),
    path("reset/request", views.reset_request.as_view(),name='reset_request'),
]
