from typing import List
import copy
from app.database.sessions.session import con
import base64
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    File,
    Form,
    UploadFile,
    BackgroundTasks,
)

from app.api.dependencies.db.db import get_db
from app.api.dependencies.db.db2 import get_db2
from app.models.EnhancedImages import EnhancedImages
from app.models.OrignalImages import OriginalImages

from app.repositories.user import user_repo
from app.models.image_status import ImageStatus
from app.repositories.image_status import imageStatus_repo
from app.repositories.manually_edited_photos import manuallyEdited_repo
from sqlalchemy.orm import Session
from app.repositories.image_status import ImageQualityRepositories
from app.repositories.user import user_repo
from app.api.dependencies.authentication.auth import (
    get_currently_authenticated_user,
    reviewer_permission,
    editor_permission,
)
from app.schemas.image_status import (
    CroppedVersion,
    ImageQuality,
    ShowImage,
    scheduleImageForDownload,
)
from app.schemas.manuall_edited_photos import PhotoCreate
from app.core.settings.utilities import Utilities
from app.api.routes.automations import (
    send_multiple_good_photoName,
    send_rejected_photoName,
    send_cropped_photo_names,
)
from app.schemas.user import User


router = APIRouter()


@router.get(
    "/get_images_for_review",
    response_model=List[ShowImage],
    status_code=200,
    dependencies=[Depends(reviewer_permission)],
)
def get_images_for_review(
    *,
    current_user: User = Depends(get_currently_authenticated_user),
    db: Session = Depends(get_db),
    db2: Session = Depends(get_db2),
):

    """
    This end point gets a list of 30 images for review.
    Provide a valid user id to get the images.
    """

    user_exist = user_repo.get(db, id=current_user.id)
    if not user_exist:
        raise HTTPException(
            status_code=404, detail=f"user with id {current_user.id} does not exit"
        )
    null_images = (
        db.query(ImageStatus)
        .filter(
            (ImageStatus.reviewed_by == current_user.id),
            (ImageStatus.image_status == None),
        )
        .all()
    )

    if null_images:
        for image in null_images:
            imageStatus_repo.delete(db, photo_name=image.photo_name)
    query = """
        select top 30 im.RegistrationId, 
        im.photo30,
        im.photoName from CardGenDb.dbo.ResidentBRCroppedImages im
        where im.photoName not in (select st.photo_name from ImageQcDbTest.dbo.image_enhancement_status st)
        """

    images = db.execute(query).fetchall()
    if not images:
        raise HTTPException(
            status_code=404, detail="There are no more images at this time"
        )
    for image in images:
        imageStatus_repo.create(
            db, photo_name=image["photoName"], reviewed_by=current_user.id
        )
    return [
        ShowImage(
            id=images.index(image),
            registration_id=image["RegistrationId"],
            photo=Utilities.convert_to_base_64(image["photo30"]),
            photo_name=image["photoName"],
            cropped_column="column30",
        )
        for image in images
    ]


@router.get(
    "/get_images_for_edit",
    response_model=List[ShowImage],
    dependencies=[Depends(editor_permission)],
    status_code=200,
)
def get_images_for_edit(
    *, user_id: int, db: Session = Depends(get_db), db2: Session = Depends(get_db2)
):
    """
    This end point gets a list of 20 images for download and editing.
    Provide a valid user id to get the images.
    """

    user_exist = user_repo.get(db, id=user_id)
    if not user_exist:
        raise HTTPException(
            status_code=404, detail=f"user with id {user_id} does not exit"
        )
    if user_exist.user_role.lower() != "editor":
        raise HTTPException(
            status_code=401, detail=f"You are not authorised to access this function"
        )
    query = """
                  SELECT TOP (20) 
      photo_name
      ,image_status
      ,is_original_downloaded
	  	  ,tr.[photo30] as enhanced_photo
	  ,sr.photo30 as original_photo
   ,tr.RegistrationId as registration_id

  FROM [ImageQcDb].[dbo].[image_enhancement_status] st
  LEFT JOIN [CardGenDb].[dbo].[ResidentBRCroppedImages] tr
   on st.photo_name = tr.photoName
  LEFT JOIN  [CardGenDb].[dbo].[ResidentOriginalCroppedImages] sr
  on tr.photoName = sr.photoName
  where st.image_status ='download'
and st.edited_by is null and st.upload_status is null
            """

    enhanced_images = db.execute(query).fetchall()
    if not enhanced_images:
        raise HTTPException(
            status_code=404, detail="There are no more images at this time"
        )

    return [
        ShowImage(
            id=enhanced_images.index(image),
            registration_id=image.registration_id,
            photo_name=image.photo_name,
            cropped_column="column30",
            photo=Utilities.convert_to_base_64(image.original_photo)
            if image.is_original_downloaded
            else Utilities.convert_to_base_64(image.enhanced_photo),
        )
        for image in enhanced_images
    ]


