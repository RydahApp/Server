from django.urls import path
from .views import HomeView, RegisterView, LoginView, LogOutView

app_name = "apps.registration"


urlpatterns = [
    path('home/', HomeView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout")
]