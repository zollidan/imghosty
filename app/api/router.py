import os
import datetime
from fastapi import APIRouter, Response, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from loguru import logger
from app.api.utils import generate_random_string
from app.config import settings, celery_app, redis_client, s3_client



router = APIRouter(prefix='/api', tags=['API'])

@router.post("/upload/s3")
async def upload_s3(file: UploadFile):
    try:
        # Прочитать загруженный файл
        file_content = await file.read()
        
    
        start_file_name = file.filename
        # Сгенерировать уникальное имя файла и ID для удаления
        file_extension:str = os.path.splitext(file.filename)[1]
        file_id = generate_random_string(12)
         
        
        response = s3_client.put_object(Body=file_content, Bucket=settings.AWS_BUCKET_NAME, Key=file_id + file_extension)
        
        """
            добавить запись в postgres или redis
        
        """
        
        
        return {"response": response}
        
    except HTTPException as e:
        raise e
    
@router.get("/files/s3")
async def get_s3_files():
    return s3_client.list_objects(Bucket=settings.AWS_BUCKET_NAME)['Contents']

@router.get("/files/{file_id}")
async def get_file_by_id(file_id:str):
    
    # Получить объект
    get_object_response = s3_client.get_object(Bucket=settings.AWS_BUCKET_NAME,Key=file_id)
    file_binary = get_object_response['Body'].read()
    
    # Получаем Content-Type из метаданных S3
    content_type = get_object_response['ContentType']
    
    return Response(
        content=file_binary,
        media_type=content_type
    )
    