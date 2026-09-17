from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class SiteMetricBase(BaseModel):
    carbon_value: Optional[float] = None
    biodiversity_value: Optional[float] = None

class SiteMetricCreate(SiteMetricBase):
    pass

class SiteMetricResponse(SiteMetricBase):
    id: UUID
    site_id: UUID
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)
