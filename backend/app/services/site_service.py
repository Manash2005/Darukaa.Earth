import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from fastapi import HTTPException
from app.models.site import Site
from app.models.project import Project
from app.schemas.site import SiteCreate, SiteUpdate

def get_sites(db: Session, project_id: UUID, skip: int = 0, limit: int = 100):
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # We query the Site model but also calculate area and geojson
    sites = db.query(
        Site, 
        func.ST_AsGeoJSON(Site.geometry).label("geojson"),
        func.ST_Area(func.ST_Transform(Site.geometry, 3857)).label("area_sqm")
    ).filter(Site.project_id == project_id).offset(skip).limit(limit).all()
    
    result = []
    for site, geojson, area_sqm in sites:
        site_dict = site.__dict__.copy()
        site_dict["geometry"] = json.loads(geojson)
        # Convert sqm to hectares
        site_dict["area_hectares"] = area_sqm / 10000 if area_sqm else None
        result.append(site_dict)
    
    return result

def get_site(db: Session, site_id: UUID):
    site_query = db.query(
        Site, 
        func.ST_AsGeoJSON(Site.geometry).label("geojson"),
        # We use ST_Transform to EPSG:3857 (pseudo-mercator) to approximate area in meters,
        # or use geography cast. Geography cast is more accurate.
        func.ST_Area(func.cast(Site.geometry, getattr(func, 'geography'))).label("area_sqm")
    ).filter(Site.id == site_id).first()
    
    if not site_query:
        raise HTTPException(status_code=404, detail="Site not found")
        
    site, geojson, area_sqm = site_query
    site_dict = site.__dict__.copy()
    site_dict["geometry"] = json.loads(geojson)
    site_dict["area_hectares"] = area_sqm / 10000 if area_sqm else None
    
    return site_dict

def create_site(db: Session, project_id: UUID, site: SiteCreate):
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    geojson_str = json.dumps(site.geometry.model_dump())
    
    db_site = Site(
        project_id=project_id,
        name=site.name,
        description=site.description,
        # Use ST_GeomFromGeoJSON to parse the string into PostGIS geometry
        geometry=func.ST_GeomFromGeoJSON(geojson_str)
    )
    
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    
    return get_site(db, db_site.id)

def update_site(db: Session, site_id: UUID, site_update: SiteUpdate):
    # Verify site exists
    db_site = db.query(Site).filter(Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    update_data = site_update.model_dump(exclude_unset=True)
    
    if "geometry" in update_data:
        geojson_str = json.dumps(update_data["geometry"])
        db_site.geometry = func.ST_GeomFromGeoJSON(geojson_str)
        del update_data["geometry"]
        
    for key, value in update_data.items():
        setattr(db_site, key, value)
        
    db.commit()
    
    return get_site(db, site_id)

def delete_site(db: Session, site_id: UUID):
    db_site = db.query(Site).filter(Site.id == site_id).first()
    if not db_site:
        raise HTTPException(status_code=404, detail="Site not found")
        
    db.delete(db_site)
    db.commit()
    return {"ok": True}
