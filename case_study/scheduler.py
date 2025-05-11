from apscheduler.schedulers.background import BackgroundScheduler
from src.scraper import scrape_and_save

def start_scheduler():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(scrape_and_save, "interval", hours=24)
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
