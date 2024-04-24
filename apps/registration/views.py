from rest_framework import generics, status, permissions
from .models import User
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
            sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_KEY'))
            message = Mail(
            from_email='rydah2024@gmail.com',  # Sender's email address
            to_emails=f"lasisihabeeb67@gmail.com",  # Recipient's email address
            subject="Congratulations! You're Successfully Registered",
            html_content=f"<p>Dear User,</p><p>We are thrilled to inform you that your registration on Rydah E-commerce. We look forward to working together to achieve great things!</p><p>Best regards</p>")  # Email content (HTML supported)

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