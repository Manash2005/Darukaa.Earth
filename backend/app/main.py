from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db

from app.api.router import api_router

app = FastAPI(title="Darukaa.Earth API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Darukaa.Earth API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/test-postgis")
def test_postgis(db: Session = Depends(get_db)):
    """
    Temporary endpoint to test PostGIS functionality.
    1. Creates a sample polygon using ST_GeomFromText
    2. Calculates its area in square meters using ST_Area with Geography cast (since it's SRID 4326)
    3. Converts it to GeoJSON using ST_AsGeoJSON
    """
    query = text("""
        SELECT 
            ST_AsGeoJSON(ST_GeomFromText('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', 4326)) as geojson,
            ST_Area(ST_GeomFromText('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', 4326)::geography) as area_sqm
    """)
    result = db.execute(query).fetchone()
    
    return {
        "status": "success",
        "message": "PostGIS is working properly!",
        "geojson": result.geojson,
        "area_sqm": result.area_sqm
    }
