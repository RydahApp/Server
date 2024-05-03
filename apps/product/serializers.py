from rest_framework import serializers
from .models import ProductModel
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'
    
    def get(self, request, format=None):
        product = ProductModel.objects.all()

        return Response(
            {"data": self.serializer_class(product, many=True).data}, 
            status=status.HTTP_200_OK
            )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
            )
    
   
    

   