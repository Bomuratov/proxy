import os
import requests
from fastapi import HTTPException, File, UploadFile, HTTPException
from fastapi import APIRouter
from dotenv import load_dotenv
import certifi
from starlette import status

from schemas import VerifyCode
from sms_service import EskizSMS
from telegram_service import TelegramService
from fastapi import Header

load_dotenv()


router = APIRouter(
    tags=["РАСХОДНИК API"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ca_path = os.path.join(BASE_DIR, "keys/_.ofd.uz.pem")
ca_path = os.path.join(BASE_DIR, "keys/test_ofd.pem")
ofd_client_cert = None
OFD_URL = os.environ.get("OFD_URL", "")
PROD_OFD_URL = "https://ofd.uz/emp/v3/receipt"
TEST_OFD_URL = "https://test.ofd.uz/emp/v3/receipt"
NOTIFY_URL = "https://notify.aurora-api.uz/fastapi/reject/ofd"


@router.post("/v2/ofd/punch")
async def punch_receipt_proxy(file: UploadFile = File(...), x_source: str | None = Header(default=None),):
    """
    Получает p7b файл от Django и отправляет на OFD
    """
    if x_source == "django-stage":
        ofd_url = TEST_OFD_URL
    else:
        ofd_url = PROD_OFD_URL
    try:
        p7b_bytes = await file.read()
        headers = {"Content-Type": "application/octet-stream"}

        print("OFD URL:", ofd_url)
        print("X-SOURCE:", x_source)
        resp = requests.post(
            url=ofd_url,
            data=p7b_bytes,
            headers=headers,
            verify=certifi.where(),
            timeout=(5, 10),
        )
        resp.raise_for_status()
        return {"success": True, "ofd_response": resp.json()}

    except requests.RequestException as e:
        print(e)
        # --- ДОБАВИЛИ: отправка в notify API ---
        try:
            requests.post(
                NOTIFY_URL,
                files={"file": (file.filename, p7b_bytes, "application/octet-stream")},
                data={
                    "error": str(e),
                },
                timeout=5,
            )
        except Exception as notify_err:
            print("Notify error:", notify_err)

        # --- оставляем твою логику ---
        raise HTTPException(status_code=500, detail=f"OFD request failed: {str(e)}")


@router.post("/send-verify-code")
def send_verification(payload: VerifyCode):
    eskiz = EskizSMS()
    bot = TelegramService()
    response = None

    try:
        response = eskiz.send_sms(phone=str(payload.phone), otp=str(payload.otp))

        data = response.json()
        # text = f"OTP успешно отправлен на номер +{payload.phone},\nOTP код: {payload.otp}\nОтвет от ESKIZ:\n<pre language='json'>{data}</pre>"

        # bot.send_message(
        #     text=text,
        # )

        return data

    except requests.RequestException as e:
        error_text = f"Ошибка при отправке OTP на номер +{payload.phone}\nOTP: {payload.otp}\nОшибка: {str(e)}"
        # bot.send_message(
        #     text=error_text,
        # )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке SMS",
        )


# import os
# import json
# import ssl
# import requests
# from fastapi import APIRouter, File, UploadFile, HTTPException
# from dotenv import load_dotenv
# from requests.adapters import HTTPAdapter
# from urllib3.poolmanager import PoolManager

# load_dotenv()

# router = APIRouter(
#     tags=["РАСХОДНИК API"],
# )

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ca_path = os.path.join(BASE_DIR, "keys/_.ofd.uz.pem")

# ofd_client_cert = None
# # если нужен клиентский сертификат:
# # ofd_client_cert = ("/path/to/client.crt", "/path/to/client.key")

# OFD_URL = os.environ.get("OFD_URL", "")


# class SSLAdapter(HTTPAdapter):
#     def __init__(self, ca_path, **kwargs):
#         self.ca_path = ca_path
#         super().__init__(**kwargs)

#     def init_poolmanager(self, connections, maxsize, block=False):
#         context = ssl.create_default_context(cafile=self.ca_path)
#         context.verify_mode = ssl.CERT_REQUIRED
#         context.check_hostname = True

#         self.poolmanager = PoolManager(
#             num_pools=connections,
#             maxsize=maxsize,
#             block=block,
#             ssl_context=context,
#         )


# @router.post("/v2/ofd/punch")
# async def punch_receipt_proxy(file: UploadFile = File(...)):
#     """
#     Получает p7b файл от Django и отправляет на OFD
#     """
#     try:
#         p7b_bytes = await file.read()

#         headers = {
#             "Content-Type": "application/octet-stream",
#             "User-Agent": "ofd-client/1.0",
#         }

#         # HTTPS-сессия с CA (эквивалент https.Agent в Node.js)
#         session = requests.Session()
#         session.mount("https://", SSLAdapter(ca_path))

#         resp = session.post(
#             OFD_URL,
#             data=p7b_bytes,
#             headers=headers,
#             cert=ofd_client_cert,
#             timeout=30,
#         )

#         resp.raise_for_status()

#         # OFD может вернуть не-JSON
#         try:
#             ofd_response = resp.json()
#         except ValueError:
#             ofd_response = resp.text

#         return {
#             "success": True,
#             "ofd_response": ofd_response,
#         }

#     except requests.RequestException as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"OFD request failed: {str(e)}",
#         )
