from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True)
    original_name = Column(String)
    extension = Column(String)
    size = Column(Integer)
    content_type = Column(String)
