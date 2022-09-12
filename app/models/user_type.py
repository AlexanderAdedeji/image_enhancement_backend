from app.commonLib.models import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class UserType(Base):
    __tablename__ ="usertype"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    users = relationship("User", back_populates="user_type")

