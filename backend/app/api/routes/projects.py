from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services import project_service
# Hardcoded user UUID for development until authentication is implemented
# This assumes the seed script creates a user with this ID
DEV_USER_ID = UUID("00000000-0000-0000-0000-000000000001")

router = APIRouter()

@router.get("", response_model=List[ProjectResponse])
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all projects."""
    return project_service.get_projects(db, skip=skip, limit=limit)

@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project. Unauthenticated for now (uses dev user ID)."""
    return project_service.create_project(db, project, user_id=DEV_USER_ID)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a specific project."""
    return project_service.get_project(db, project_id)

from app.schemas.site import SiteCreate, SiteResponse
from app.services import site_service

@router.get("/{project_id}/sites", response_model=List[SiteResponse])
def get_project_sites(project_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all sites belonging to a project."""
    return site_service.get_sites(db, project_id, skip=skip, limit=limit)

@router.post("/{project_id}/sites", response_model=SiteResponse, status_code=201)
def create_project_site(project_id: UUID, site: SiteCreate, db: Session = Depends(get_db)):
    """Create a new site (polygon) within a project."""
    return site_service.create_site(db, project_id, site)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: UUID, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    """Update a specific project."""
    return project_service.update_project(db, project_id, project_update)

@router.delete("/{project_id}")
def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    """Delete a specific project."""
    return project_service.delete_project(db, project_id)
