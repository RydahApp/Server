from .serializers import *
from rest_framework import generics, status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ProductModel
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

   
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
