from rest_framework import generics, status, permissions, views
from .models import User
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .otp import generateKey, verify_otp
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import *
from django.contrib.auth import get_user_model
from rest_framework import viewsets

# Create your views here.

class HomeView(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """
    UserModel View.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response({'message': "auths Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(views.APIView):
    serializer_class = EmailOTPVerificationSerializer
    otp_param_config = openapi.Parameter('otp', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[otp_param_config])
    def get(self, request):
        otp = request.GET.get('otp')
        try:
            user = User.objects.get(otp=otp)
            verify = verify_otp(user.activation_key,otp)
            if verify:
                user.is_verified = True
                user.user_secret_key = generateKey()['totp']
                user.otp = None
                user.save()
                VerifyEmailMessage(user.email)
                return Response({'message': 'Verification Successful', 'email': user.email, 'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({"message" : "Time Out, Given OTP is expired!!"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except:
            return Response({"message" : "Invalid OTP OR No any inactive user found for given otp"}, status=status.HTTP_400_BAD_REQUEST)
       
class ResendOTP(views.APIView):
    serializer_class = EmailResendOTPVerificationSerializer
    email_param_config = openapi.Parameter('email', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[email_param_config])
    def get(self, request):
        email = request.GET.get("email")
        try:
            user = User.objects.get(email = email)
            key = generateKey()
            user.otp = key['OTP']
            user.activation_key = key['totp']
            user.save(update_fields=['otp','activation_key'])   
            ResendOTPEmailMessage(user.email, key['OTP'])    
            return Response({"message" : "OTP successfully resent!"},status=status.HTTP_200_OK)
        except:
            return Response({"message" : "No Inactive account found for this given email!!"}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RequestResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': "OTP Sent", "status": "success"}, status=status.HTTP_201_CREATED)
    

class SetResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

class UserProfileAPIView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
