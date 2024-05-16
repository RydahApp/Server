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

class ViewProduct(APIView):
  def get(self, request):
    category = self.request.query_params.get('category')
    if category:
        queryset = ProductModel.objects.filter(category__category_name =  category)
    else:
        queryset = ProductModel.objects.all()
    serializer = ViewProductModelSerializer(queryset , many = True)
    return Response({'count' : len(serializer.data) ,'data' :serializer.data})

class ProductCreateView(generics.CreateAPIView):
  serializer_class = CreateProductModelSerializer
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
      serializer = CreateProductModelSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

