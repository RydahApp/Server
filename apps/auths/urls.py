from django.urls import path
from .views import *

app_name = "apps.auths"


urlpatterns = [
    # path('home/', HomeView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-otp-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('email-resend-otp-verify/', ResendOTP.as_view(), name="email-verify"),
    path('reset-password-request/', RequestResetPasswordView.as_view(), name="reset-request-pass"),
    path('reset-verify-otp/', VerifyEmail.as_view(), name="reset-verify-pass"),
    path('reset-set-new-password/', SetResetPasswordAPIView.as_view(), name="reset-set-new-pass"),
    path('create-userprofile/', UserProfileAPIView.as_view(), name="userprofile"),
]