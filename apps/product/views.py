from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ProductModel
from rest_framework.views import APIView

   
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

