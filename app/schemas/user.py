import string
from typing import List, Optional
from pydantic import BaseModel



class User(BaseModel):
    first_name:str
    last_name:str
    email:str
    user_type:str



class FullUser(User):
    is_active:str
    

class UserCreate(User):
    password:str
    


class UserLogin(BaseModel):
    email:str
    password:str

    
class UserValidated(BaseModel):
    first_name:str
    last_name:str
    user_type:str
    token:str
    uploadImageCount:Optional[int]
    
    
class DisplayUser(User):
    id:int
    is_active:bool