@router.get("/search")
def search_image(
    lasrraId: str,
    user_id: int,
    db: Session = Depends(get_db),
    db2: Session = Depends(get_db2),
):
    user_exist = user_repo.get(db, id=user_id)
    if not user_exist:
        raise HTTPException(
            status_code=404, detail=f"user with id {user_id} does not exit"
        )
    query = """
       select im.RegistrationId, 
       im.ID,
                im.photo30,
                im.photoName from CardGenDb.dbo.ResidentBRCroppedImages im
                join CardGenDb.dbo.ResidentEnrollmentReg st on im.RegistrationId=st.RegistrationId
                where st.EnrollmentId = ?
     """
    searched_image = con.execute(query, (lasrraId)).fetchone()
    if not searched_image:
        raise HTTPException(status_code=403, detail="Lasrra Id not found")

    if user_exist.user_role.lower() == "editor":
        image = (
            db.query(ImageStatus)
            .filter(
                ImageStatus.photo_name == searched_image.photoName
                and ImageStatus.upload_status == None
            )
            .all()
        )
        if not image:
            raise HTTPException(
                status_code=404, detail="There Image has already been processed"
            )
        imageStatus_repo.update(
            db,
            field_name="edited_by",
            field_value=user_id,
            name=searched_image["photoName"],
        )
        imageStatus_repo.update(
            db,
            field_name="upload_status",
            field_value="pending",
            name=searched_image["photoName"],
        )
    if user_exist.user_role.lower() == "reviewer":
        image = (
            db.query(ImageStatus)
            .filter(ImageStatus.photo_name == searched_image.photoName)
            .all()
        )
        if image:
            raise HTTPException(
                status_code=404, detail="There Image has already been processed"
            )
        imageStatus_repo.create(
            db, photo_name=searched_image["photoName"], reviewed_by=user_id
        )

    return ShowImage(
        id=searched_image["ID"],
        registration_id=searched_image["RegistrationId"],
        photo=Utilities.convert_to_base_64(searched_image["photo30"]),
        photo_name=searched_image["photoName"],
        cropped_column="column30",
    )


@router.delete("/remove_image_status_record")
def remove_image_status_record(photo_names: List[str], db: Session = Depends(get_db)):
    for photo_name in photo_names:
        data = imageStatus_repo.get_by_field(
            db, field_name="photo_name", field_value=photo_name
        )
        if not data:
            raise HTTPException(status_code=404, detail=f"{photo_name} does not exist")
        imageStatus_repo.delete(db, photo_name=photo_name)
    return {"message": "Image Removed Successfully."}


@router.delete("/unassign_editor_from_image_record")
def unassign_editor_from_image_record(
    photo_names: List[str], db: Session = Depends(get_db)
):
    for photo_name in photo_names:
        data = imageStatus_repo.get_by_field(
            db, field_name="photo_name", field_value=photo_name
        )
        if not data:
            raise HTTPException(status_code=404, detail=f"{photo_name} does not exist")
        imageStatus_repo.update(
            db, field_name="edited_by", field_value=None, name=photo_name
        )
    return {"message": "Image Removed Successfully."}


@router.put("/save_cropped_version")
def save_cropped_version(
    croppedObj: CroppedVersion,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
):
    imageStatus_repo.update(
        db,
        field_name="image_status",
        field_value=f"{croppedObj.photo_type.lower()}_{croppedObj.column}",
        name=croppedObj.photo_name,
    )
    background_task.add_task(send_cropped_photo_names, croppedObj)
    return {"message": "Image Saved Successfully."}


