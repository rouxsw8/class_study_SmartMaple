from sqlalchemy import Column, Float, Integer, String, Text
from database import Base
import log_config


class Campground(Base):
    __tablename__ = "campgrounds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(Text) 
    amenities = Column(Text)
    rating = Column(Float)
    description = Column(Text)
    url = Column(String)
