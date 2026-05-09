from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from app.config import settings
from app.db import Base, engine
from app.routers.api_reports import router as api_reports_router
from app.routers.web import router as web_router

app = FastAPI(title=settings.app_title)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(web_router)
app.include_router(api_reports_router)
