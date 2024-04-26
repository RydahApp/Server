from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .otp import generateKey, verify_otp
import os

sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_KEY'))
fr = ""
def VerifyEmailMessage(to):
    message = Mail(
    from_email=fr,  # Sender's email address
    to_emails=to,  # Recipient's email address
    subject="Email Verification Successful!",
    html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Email verified successfully.</p><p> </p><p>Best regards</p>") # Email content (HTML supported)

    try:
        # Send the email
        response = sg.send(message)
        print("Email sent successfully!")
        print(response.status_code)
    except Exception as e:
        print("Error sending email.")
        print(e)

def RegisterEmailMessage(to):
    message = Mail(
    from_email=fr,  # Sender's email address
    to_emails=to,  # Recipient's email address
    subject="Email Verification Code",
    html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Kindly use the code below to verify your account.</p><p><h2>{user_otp['OTP']}</h2> </p><p>Best regards</p>") # Email content (HTML supported)

    try:
        # Send the email
        response = sg.send(message)
        print("Email sent successfully!")
        print(response.status_code)
    except Exception as e:
        print("Error sending email.")
        print(e)

def ResendOTPEmailMessage(to):
    message = Mail(
    from_email=fr,  # Sender's email address
    to_emails=to,  # Recipient's email address
    subject="Email Verification Code Resent!",
    html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Kindly use the code below to verify your account.</p><p><h2>{key['OTP']}</h2> </p><p>Best regards</p>") # Email content (HTML supported)

    try:
        # Send the email
        response = sg.send(message)
        print("Email sent successfully!")
        print(response.status_code)
    except Exception as e:
        print("Error sending email.")
        print(e) 