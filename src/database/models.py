from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, unique=True)
    filename = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String)