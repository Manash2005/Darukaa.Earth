from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: UUID):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

def create_project(db: Session, project: ProjectCreate, user_id: UUID):
    db_project = Project(
        name=project.name,
        description=project.description,
        created_by=user_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: UUID, project_update: ProjectUpdate):
    db_project = get_project(db, project_id)
    
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
        
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: UUID):
    db_project = get_project(db, project_id)
    db.delete(db_project)
    db.commit()
    return {"ok": True}
