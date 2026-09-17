from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from app.schemas.geojson import GeoJSONPolygon

class SiteBase(BaseModel):
    name: str
    description: Optional[str] = None

class SiteCreate(SiteBase):
    geometry: GeoJSONPolygon

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    geometry: Optional[GeoJSONPolygon] = None

class SiteResponse(SiteBase):
    id: UUID
    project_id: UUID
    geometry: GeoJSONPolygon
    area_hectares: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
