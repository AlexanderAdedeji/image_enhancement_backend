import string
from typing import List, Optional
from pydantic import BaseModel



class PhotoCreate(BaseModel):
    photo_name:str
    photo:str
    user_id:str
 
