from django.urls import path
from .views import *

app_name = "apps.registration"


urlpatterns = [
    path('home/', HomeView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
]