from celery import shared_task

from phone_number.models import TwilioSubAccount


@shared_task
def send_sms_message(
    to_number: str, from_number: str, message: str, organization_id: int
) -> bool:
    """Send SMS message via Twilio or SMS service"""
    try:
        # Import Twilio client
        from twilio.rest import Client

        twillio_sub_account = TwilioSubAccount.objects.get(
            organization_id=organization_id
        )
        account_sid = twillio_sub_account.twilio_account_sid
        auth_token = twillio_sub_account.twilio_auth_token

        twilio_client = Client(account_sid, auth_token)

        sms = twilio_client.messages.create(
            body=message, from_=from_number, to=to_number
        )

        print(f"SMS sent successfully: {sms.sid}")
        return True

    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False
