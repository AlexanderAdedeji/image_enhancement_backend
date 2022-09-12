from typing import List
from app.models.user_type import UserType
from app.commonLib.repositories import Base
from app.schemas.user_type_schemas import UserTypeCreate, UserTypeUpdate
from sqlalchemy.orm import Session


class UserTypeRepository(Base[UserType]):
    def get_by_name(self, db: Session, *, name:str) -> UserType:
        return db.query(UserType).filter(UserType.name == name).first()
    def get_all_names(self, db:Session)->UserType:
        return db.query(UserType.name).all()
    def get_by_id(self, db:Session, *,id:int )->UserType:
        return db.query(UserType).filter(UserType.id == id).first()

user_type_repo = UserTypeRepository(UserType)
