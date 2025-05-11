from sqlalchemy.orm import Session
from models.campground import Campground
from db.campground_orm import CampgroundORM
from database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import logging
from src.map_scraper import scrape_multiple_pages

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_and_save():
    # Example URLs to scrape different pages/regions
    urls = [
        'https://thedyrt.com/search?filters=%7B"bbox"%3A"32.708%2C39.815%2C33.072%2C39.986"%7D',
        'https://thedyrt.com/search?filters=%7B"bbox"%3A"33.072%2C39.986%2C33.436%2C40.157"%7D',
        'https://thedyrt.com/api/v6/location-search-results?filter%5Bsearch%5D%5Bair_quality%5D=any&filter%5Bsearch%5D%5Bbbox%5D=32.937%2C39.898%2C32.942%2C39.9&filter%5Bsearch%5D%5Bdrive_time%5D=any&filter%5Bsearch%5D%5Belectric_amperage%5D=any&filter%5Bsearch%5D%5Bmax_vehicle_length%5D=any&filter%5Bsearch%5D%5Bprice%5D=any&filter%5Bsearch%5D%5Brating%5D=any&page%5Bnumber%5D=1&page%5Bsize%5D=500&sort=recommended',
        'https://thedyrt.com/api/v6/location-search-results?filter%5Bsearch%5D%5Bair_quality%5D=any&filter%5Bsearch%5D%5Bbbox%5D=32.937%2C39.898%2C32.942%2C39.9&filter%5Bsearch%5D%5Bdrive_time%5D=any&filter%5Bsearch%5D%5Belectric_amperage%5D=any&filter%5Bsearch%5D%5Bmax_vehicle_length%5D=any&filter%5Bsearch%5D%5Bprice%5D=any&filter%5Bsearch%5D%5Brating%5D=any&page%5Bnumber%5D=1&page%5Bsize%5D=500&sort=recommended'
    ]

    data = scrape_multiple_pages(urls)
    db: Session = SessionLocal()

    for item in data:
        try:
            campground = Campground(
                name=item["name"],
                url=item["url"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                address=item["address"]
            )

            existing = db.query(CampgroundORM).filter_by(url=campground.url).first()

            if existing:
                existing.name = campground.name
                existing.latitude = campground.latitude
                existing.longitude = campground.longitude
                existing.address = campground.address
                logging.info(f"Updated: {existing.name}")
            else:
                new_entry = CampgroundORM(
                    name=campground.name,
                    url=campground.url,
                    latitude=campground.latitude,
                    longitude=campground.longitude,
                    address=campground.address
                )
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
