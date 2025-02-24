from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from twilio.rest import Client
from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE

# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True, 
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fm = FastMail(conf)

# Function to Send Email
async def send_email(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html"
    )
    await fm.send_message(message)

# Configuration
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Function to Send SMS
def send_sms(phone_number: str, message: str):
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=phone_number
    )
