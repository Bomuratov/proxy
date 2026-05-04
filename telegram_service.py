import requests
from config import settings

class TelegramService:
    @staticmethod
    def send_message(text: str):
        token = settings.bot.token
        chat_id = settings.bot.chat_id

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
            },
            timeout=5
        )

        response.raise_for_status()
        return response.json()