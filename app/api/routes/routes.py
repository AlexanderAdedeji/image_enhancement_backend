from fastapi import APIRouter
from app.api.routes import users
from app.api.routes import user_type
from app.api.routes import automations
from app.api.routes import image_status
from app.api.routes import admin
from app.api.routes import reports



router =APIRouter()
router.include_router(users.router, tags=["Users"], prefix="/user")

router.include_router(user_type.router, tags=["UsersType"], prefix="/user_type")
router.include_router(image_status.router, tags=["Image Status"], prefix="/imageStatus")
router.include_router(admin.router, tags=["Admin"], prefix="/admin")
router.include_router(automations.router, tags=[
                      "Automations"], prefix="/automation")
router.include_router(reports.router, tags=["Reports"], prefix="/reports")


