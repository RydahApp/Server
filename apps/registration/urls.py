from django.urls import path
from .views import RegisterView

app_name = "apps.registration"


urlpatterns = [
    path('register/', RegisterView.as_view(), name="user_register"),
]