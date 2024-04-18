from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import *

class GoogleSignupSocialAuthView(GenericAPIView):
    serializer_class = GoogleSignupSocialAuthSerializer
    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = ((serializer.validated_data)['auth_token'])
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GoogleLoginSocialAuthView(GenericAPIView):
    serializer_class = GoogleLoginSocialAuthSerializer
    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = ((serializer.validated_data)['auth_token'])
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)