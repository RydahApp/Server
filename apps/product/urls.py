from django.urls import path
from .views import  *

urlpatterns = [
    path('catogories/',  CategoryAPIView.as_view()),
    path('product_image/<int:product_id>/',  ProductImageAPIView.as_view()),
    path('product/',  ProductModelAPIView.as_view()),
    path("product/search/", ProductSearchAPIView.as_view()),

    # path('create-product/', ProductCreateView.as_view()),

    

]
