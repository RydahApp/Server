from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_KEY'))
fr = os.environ.get('SENDER_EMAIL')##changed
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

def RegisterEmailMessage(to, otp):
    message = Mail(
    from_email=fr,  # Sender's email address
    to_emails=to,  # Recipient's email address
    subject="Email Verification Code",
    html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Kindly use the code below to verify your account.</p><p><h2>{otp}</h2> </p><p>Best regards</p>") # Email content (HTML supported)

    try:
        # Send the email
        response = sg.send(message)
        print("Email sent successfully!")
        print(response.status_code)
    except Exception as e:
        print("Error sending email.")
        print(e)

def ResendOTPEmailMessage(to, otp):
    message = Mail(
    from_email=fr,  # Sender's email address
    to_emails=to,  # Recipient's email address
    subject="Email Verification Code Resent!",
    html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Kindly use the code below to verify your account.</p><p><h2>{otp}</h2> </p><p>Best regards</p>") # Email content (HTML supported)

    try:
        # Send the email
        response = sg.send(message)
        print("Email sent successfully!")
        print(response.status_code)
    except Exception as e:
        print("Error sending email.")
        print(e) 

def ResetPasswordEmailMessage(to, otp):
    message = Mail(
    from_email=fr,  # Sender's email address
    to_emails=to,  # Recipient's email address
    subject="Email Reset Password Code!",
    html_content=f"<p>Dear User, Welcome to Rydah E-commerce</p><p>Kindly use the code below to reset your account password.</p><p><h2>{otp}</h2> </p><p>Best regards</p>") # Email content (HTML supported)

    try:
        # Send the email
        response = sg.send(message)
        print("Email sent successfully!")
        print(response.status_code)
    except Exception as e:
        print("Error sending email.")
        print(e) 

def PasswordResetSuccessEmail(to):
    message = Mail(
    from_email=fr,  # Sender's email address
    to_emails=to,  # Recipient's email address
    subject="Email Reset Password Successful!",
    html_content=f"<p>Dear User,</p><p>Your account password was reset successfully.</p><p>Best regards</p>") # Email content (HTML supported)

    try:
        # Send the email
        response = sg.send(message)
        print("Email sent successfully!")
        print(response.status_code)
    except Exception as e:
        print("Error sending email.")
        print(e) 