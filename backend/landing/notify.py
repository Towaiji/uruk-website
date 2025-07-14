import os
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

dotenv = load_dotenv()
TWILIO_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
SENDGRID_KEY = os.environ.get("SENDGRID_API_KEY")


def send_message(receiver_phone: str, body: str):

    client = Client(TWILIO_SID, AUTH_TOKEN)

    message = client.messages.create(
        from_=f"whatsapp:{TWILIO_NUMBER}",
        body=body,
        to=f"whatsapp:{receiver_phone}",
    )

    return message

def send_email(from_email: str, to_emails: list, body: str, subject: str = "Uruk GC Task Reminder"):
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=f'<strong>{body}</strong>')

    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

