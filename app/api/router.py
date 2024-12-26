import os
import datetime
from fastapi import APIRouter, UploadFile, HTTPException, Form
from loguru import logger
import requests

router = APIRouter(prefix='/api', tags=['API'])

@router.get("/")
def init_page():
    return {"msg": "0.0.1"}