@router.put("/update_image_status", dependencies=[Depends(reviewer_permission)])
def update_image_status(
    photo_names: ImageQuality,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_currently_authenticated_user),
):
    background_task.add_task(send_multiple_good_photoName, photo_names.good)
    for photo_name in photo_names.good:
        imageStatus_repo.update(
            db, field_name="image_status", field_value="Good", name=photo_name
        )
    for photo_name in photo_names.bad:
        imageStatus_repo.update(
            db, field_name="image_status", field_value="Bad", name=photo_name
        )
    return {"message": "Image Status Updated Successfully."}


@router.put("/reject_image", dependencies=[Depends(reviewer_permission)])
def reject_image(
    photo_name: str, background_task: BackgroundTasks, db: Session = Depends(get_db), current_user= Depends(get_currently_authenticated_user)
):

    image = imageStatus_repo.get_by_photoname(db, photo_name=photo_name)
    if not image:
        raise HTTPException(status_code=404, detail=f"{photo_name} does not exist")
    if image.reviewed_by != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"you are not the Reviewer that selected this image"
        )
    if image.image_status != "Bad" and image.image_status != None:
        raise HTTPException(
            status_code=403, detail=f"you have already worked on this image"
        )

    imageStatus_repo.update(
        db, field_name="image_status", field_value="rejected", name=photo_name
    )
    background_task.add_task(send_rejected_photoName, photo_name)

    return {"message": f"{photo_name} has been rejected"}


@router.put("/schedule_for_download")
def schedule_for_download(
    imageData: scheduleImageForDownload, db: Session = Depends(get_db)
):
    image = imageStatus_repo.get_by_photoname(db, photo_name=imageData.photo_name)
    if not image:
        raise HTTPException(
            status_code=404, detail=f"{imageData.photo_name} does not exist"
        )
    if image.image_status != "Bad" and image.image_status != None:
        raise HTTPException(
            status_code=403, detail=f"you have already worked on this image"
        )
    imageStatus_repo.update(
        db, field_name="image_status", field_value="download", name=imageData.photo_name
    )
    if imageData.photo_type.lower() == "original":
        imageStatus_repo.update(
            db,
            field_name="is_original_downloaded",
            field_value=True,
            name=imageData.photo_name,
        )
    return {"message": f"Image Scheduled For Downlaod"}


@router.put("/download_image")
def download_image(user_id: int, photo_name: str, db: Session = Depends(get_db)):
    image = imageStatus_repo.get_by_photoname(db, photo_name=photo_name)
    if not image:
        raise HTTPException(status_code=404, detail=f"{photo_name} does not exist")
    # if image.image_status != 'Bad' and image.image_status !=None:
    #     raise HTTPException(status_code=403, detail=f"you have already worked on this image")
    imageStatus_repo.update(
        db, field_name="edited_by", field_value=user_id, name=photo_name
    )
    imageStatus_repo.update(
        db, field_name="upload_status", field_value="pending", name=photo_name
    )

    return {"message": f"Image Downlaoded Successfully"}


@router.get("/get_original_image")
def get_original_images(
    registration_id: str, db2: Session = Depends(get_db2), db: Session = Depends(get_db)
):
    image = (
        db2.query(OriginalImages)
        .filter(OriginalImages.RegistrationId == registration_id)
        .first()
    )
    if not image:
        raise HTTPException(status_code=403, detail=f"Image does not exist")
    img = imageStatus_repo.get_by_photoname(db, photo_name=image.photoName)
    if not img:
        raise HTTPException(status_code=403, detail=f"Image does not exist")
    if img.image_status != "Bad" and img.image_status != None:
        raise HTTPException(
            status_code=403, detail=f"you have already worked on this image"
        )

    return ShowImage(
        id=image.ID,
        registration_id=image.RegistrationId,
        photo=Utilities.convert_to_base_64(image.photo30),
        photo_name=image.photoName,
        cropped_column="column30",
    )


