import os
import requests
from fastapi import HTTPException, File, UploadFile, HTTPException
from fastapi import APIRouter


router = APIRouter(
    tags=["РАСХОДНИК API"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


ca_path = os.path.join(BASE_DIR, "keys/_.ofd.uz.pem")
ofd_client_cert = None
OFD_URL = "https://test.ofd.uz/emp/v3/receipt"

@router.post("/v2/ofd/punch")
async def punch_receipt_proxy(file: UploadFile = File(...)):
    """
    Получает p7b файл от Django и отправляет на OFD
    """
    try:
        p7b_bytes = await file.read()
        headers = {"Content-Type": "application/octet-stream"}

        resp = requests.post(
            OFD_URL,
            data=p7b_bytes,
            headers=headers,
            verify=ca_path,
            cert=ofd_client_cert,
            timeout=30,
        )
        resp.raise_for_status()
        return {"success": True, "ofd_response": resp.json()}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"OFD request failed: {str(e)}")

