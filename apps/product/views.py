from rest_framework.generics import GenericAPIView
from .serializers import ProductModelSerializer
from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import ProductModel

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductModelSerializer
    queryset = ProductModel.objects.all()
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = ProductModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Product Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   

  
