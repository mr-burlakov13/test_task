# main.py

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
import os
import asyncio

import models, schemas, utils, cloud_storage
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Путь для сохранения файлов
UPLOAD_DIRECTORY = "./uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/upload", response_model=schemas.FileResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    uid = utils.generate_uid()
    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIRECTORY, f"{uid}{file_extension}")

    # Сохранение файла на диск
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Получение метаданных
    size = os.path.getsize(file_path)
    content_type = file.content_type
    original_name = file.filename

    # Сохранение метаданных в БД
    db_file = models.File(
        uid=uid,
        original_name=original_name,
        extension=file_extension,
        size=size,
        content_type=content_type
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    # Асинхронная отправка в облако
    asyncio.create_task(cloud_storage.upload_to_cloud(file_path, original_name))

    return db_file

# Эндпоинт для получения файла по UID
@app.get("/files/{uid}")
def get_file(uid: str, db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.uid == uid).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = os.path.join(UPLOAD_DIRECTORY, f"{uid}{db_file.extension}")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(path=file_path, filename=db_file.original_name, media_type=db_file.content_type)

