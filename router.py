import os
import requests
from fastapi import HTTPException, File, UploadFile, HTTPException
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()




router = APIRouter(
    tags=["РАСХОДНИК API"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


ca_path = os.path.join(BASE_DIR, "keys/_.ofd.uz.pem")
ofd_client_cert = None
OFD_URL = os.environ.get("OFD_URL","")

@router.post("/v2/ofd/punch")
async def punch_receipt_proxy(file: UploadFile = File(...)):
    """
    Получает p7b файл от Django и отправляет на OFD
    """
    try:
        p7b_bytes = await file.read()
        headers = {
            "Content-Type": "application/octet-stream"
            
            }

        resp = requests.post(
            OFD_URL,
            data=p7b_bytes,
            headers=headers,
            verify=ca_path,
            cert=ofd_client_cert,
            timeout=10,
        )
        resp.raise_for_status()
        return {"success": True, "ofd_response": resp.json()}

    except requests.RequestException as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"OFD request failed: {str(e)}")







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


