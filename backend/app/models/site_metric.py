import uuid
from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base

class SiteMetric(Base):
    __tablename__ = "site_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    recorded_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    carbon_value = Column(Float, nullable=True)
    biodiversity_value = Column(Float, nullable=True)

    site = relationship("Site", back_populates="metrics")
