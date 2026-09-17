from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.site import SiteCreate, SiteResponse, SiteUpdate
from app.services import site_service

router = APIRouter()

# Note: sites are typically nested under projects in standard REST
# e.g., /projects/{project_id}/sites
# We'll expose them both under /projects/{project_id}/sites (handled in project router or top-level router)
# and flat /sites for independent access.

@router.get("/{site_id}", response_model=SiteResponse)
def get_site(site_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a specific site and its geometry."""
    return site_service.get_site(db, site_id)

@router.put("/{site_id}", response_model=SiteResponse)
def update_site(site_id: UUID, site_update: SiteUpdate, db: Session = Depends(get_db)):
    """Update a specific site."""
    return site_service.update_site(db, site_id, site_update)

@router.delete("/{site_id}")
def delete_site(site_id: UUID, db: Session = Depends(get_db)):
    """Delete a specific site."""
    return site_service.delete_site(db, site_id)
