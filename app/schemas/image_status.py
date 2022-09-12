from pydantic import  BaseModel
from typing import List,Optional

from sqlalchemy import column



class Image(BaseModel):
    registration_id:str
    photo:str
    

class ImageQuality(BaseModel):
    good:Optional[List[str]] = None
    bad:Optional[List[str]]=None
    
    
class ShowImage(Image):
    id:int
    photo_name:str
    cropped_column:str
    
    
    
class ImageCreate(Image):
    width:str
    height:str
    photoName:str
    reviewed:str
    
    
    
class CroppedVersion(BaseModel):
    photo_name:str
    column:str
    photo_type:str
    
class CheckedImages(BaseModel):
    ID:int
    height:str
    RegistrationId:str
    photo:str
    photoName:str
    reviewd:str
    width:str



class scheduleImageForDownload(BaseModel):
    photo_name:str
    photo_type:str

    
    
    
class UncheckImages(BaseModel):
    RegistrationId:List[str]
    
    
class InsertCheckImages(BaseModel):
    images: List[CheckedImages]