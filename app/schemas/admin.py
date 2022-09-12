import string
from typing import List, Optional
from pydantic import BaseModel



class User(BaseModel):
    first_name:str
    last_name:str
    email:str
    role:str


    
    
class UserOverview(BaseModel):
    active:int
    in_active:int

    




    
