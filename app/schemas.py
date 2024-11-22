from pydantic import BaseModel

class FileCreate(BaseModel):
    pass  # Дополнительно, если нужны входные данные

class FileResponse(BaseModel):
    uid: str
    original_name: str
    extension: str
    size: int
    content_type: str

    class Config:
        orm_mode = True
