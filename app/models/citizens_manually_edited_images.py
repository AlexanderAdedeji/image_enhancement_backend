
from sqlalchemy import Column, Integer, String,Boolean
from app.commonLib.models import Base
from app.database.sessions.session2 import Base2






class ResidentManuallyEditedPhotos(Base2):
    __tablename__="ResidentManuallyEditedPhotos"
    id=Column(Integer, nullable=False,primary_key=True)
    photo_name=Column(String, nullable=False)
    photo= Column(String, nullable=False)
    user_id=Column(Integer, nullable=False)
