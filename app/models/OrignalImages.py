from sqlalchemy import Column, Integer, String,Boolean
from app.database.sessions.session2 import Base2


class OriginalImages(Base2):
    __tablename__='ResidentOriginalCroppedImages'
    ID= Column(Integer, primary_key=True,index=True)
    RegistrationId= Column(String,  nullable=False)
    photo0= Column(String, nullable=False)
    photo10= Column(String, nullable=False)
    photo20= Column(String, nullable=False)
    photo30= Column(String, nullable=False)
    photo40= Column(String, nullable=False)
    photo50= Column(String, nullable=False)
    photo60= Column(String, nullable=False)
    photoName= Column(String, nullable=False)