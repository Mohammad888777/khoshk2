from django.urls import path
from . import views


urlpatterns=[
    path("",views.LoginView.as_view(),name="login"),
    path("verify/",views.VerifyView.as_view(),name="verify"),
    path("resend/",views.ResendOtp.as_view(),name="resend"),
]