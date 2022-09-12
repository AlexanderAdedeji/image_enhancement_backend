from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import Integer, Column, Boolean, String,ForeignKey
from sqlalchemy.orm import relationship
from app.commonLib.models import Base
from app.core.settings.config import AppSettings
from app.core.services.security import AppSecurity
from app.schemas.jwt import JWTUser
import jwt



settings = AppSettings()
security = AppSecurity()
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXPIRE_MINUTES = settings.JWT_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY
RESET_TOKEN_EXPIRE_MINUTES = settings.RESET_TOKEN_EXPIRE_MINUTES

class User(Base):
    __tablename__ = 'image_enhancement_users'
    id =Column(Integer, primary_key=True, index=True)
    first_name = Column(String,nullable=False)
    last_name= Column(String, nullable=False)
    email = Column(String, nullable=False)
    is_active=Column(Boolean, nullable=False, default=False)
    hashed_password=Column(String, nullable=False)
    user_type_id=Column(Integer,ForeignKey("usertype.id"),nullable=False )
    user_type = relationship("UserType", back_populates="users")
    @property
    def is_superuser(self):
        print('super user')
    def set_password(self, password: str) -> None:
        self.password = security.get_password_hash(password)
    def generate_unique_id(self) -> str:
        self.id = str(uuid4())
    def verify_password(self, password: str) -> bool:
        return security.verify_password(password, self.password)

    def generate_jwt(self, expires_delta: timedelta = None):
        if not self.is_active:
            raise Exception("user is not active")
        jwt_content = JWTUser(id=self.id, user_type=self.user_type.name).dict()
        if expires_delta is None:
            expires_delta = timedelta(minutes=JWT_EXPIRE_MINUTES)
        now = datetime.now()
        expires_at = now + expires_delta
        jwt_content["exp"] = expires_at.timestamp()
        jwt_content["iat"] = now.timestamp()
        encoded_token = jwt.encode(jwt_content, SECRET_KEY, algorithm="HS256")
        return encoded_token