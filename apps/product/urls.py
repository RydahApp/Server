from django.urls import path
from .views import  *

urlpatterns = [
    path('catogories/',  CategoryAPIView.as_view()),
    path('product_image/<int:product_id>/',  ProductImageAPIView.as_view()),
    path('product/',  ProductModelAPIView.as_view()),
    path('product/details/<int:product_id>',  ProductModelDetailsAPIView.as_view()),
    path("product/search/", ProductSearchAPIView.as_view()),
    path("product/favourite/", UserFavouriteProductsAPIView.as_view()),
    path("product/review/", CustomerProductReviewAPIView.as_view()),
    path('product/review/<int:product_id>/',  ProductReviewAPIView.as_view()),
    # path('create-product/', ProductCreateView.as_view()),

    

]
