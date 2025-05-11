from database import engine
from db.campground_orm import CampgroundORM
from database import Base
import sys
print(sys.executable)

Base.metadata.create_all(bind=engine)
