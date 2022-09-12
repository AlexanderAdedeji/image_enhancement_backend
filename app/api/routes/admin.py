from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.image_status import ImageStatus
from app.repositories.user import user_repo
from app.api.dependencies.db.db import get_db
from app.schemas.admin import UserOverview
from app.schemas.user import DisplayUser
from app.api.dependencies.authentication.auth import superuser_permission

router = APIRouter()


@router.get('/get_all_reviewers',  dependencies=[Depends(superuser_permission)])
def get_all_reviewers(id: int, db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    reviewers = db.query(User).filter(User.user_role == "reviewer").all()
    return [
        DisplayUser(
            first_name=reviewer.first_name,
            email=reviewer.email,
            last_name=reviewer.last_name,
            is_active=reviewer.is_active,
            role=reviewer.user_role,
            id=reviewer.id

        )
        for reviewer in reviewers
    ]


@router.get('/get_all_active_reviewers')
def get_all_active_reviewers(id: int, db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    reviewers = db.query(User).filter(
        User.user_role == "reviewer", User.is_active == True).all()
    return [
        DisplayUser(
            first_name=reviewer.first_name,
            email=reviewer.email,
            last_name=reviewer.last_name,
            is_active=reviewer.is_active,
            role=reviewer.user_role,
            id=reviewer.id

        )
        for reviewer in reviewers
    ]


@router.get('/get_all_inactive_reviewers')
def get_all_inactive_reviewers(id: int,  db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')
    reviewers = db.query(User).filter(
        User.user_role == "reviewer", User.is_active == False).all()
    return [
        DisplayUser(
            first_name=reviewer.first_name,
            email=reviewer.email,
            last_name=reviewer.last_name,
            is_active=reviewer.is_active,
            role=reviewer.user_role,
            id=reviewer.id

        )
        for reviewer in reviewers
    ]


@router.get('/get_all_editors')
def get_all_editors(id: int, db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    editors = db.query(User).filter(User.user_role == "editor").all()
    return [
        DisplayUser(
            first_name=editor.first_name,
            email=editor.email,
            last_name=editor.last_name,
            is_active=editor.is_active,
            role=editor.user_role,
            id=editor.id

        )
        for editor in editors
    ]


@router.get('/get_all_active_editors')
def get_all_active_editors(id: int,  db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    editors = db.query(User).filter(
        User.user_role == "editor", User.is_active == True).all()
    return [
        DisplayUser(
            first_name=editor.first_name,
            email=editor.email,
            last_name=editor.last_name,
            is_active=editor.is_active,
            role=editor.user_role,
            id=editor.id

        )
        for editor in editors
    ]


@router.get('/get_all_inactive_editors')
def get_all_inactive_editors(id: int, db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    editors = db.query(User).filter(
        User.user_role == "editor", User.is_active == False).all()
    return [
        DisplayUser(
            first_name=editor.first_name,
            email=editor.email,
            last_name=editor.last_name,
            is_active=editor.is_active,
            role=editor.user_role,
            id=editor.id

        )
        for editor in editors
    ]


@router.get('/get_editors_overview')
def get_editors_overview(id: int, db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    active_editors = db.query(User).filter(
        User.user_role == "editor", User.is_active == True).count()

    in_active_editors = db.query(User).filter(
        User.user_role == "editor", User.is_active == False).count()
    return UserOverview(
        active=active_editors,
        in_active=in_active_editors
    )


@router.get('/get_all_admins')
def get_all_admins(id: int, db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    admins = db.query(User).filter(User.user_role == "admin" and User.email !=
                                   user.email and User.email != "superAdmin@gmail.com").all()
    return [
        DisplayUser(
            first_name=admin.first_name,
            email=admin.email,
            last_name=admin.last_name,
            is_active=admin.is_active,
            role=admin.user_role,
            id=admin.id

        )
        for admin in admins
    ]


@router.get('/get_user_overview_by_role')
def get_user_overview_by_role(id: int, user_role: str, db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')
    if user_role.lower() not in ["admin", "reviewer", "editor"]:
        raise HTTPException(
            status_code=403, detail="Invalid User Role"
        )
    active_users = db.query(User).filter(
        User.user_role == user_role.lower(), User.is_active == True).count()

    in_active_users = db.query(User).filter(
        User.user_role == user_role.lower(), User.is_active == False).count()
    print(in_active_users)
    return UserOverview(
        active=active_users,
        in_active=in_active_users
    )


@router.get('/get_all_active_admins')
def get_all_active_admins(id: int,  db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    admins = db.query(User).filter(
        User.user_role == "admin", User.is_active == True).all()
    return [
        DisplayUser(
            first_name=admin.first_name,
            email=admin.email,
            last_name=admin.last_name,
            is_active=admin.is_active,
            role=admin.user_role,
            id=admin.id

        )
        for admin in admins
    ]


@router.get('/get_all_inactive_admins')
def get_all_active_admins(id: int,  db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    admins = db.query(User).filter(
        User.user_role == "admin", User.is_active == False).all()
    return [
        DisplayUser(
            first_name=admin.first_name,
            email=admin.email,
            last_name=admin.last_name,
            is_active=admin.is_active,
            role=admin.user_role,
            id=admin.id

        )
        for admin in admins
    ]


@router.get('/get_user')
def get_user(user_id: int, id: int,  db: Session = Depends(get_db)):
    user = user_repo.get(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist')
    if user.user_role.lower() != "admin":
        raise HTTPException(
            status_code=401, detail=f'user does not have permissions')

    users = db.query(User).filter(User.id == user_id).all()
    return [
        DisplayUser(
            first_name=user.first_name,
            email=user.email,
            last_name=user.last_name,
            is_active=user.is_active,
            role=user.user_role,
            id=user.id

        )
        for user in users
    ]


@router.get("/reviewers_report")
def get_reviewers_report(id: int, db: Session = Depends(get_db)):

    reviewers = db.query(User).filter(User.user_role == "reviewer").all()
    reports =[]    
    for reviewer in reviewers:
        report = {"reviewer":reviewer, "report":{"good": 30, "rejected":"40", "cropped":30, "sent_for_download":43}}
        reports.append(report)
    return {
        "report": reports
    }
