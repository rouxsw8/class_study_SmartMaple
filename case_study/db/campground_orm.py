from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text
from database import Base

class CampgroundORM(Base):
    __tablename__ = "campgrounds"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    region_name = Column(String)
    administrative_area = Column(String)
    nearest_city_name = Column(String)
    accommodation_type_names = Column(Text)  # JSON string or comma-separated
    bookable = Column(Boolean)
    camper_types = Column(Text)              # JSON string or comma-separated
    operator = Column(String)
    photo_url = Column(String)
    photo_urls = Column(Text)                # JSON string or comma-separated
    photos_count = Column(Integer)
    rating = Column(Float)
    reviews_count = Column(Integer)
    slug = Column(String)
    price_low = Column(Float)
    price_high = Column(Float)
    availability_updated_at = Column(DateTime)
    address = Column(Text)  # BONUS FIELD
