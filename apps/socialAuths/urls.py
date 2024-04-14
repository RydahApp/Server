from django.urls import path
from .views import *
urlpatterns = [
    path('google_register/', GoogleSignupSocialAuthView.as_view()),
    path('google_login/', GoogleLoginSocialAuthView.as_view())
]