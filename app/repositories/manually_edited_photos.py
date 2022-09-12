from app.models.citizens_manually_edited_images import ResidentManuallyEditedPhotos
from sqlalchemy.orm import Session 
from app.commonLib.repositories import Base
from app.schemas.manuall_edited_photos import PhotoCreate
from app.schemas.user import  FullUser
from app.core.settings.utilities import Utilities







class ManuallyEditedRepositories(Base[ResidentManuallyEditedPhotos]):    
    def get_by_photo_name(self, db, *, photo_name):
        user = db.query(ResidentManuallyEditedPhotos).filter(ResidentManuallyEditedPhotos.photo_name == photo_name).first()
        return user
    
    def create(self,db,*, img_in:PhotoCreate):
        image_obj = ResidentManuallyEditedPhotos(
            photo_name= img_in.photo_name,
            photo= img_in.photo,
            user_id=img_in.user_id
            )
        db.add(image_obj)
        db.commit()
        db.refresh(image_obj)
        return image_obj
    

manuallyEdited_repo = ManuallyEditedRepositories(ResidentManuallyEditedPhotos)