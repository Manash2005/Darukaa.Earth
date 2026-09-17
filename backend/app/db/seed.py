import uuid
import json
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine

from app.models.user import User
from app.models.project import Project
from app.models.site import Site
from app.models.site_metric import SiteMetric
from sqlalchemy import func

def seed_db():
    print("Seeding database...")
    db = SessionLocal()
    
    # Check if dev user already exists
    dev_user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    dev_user = db.query(User).filter(User.id == dev_user_id).first()
    
    if not dev_user:
        print("Creating dev user...")
        dev_user = User(
            id=dev_user_id,
            name="Dev User",
            email="dev@darukaa.earth",
            password_hash="fakehash"
        )
        db.add(dev_user)
        db.commit()
    
    # Check if projects exist
    if db.query(Project).count() == 0:
        print("Creating sample projects...")
        project1 = Project(
            name="Amazon Forest Restoration",
            description="Restoring deforested areas in the Amazon basin",
            created_by=dev_user_id
        )
        db.add(project1)
        db.commit()
        db.refresh(project1)
        
        print("Creating sample sites...")
        geojson_str = json.dumps({
            "type": "Polygon",
            "coordinates": [[
                [-60.0, -3.0],
                [-59.9, -3.0],
                [-59.9, -2.9],
                [-60.0, -2.9],
                [-60.0, -3.0]
            ]]
        })
        
        site1 = Site(
            project_id=project1.id,
            name="Zone Alpha",
            description="Primary planting zone",
            geometry=func.ST_GeomFromGeoJSON(geojson_str)
        )
        db.add(site1)
        db.commit()
        db.refresh(site1)
        
        print("Creating sample metrics...")
        metric1 = SiteMetric(
            site_id=site1.id,
            carbon_value=125.5,
            biodiversity_value=8.4
        )
        db.add(metric1)
        db.commit()
        
    print("Seeding complete!")
    db.close()

if __name__ == "__main__":
    seed_db()
