from fastapi import FastAPI
from app.api.routes.routes import router as global_router
from starlette.middleware.cors import CORSMiddleware
import starlette.responses as _responses
from app.database.sessions.session import engine
from app.database.sessions.session2 import engine2
from app.models import user
from app.models import citizens_manually_edited_images




user.Base.metadata.create_all(bind=engine)
citizens_manually_edited_images.Base2.metadata.create_all(bind=engine2)



def create_appication_instance()-> FastAPI:
    application = FastAPI(title="Image Enhancement", debug=True)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(global_router)
    
    return application


app = create_appication_instance()



@app.get('/')
async def root():
    return _responses.RedirectResponse("/docs'")