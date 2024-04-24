from rest_framework import generics, status, permissions, views
from .models import User
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .otp import generateKey, verify_otp
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class HomeView(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]

# class RegisterView(generics.CreateAPIView):
#   queryset = User.objects.all()
#   serializer_class = RegisterSerializer
#   permission_classes = [AllowAny]

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    """
    API to register a user
    """
    def post(self, request):
        """
        Register a new user endpoint
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            user_otp = generateKey()
            user = User.objects.get(email=request.data.get('email'))
            user.otp = user_otp['OTP']
            user.activation_key = user_otp['totp']
            user.save()
            sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_KEY'))
            message = Mail(
            from_email='rydah2024@gmail.com',  # Sender's email address
            to_emails=user.email,  # Recipient's email address
            subject="Email Verification Code",
            html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Kindly use the code below to verify your account.</p><p><h2>{user_otp['OTP']}</h2> </p><p>Best regards</p>") # Email content (HTML supported)

            try:
                # Send the email
                response = sg.send(message)
                print("Email sent successfully!")
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print("Error sending email.")
                print(e)

            return Response({'message': "Registration Successful"}, status=status.HTTP_201_CREATED)
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
                sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_KEY'))
                message = Mail(
                from_email='rydah2024@gmail.com',  # Sender's email address
                to_emails=user.email,  # Recipient's email address
                subject="Email Verification Successful!",
                html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Email verified successfully.</p><p> </p><p>Best regards</p>") # Email content (HTML supported)

                try:
                    # Send the email
                    response = sg.send(message)
                    print("Email sent successfully!")
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print("Error sending email.")
                    print(e)
                return Response({'message': 'Email Verification Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({"message" : "Time Out, Given OTP is expired!!"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except:
            return Response({"message" : "Invalid OTP OR No any inactive user found for given otp"}, status=status.HTTP_400_BAD_REQUEST)
       
class ResendOTP(views.APIView):
    serializer_class = EmailResendOTPVerificationSerializer
    email_param_config = openapi.Parameter('email', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[email_param_config])
    def get(self, request):
        email = request.data["email"]
        try:
            user = User.objects.get(email = email)
            key = generateKey()
            user.otp = key['OTP']
            user.activation_key = key['totp']
            user.save(update_fields=['otp','activation_key'])
            sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_KEY'))
            message = Mail(
            from_email='rydah2024@gmail.com',  # Sender's email address
            to_emails=user.email,  # Recipient's email address
            subject="Email Verification Code Resent!",
            html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Kindly use the code below to verify your account.</p><p><h2>{key['OTP']}</h2> </p><p>Best regards</p>") # Email content (HTML supported)

            try:
                # Send the email
                response = sg.send(message)
                print("Email sent successfully!")
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print("Error sending email.")
                print(e)        
            return Response({"message" : "OTP successfully sent!"},status=status.HTTP_200_OK)
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