@router.get("/get_original_cropped_images")
def get_cropped_images(
    registration_id: str, db2: Session = Depends(get_db2), db: Session = Depends(get_db)
):

    image = (
        db2.query(OriginalImages)
        .filter(OriginalImages.RegistrationId == registration_id)
        .first()
    )
    if not image:
        raise HTTPException(status_code=403, detail=f"Image does not exist")
    img = imageStatus_repo.get_by_photoname(db, photo_name=image.photoName)
    if not img:
        raise HTTPException(status_code=403, detail=f"Image does not exist")
    if img.image_status != "Bad" and img.image_status != None:
        raise HTTPException(
            status_code=403, detail=f"you have already worked on this image"
        )

    image_copy = copy.deepcopy(image)
    image_copy.photo0 = base64.b64encode(image.photo0)
    image_copy.photo10 = base64.b64encode(image.photo10)
    image_copy.photo20 = base64.b64encode(image.photo20)
    image_copy.photo30 = base64.b64encode(image.photo30)
    image_copy.photo40 = base64.b64encode(image.photo40)
    image_copy.photo50 = base64.b64encode(image.photo50)
    image_copy.photo60 = base64.b64encode(image.photo60)
    return image_copy


@router.get("/get_enhanced_cropped_images",dependencies=[Depends(reviewer_permission)])
def get_cropped_images(
    registration_id: str, db2: Session = Depends(get_db2), db: Session = Depends(get_db)
):

    image = (
        db2.query(EnhancedImages)
        .filter(EnhancedImages.RegistrationId == registration_id)
        .first()
    )
    if not image:
        raise HTTPException(status_code=403, detail=f"Image does not exist")
    img = imageStatus_repo.get_by_photoname(db, photo_name=image.photoName)
    if not img:
        raise HTTPException(status_code=403, detail=f"Image does not exist")
    if img.image_status != "Bad" and img.image_status != None:
        raise HTTPException(
            status_code=403, detail=f"you have already worked on this image"
        )

    image_copy = copy.deepcopy(image)
    image_copy.photo0 = base64.b64encode(image.photo0)
    image_copy.photo10 = base64.b64encode(image.photo10)
    image_copy.photo20 = base64.b64encode(image.photo20)
    image_copy.photo30 = base64.b64encode(image.photo30)
    image_copy.photo40 = base64.b64encode(image.photo40)
    image_copy.photo50 = base64.b64encode(image.photo50)
    image_copy.photo60 = base64.b64encode(image.photo60)
    return image_copy


@router.get("/images_to_be_uploaded_by_user")
def get_user_images_to_upload(user_id: int, db: Session = Depends(get_db)):
    user_exist = user_repo.get(db, id=user_id)
    if not user_exist:
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")
    photo_names = (
        db.query(ImageStatus.photo_name)
        .filter(
            ImageStatus.edited_by == user_id, ImageStatus.upload_status == "Pending"
        )
        .all()
    )
    return photo_names


@router.post("/upload_image/", status_code=201)
async def imageUpload(
    user_id: int,
    image: UploadFile = File(...),
    db2: Session = Depends(get_db2),
    db: Session = Depends(get_db),
):
    data = await image.read()
    jpeg_data = (Utilities.convert_to_base_64(data),)
    img_obj = PhotoCreate(
        photo=jpeg_data[0], photo_name=str(image.filename), user_id=user_id
    )
    print(img_obj.photo_name)
    image_exist = imageStatus_repo.get_by_photoname(db, photo_name=img_obj.photo_name)
    if not image_exist:
        raise HTTPException(
            status_code=404,
            detail=f"The Image with name {img_obj.photo_name} not found",
        )
    img_exists = manuallyEdited_repo.get_by_field(
        db2, field_name="photo_name", field_value=img_obj.photo_name
    )
    if img_exists:
        raise HTTPException(
            status_code=403, detail=f"The Image has been Uploaded Already"
        )

    manuallyEdited_repo.create(db2, img_in=img_obj)
    imageStatus_repo.update(
        db, field_name="uploadStatus", field_value="uploaded", name=img_obj.photo_name
    )
    return {"message": "Image Successfully Uploaded"}
