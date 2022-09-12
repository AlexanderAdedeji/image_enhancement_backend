from datetime import datetime

from pydantic import BaseModel, EmailStr


class JWTUser(BaseModel):
    id: str
    user_type:str


class JWTMeta(BaseModel):
    exp: datetime
    sub: str