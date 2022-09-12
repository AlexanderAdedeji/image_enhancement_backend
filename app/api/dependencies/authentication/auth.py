from app.core.services.jwt import get_details_from_token
from loguru import logger
from typing import List, Optional
from fastapi import Depends, Security, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import APIKeyHeader as DefaultAPIKeyHeader
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.user import User
from starlette import requests, status
from app.models.user_type import UserType
from app.api.dependencies.db.db import get_db
from app.core.errors.error_strings import (
    AUTHENTICATION_REQUIRED,
    INACTIVE_USER_ERROR,
    MALFORMED_PAYLOAD,
    WRONG_TOKEN_PREFIX,
    UNAUTHORIZED_ACTION,
)
from app.repositories.user import user_repo
from app.core.errors.exceptions import (
    DisallowedLoginException,
    InvalidTokenException,
    UnauthorizedEndpointException,
)



from app.core.settings.config import AppSettings




settings = AppSettings()




JWT_TOKEN_PREFIX = settings.JWT_TOKEN_PREFIX
HEADER_KEY = settings.HEADER_KEY


REVIEWER_USER_TYPE =settings.REVIEWER_USER_TYPE
EDITOR_USER_TYPE =settings.EDITOR_USER_TYPE
ADMIN_USER_TYPE= settings.ADMIN_USER_TYPE
SUPERUSER_TYPE= settings.SUPERUSER_TYPE


class JWTHEADER(DefaultAPIKeyHeader):
    async def __call__(
        _,
        request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=original_auth_exc.detail or AUTHENTICATION_REQUIRED,
            )


def _extract_jwt_from_header(
    authorization_header: str = Security(JWTHEADER(name=HEADER_KEY)),
):
    try:

        token_prefix, token = authorization_header.split(" ")

    except ValueError:
        raise InvalidTokenException(detail=WRONG_TOKEN_PREFIX)
    if token_prefix != JWT_TOKEN_PREFIX:
        raise InvalidTokenException(detail=WRONG_TOKEN_PREFIX)
    return token


def check_if_user_is_valid(user: User):
    if not user:
        raise InvalidTokenException(detail=MALFORMED_PAYLOAD)
    if not user.is_active:
        raise DisallowedLoginException(detail=INACTIVE_USER_ERROR)

def get_currently_authenticated_user(
    *,
    db: Session = Depends(get_db),
    token: str = Depends(_extract_jwt_from_header),
) -> User:
    try:
        token_details = get_details_from_token(token)
        print(token_details)
        user = user_repo.get(db, id=token_details['id'])
        check_if_user_is_valid(user)
    except ValueError:
        raise InvalidTokenException(detail=MALFORMED_PAYLOAD)
    return user




class PermissionChecker:
    def __init__(self, *, allowed_user_types: List[str]):
        self.allowed_user_types = allowed_user_types
    def __call__(self, user=Depends(get_currently_authenticated_user)):
        current_user_type = user.user_type
        if current_user_type.name not in self.allowed_user_types:
            logger.debug(
                f"User with type {current_user_type.name} not in  {self.allowed_user_types}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=UNAUTHORIZED_ACTION
            )


reviewer_permission = PermissionChecker(allowed_user_types=[REVIEWER_USER_TYPE])
editor_permission = PermissionChecker(allowed_user_types=[EDITOR_USER_TYPE])
admin_permission = PermissionChecker(allowed_user_types=[ADMIN_USER_TYPE])
superuser_permission = PermissionChecker(allowed_user_types=["SUPERUSER"])
superuser_and_admin_permission = PermissionChecker(allowed_user_types=[ADMIN_USER_TYPE, SUPERUSER_TYPE])






