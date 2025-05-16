from twilio.rest import Client

TWILIO_SID = 'TWILIO_ACCOUNT_SID'  # SID شما از Twilio
TWILIO_AUTH_TOKEN = 'TWILIO_AUTH_TOKEN'  # Token شما از Twilio
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # شماره تست Twilio Sandbox

def send_whatsapp_message(to, message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to='whatsapp:+989912146083'
    )
