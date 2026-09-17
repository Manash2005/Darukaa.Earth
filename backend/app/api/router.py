from fastapi import APIRouter
from app.api.routes import projects, sites

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
