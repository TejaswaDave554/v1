import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email_notification(to_email: str, subject: str, body: str):
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        sender_email = os.getenv('SENDER_EMAIL', 'noreply@chaalak.com')
        sender_password = os.getenv('SENDER_PASSWORD', '')

        if not sender_password:
            return False

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def notify_booking_confirmed(user_email: str, booking_details: dict):
    subject = "Booking Confirmed - Chaalak"
    body = f
    return send_email_notification(user_email, subject, body)

def notify_ride_completed(user_email: str, booking_id: str):
    subject = "Ride Completed - Chaalak"
    body = f
    return send_email_notification(user_email, subject, body)
