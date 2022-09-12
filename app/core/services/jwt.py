from app.core.settings.config import AppSettings
from datetime import datetime
from pydantic import ValidationError
from app.core.errors.exceptions import InvalidTokenException
import jwt



settings = AppSettings()

JWT_ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY= settings.SECRET_KEY




def get_details_from_token(token:str):
    try:
        decode_payload = jwt.decode(token, str(SECRET_KEY), algorithms=[JWT_ALGORITHM])
        if decode_payload["exp"] <= datetime.now().timestamp():
            raise InvalidTokenException(detail="token has expired.")
        jwt_data={"id":decode_payload["id"], "user_type":decode_payload["user_type"]}
        return jwt_data
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except KeyError as decode_error:
        raise ValueError ("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error






