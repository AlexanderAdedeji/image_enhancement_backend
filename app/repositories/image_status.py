# from app.schemas.image_quality import ImageQualityCreate
from app.models.image_status import ImageStatus
from app.commonLib.repositories import Base
# from app.models.manual_background_removed import ManuallyEdited




class ImageQualityRepositories(Base[ImageStatus]):
    def create(self, db, photo_name:str, reviewed_by:int):
        db_obj= ImageStatus(
            photo_name=photo_name,
            reviewed_by=reviewed_by
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    def get_by_photoname(self,db, photo_name:str):
        return db.query(ImageStatus).filter(ImageStatus.photo_name == photo_name).first()   
    
    def delete(self, db, photo_name:str):
        data = db.query(ImageStatus).filter(ImageStatus.photo_name == photo_name).first()
        db.delete(data)
        
        db.commit()
        
    def update(self,db, field_name:str, field_value, name:str):
        image= db.query(ImageStatus).filter(ImageStatus.photo_name == name).first()        
        setattr(image,field_name, field_value)
        db.commit()
        db.refresh(image)
        return image
        
        
    
    
imageStatus_repo =ImageQualityRepositories(ImageStatus)