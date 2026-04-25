import requests
from config import settings


class EskizSMS:

    @staticmethod
    def get_token():
        response = requests.post(
            settings.eskiz.auth_url,
            data={
                "email": settings.eskiz.email,
                "password": settings.eskiz.password,
            },
            timeout=5
        )

        response.raise_for_status()

        return response.json()["data"]["token"]

    @staticmethod
    def send_sms(phone: str, otp: str):
        token = EskizSMS.get_token()

        message = (
            f"Kod verifikatsii dlya vxoda v mobilnoye prilojenie Aurora Delivery: {otp}"
        )

        response = requests.post(
            settings.eskiz.sms_url,
            headers={"Authorization": f"Bearer {token}"},
            data={
                "mobile_phone": phone,
                "message": message,
                "from": "4546",
            },
            timeout=5
        )

        response.raise_for_status()

        return response