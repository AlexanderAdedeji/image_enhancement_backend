from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.authentication.auth import superuser_permission
from app.api.dependencies.db.db import get_db
from app.schemas.user_type_schemas import UserTypeCreate, UserTypeInDB
from app.repositories.user_type import user_type_repo
from app.core.errors.error_strings import ALREADY_EXISTS
from app.core.errors.exceptions import AlreadyExistsException


router = APIRouter()


@router.get(
    "/",
    #  dependencies=[Depends(superuser_permission)], 
     response_model=List[UserTypeInDB]
)
def get_all_user_types(db: Session = Depends(get_db)):
    user_types = user_type_repo.get_all(db)
    return [
        UserTypeInDB(id=user_type.id, name=user_type.name) for user_type in user_types
    ]



@router.post(
    "/",
    #  dependencies=[Depends(superuser_permission)], 
     response_model=UserTypeInDB
)
def create(user_type_in: UserTypeCreate, db: Session = Depends(get_db)):

    """
    This is used to create a new user type in the application
    You need to be a superuser to use this endpoint.
    You send the token in as a header of the form \n
    <b>Authorization</b> : 'Token <b> {JWT} </b>'
    """
    exists = bool(user_type_repo.get_by_name(db, name=user_type_in.name))
    if exists:
        raise AlreadyExistsException(
            detail=ALREADY_EXISTS.format("user type with name " + user_type_in.name)
        )

    user_type = user_type_repo.create(db, obj_in=user_type_in)
    return UserTypeInDB(id=user_type.id, name=user_type.name)
