"""
Main entrypoint for The Dyrt web scraper case study.

Usage:
    The scraper can be run directly (`python main.py`) or via Docker Compose (`docker compose up`).

If you have any questions in mind you can connect to me directly via info@smart-maple.com
"""
from fastapi import FastAPI
from src.scraper import data  # Import the 'data' function from scraper

app = FastAPI()

@app.get("/scrape")
async def scrape():
    camp_data = data()  # Call the 'data' function
    return {"message": camp_data["message"]}

if __name__ == "__main__":
    print("Hello Smart Maple!")
