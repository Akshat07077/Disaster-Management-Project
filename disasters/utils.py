from twilio.rest import Client
from django.conf import settings
import re
def send_sms(to, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )
    return message.sid

def validate_phone_number(phone_number):
    # E.164 format: + followed by country code and subscriber number
    pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
    return pattern.match(phone_number) is not None

import phonenumbers
from phonenumbers import NumberParseException

def format_phone_number(phone_number, region='IN'):
    try:
        parsed_number = phonenumbers.parse(phone_number, region)
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        else:
            return None
    except NumberParseException:
        return None
