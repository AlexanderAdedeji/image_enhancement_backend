import base64
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Utilities():
    def convert_to_base_64(image):
        return base64.b64encode(image)
    
    def convert_to_image(b):
        return base64.b64decode(b)
    
    def hash_password(password):
        return pwd_context.hash(password)
    
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    