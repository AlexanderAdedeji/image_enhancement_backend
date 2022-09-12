from fastapi import APIRouter, BackgroundTasks
from typing import List
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.db.db import get_db
from app.schemas.image_status import CroppedVersion
from app.core.settings.config import AppSettings
import requests


settings = AppSettings()
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)




router = APIRouter()


def count_to_n(n: int):
    for i in range(n):
        print(i)
        time.sleep(1)


def send_multiple_good_photoName(photoNames:List[str]):
    print(photoNames)
    try:
        response =http.post(settings.MULTI_GOOD, photoNames)
        print(response)
    except :
        print("failed")
        time.sleep(1)
    return {"message": "Photonames sent successfully"}


def send_rejected_photoName(photoName: str):
    time.sleep(10)
    print(photoName)
    try:
        body = {"FileName": photoName}
        response = http.post(settings.REJECTED, body)
    except:
        print("not up")
    return {"message": photoName}


def send_cropped_photo_names(croppedObj:CroppedVersion):
 
    print(croppedObj)
    try:
        body = {"FileName": croppedObj.photo_name, "Column": croppedObj.column,
                    "Type": croppedObj.photo_type}
                    
        response =http.post(settings.GOOD, body)
        
        print(response)
    except:
            time.sleep(1)
            print("failed")
    return {"message": croppedObj.photo_name}

