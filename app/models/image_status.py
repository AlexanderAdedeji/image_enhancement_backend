
from sqlalchemy import Column, Integer, String,Boolean
from app.commonLib.models import Base






class ImageStatus(Base):
    __tablename__="image_enhancement_status"
    id=Column(Integer, nullable=False,primary_key=True)
    photo_name=Column(String, nullable=False)
    image_status=Column(String, nullable=True)
    is_original_downloaded=Column(Boolean, nullable=True)
    upload_status=Column(String, nullable=True)
    sent = Column(Boolean, nullable=True)
    reviewed_by=Column(Integer, nullable=False)
    edited_by=Column(Integer, nullable=True)