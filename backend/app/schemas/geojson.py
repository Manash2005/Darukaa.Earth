from typing import List, Literal, Any
from pydantic import BaseModel, Field, model_validator

class GeoJSONPolygon(BaseModel):
    """
    Schema for a valid GeoJSON Polygon.
    Coordinates must be a list of lists of coordinate pairs.
    """
    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[List[float]]]
    
    @model_validator(mode='after')
    def validate_coordinates(self) -> 'GeoJSONPolygon':
        if not self.coordinates:
            raise ValueError("Coordinates cannot be empty")
        # Ensure it's a closed polygon (first and last point same)
        for ring in self.coordinates:
            if len(ring) < 4:
                raise ValueError("A polygon ring must have at least 4 points")
            if ring[0] != ring[-1]:
                raise ValueError("First and last coordinate of a polygon ring must match to close it")
        return self
