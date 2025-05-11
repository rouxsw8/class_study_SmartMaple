from sqlalchemy.orm import Session
from models.campground import Campground
from db.campground_orm import CampgroundORM
from database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import logging
from src.map_scraper import get_campgrounds_from_map

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_and_save():
    data = get_campgrounds_from_map()
    db: Session = SessionLocal()

    for item in data:
        try:
            campground = Campground(name=item["name"], url=item["url"], latitude=item["latitude"], 
                        longitude=item["longitude"], address=item["address"])
            existing = db.query(CampgroundORM).filter_by(url=campground.url).first()

            if existing:
                existing.name = campground.name
                logging.info(f"Updated: {existing.name}")
            else:
                new_entry = CampgroundORM(name=campground.name, url=campground.url)
                db.add(new_entry)
                logging.info(f"Added: {new_entry.name}")

        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemy Error: {e}")
            db.rollback()
        except Exception as e:
            logging.error(f"Error: {e}")
            db.rollback()

    try:
        db.commit()
    except SQLAlchemyError as e:
        logging.error(f"Commit Error: {e}")
        db.rollback()
    finally:
        db.close()

def data():
    try:
        scrape_and_save()  # Run the scraper and save data
        return {"message": "Scraping completed successfully."}
    except Exception as e:
        return {"message": f"Scraping failed with error: {e}"}
