from django.urls import path
from .views import  ViewProduct, ProductCreateView

urlpatterns = [
    path('view-product/',  ViewProduct.as_view()),
    path('create-product/', ProductCreateView.as_view()),

    

]
