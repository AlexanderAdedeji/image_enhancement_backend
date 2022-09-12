from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.image_status import ImageStatus
from app.repositories.user import user_repo
from app.repositories.user_type import user_type_repo
from app.api.dependencies.db.db import get_db
from app.api.dependencies.authentication.auth import superuser_permission,superuser_and_admin_permission


from app.schemas.user import User, UserCreate, UserLogin, UserValidated
from app.core.settings.utilities import Utilities





router = APIRouter()

@router.post("/login")
def user_login(login: UserLogin,db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, email=login.email)
    if not user:
        raise HTTPException(status_code=404, detail=f'Invalid Login Credentials') 
    is_password = Utilities.verify_password(login.password, user.hashed_password)
    if not is_password:
        raise HTTPException(status_code=403,detail= f'Invalid Login Credentials')
    if not user.is_active:
        raise HTTPException(status_code=403,detail= f'Account not active')
    user_type = user_type_repo.get(db, id=user.user_type_id)
    # if user.user_role.lower() == "editor":
    #     imagesToUpload = db.query(ImageStatus).filter(ImageStatus.edited_by == user.id).count() 
    #     return UserValidated(
    #             id=user.id,
    #             email = user.email,
    #             user_type=user_type.name,
    #             uploadImageCount=imagesToUpload 
    #         )
    # else:
    return UserValidated(
                first_name=user.first_name,
                last_name=user.last_name,
                user_type = user_type.name,
                token= user.generate_jwt()

            )
        








@router.post("/SignUp",
 response_model=User
 )
def user_signup(user: UserCreate, db:Session= Depends(get_db)):
    user_type_exist = user_type_repo.get_by_name(db, name=user.user_type.lower())
    if not user_type_exist:
        raise HTTPException(status_code=403, detail="User role type is not Valid try 'EDITOR or REVIEWER or ADMIN'")
    user_exist = user_repo.get_by_email(db, email=user.email)
    if user_exist:
        raise HTTPException(status_code=403, detail ='this email already exists')
    user.user_type = user_type_exist.id
    new_user = user_repo.create(db, obj_in=user)
    return User(
        first_name=new_user.first_name,
        last_name= new_user.last_name,
        email = new_user.email,
        user_type=user_type_exist.name
        )
    
    
@router.put('/deactivateUser')
def deactivate_user(user_id:int, db:Session=Depends(get_db)):
    user_exist = user_repo.get(db, id=user_id)
    if not user_exist:
        raise HTTPException(status_code=403, detail ='This user does not exist')
    if user_exist.first_name.lower() == "super":
        raise HTTPException(status_code=403, detail ='This user cannot be deactivated')
    if not user_exist.is_active:
        raise HTTPException(status_code=403, detail ='This user has already been  deactivated')
    
    user_deactiavted = user_repo.deactivate(db, db_obj=user_exist)
        
    
    return {
        "message": f"{user_deactiavted.first_name} {user_deactiavted.first_name} has been deactivated Successfully"
    }
    
    
@router.put('/activateUser',
 dependencies=[Depends(superuser_and_admin_permission)]
 )
def activate_user(user_id:int, db:Session=Depends(get_db)):
    user_exist = user_repo.get(db, id=user_id)
    if not user_exist:
        raise HTTPException(status_code=403, detail='This user does not exist')
    if user_exist.is_active:
        raise HTTPException(status_code=403, detail='This user has already been activated')
    
    user_actiavted = user_repo.activate(db, db_obj=user_exist)
    return {
        "message": f"{user_actiavted.first_name} {user_actiavted.first_name} has been activated Successfully"
    }