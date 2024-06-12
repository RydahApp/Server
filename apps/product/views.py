from .serializers import *
from rest_framework import generics, status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ProductModel
from rest_framework.parsers import MultiPartParser
from rest_framework import filters

   
class CategoryAPIView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.all().order_by('created_at')
    
class ProductImageAPIView(generics.GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        images = ProductImage.objects.filter(product__id=product_id)
        serializer = ProductImageSerializer(images, many=True)
        result, images = {}, []
        for d in serializer.data:
            images.append(d['image'])
        result['images'] = images
        return Response(result)
    
    def post(self, request, product_id):
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            product = ProductModel.objects.get(id=product_id)
            serializer.save(seller=self.request.user, product=product)
            data = serializer.data
            data['status'] = "success"
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductModelAPIView(ListCreateAPIView):
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product = ProductModel.objects.filter(approve = True)
        return product
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductModelDetailsAPIView(generics.GenericAPIView):
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, product_id):
        product = ProductModel.objects.filter(id=product_id, approve=True)
        serializer = ProductModelSerializer(product, many=True)
        return Response(serializer.data)

class ProductSearchAPIView(ListAPIView):
    search_fields = ['name', 'brand', 'description', 'category__name']
    filter_backends = (filters.SearchFilter,)
    queryset = ProductModel.objects.filter(approve=True).order_by('-created_at')
    serializer_class = ListProductsSerializer
    permission_classes = [IsAuthenticated]

class UserFavouriteProductsAPIView(ListCreateAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product = UserFavouriteProducts.objects.filter(buyer = self.request.user)
        return product
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
    

class CustomerProductReviewAPIView(ListCreateAPIView):
    serializer_class = CustomerProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product = CustomerProductReview.objects.filter(product__seller = self.request.user)
        return product
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
    

class ProductReviewAPIView(generics.GenericAPIView):
    serializer_class = CustomerProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        images = CustomerProductReview.objects.filter(product__id=product_id)
        serializer = CustomerProductReviewSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)