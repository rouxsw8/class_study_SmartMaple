from pydantic import BaseModel

class CampgroundSchema(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: str
    amenities: str
    rating: float
    description: str
    url: str
