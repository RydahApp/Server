from django.urls import path
from .views import ProductCreateView, ProductEditView, ProductDeleteView

urlpatterns = [
    path('create-product/', ProductCreateView.as_view()),
    path('edit-product/<int:pk>/', ProductEditView.as_view()),
    path('delete-product/<int:pk>/', ProductDeleteView.as_view()),
]
