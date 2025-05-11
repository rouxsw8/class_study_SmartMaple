"""
Main entrypoint for The Dyrt web scraper case study.

Usage:
    The scraper can be run directly (`python main.py`) or via Docker Compose (`docker compose up`).

If you have any questions in mind you can connect to me directly via info@smart-maple.com
"""
from fastapi import FastAPI
from src.scraper import data  # Import the 'data' function from scraper
from scheduler import start_scheduler

@app.on_event("startup")
def startup_event():
    start_scheduler()
    
app = FastAPI(title="Campground Scraper API")

@app.get("/scrape", summary="Trigger campground scraping", tags=["Scraping"])
async def scrape():
    camp_data = data()
    return {"message": camp_data["message"]}

if __name__ == "__main__":
    import uvicorn
    print("Hello Smart Maple!")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
