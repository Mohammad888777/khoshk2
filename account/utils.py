import time
import random
from django.conf import settings
from kavenegar import *
from shortuuid.django_fields import ShortUUIDField
from django.core.exceptions import ValidationError
import uuid
import string

def generate_auto_custom_id(k=10):
    a=ShortUUIDField(alphabet=string.digits,length=k)
    return a._generate_uuid()



def createOtpToken(k=3):


    now=str(time.time())[-2:]
    other_number=''.join(
        random.choices(
            [str(i) for i in range(0,10)],
            k=3
        )
    )

    return other_number+now







def send_otp(user_phone_number, otp_code):
    try:
        api = KavenegarAPI(
            settings.KAVEHNEGAR_KEY,
        )
        params = {
            "receptor": user_phone_number,
            "template": settings.KAVEHNEGAR_CUSTOM_TEMPLATE_MYSELF_VAR,
            "token": otp_code,
            "type": "sms",
        }
        response = api.verify_lookup(params)

        print("*********************")
        print("*********************")
        print(response)
        print("*********************")
        print("*********************")

    except Exception as e:
        print("ERROROROR")
        print("ERROROROR")
        print(e)
        print("ERROROROR")
        print("ERROROROR")

        raise ValidationError("code not sent")





def convert_str_to_uuid(value):
    return uuid.UUID(value)
