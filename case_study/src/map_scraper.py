import concurrent.futures
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the geolocator
geolocator = Nominatim(user_agent="campground_scraper")

# Function to get the address from latitude and longitude
def get_address(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language='en', exactly_one=True)
        return location.address if location else "Address not found"
    except Exception as e:
        print(f"Error while getting address: {e}")
        return "Address not found"

# Function to scrape campgrounds from a given URL (page)
def get_campgrounds_from_map(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    results = []

    try:
        # Wait for the search result cards to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="search-result-card"]'))
        )

        cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="search-result-card"]')

        for card in cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, "h2").text
                url = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                # Scrape lat and long from the card (you might need to adjust this part depending on the structure of the page)
                latitude = float(card.get_attribute('data-latitude'))  # Adjust this according to the actual data attributes on the card
                longitude = float(card.get_attribute('data-longitude'))  # Adjust this according to the actual data attributes

                # Find the address based on latitude and longitude
                address = get_address(latitude, longitude)

                results.append({
                    "name": name,
                    "url": url,
                    "latitude": latitude,
                    "longitude": longitude,
                    "address": address
                })
            except Exception as e:
                print("Card error:", e)
    except Exception as e:
        print(f"Error loading page {url}: {e}")
    finally:
        driver.quit()

    return results

# Function to scrape multiple pages concurrently using ThreadPoolExecutor
def scrape_multiple_pages(urls):
    # Using ThreadPoolExecutor to scrape pages concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_campgrounds_from_map, url) for url in urls]

        all_results = []
        for future in concurrent.futures.as_completed(futures):
            all_results.extend(future.result())

    return all_results

if __name__ == "__main__":
    # Example URLs to scrape different pages/regions
    urls = [
        'https://thedyrt.com/search?filters=%7B"bbox"%3A"32.708%2C39.815%2C33.072%2C39.986"%7D',
        'https://thedyrt.com/search?filters=%7B"bbox"%3A"33.072%2C39.986%2C33.436%2C40.157"%7D',
        'https://thedyrt.com/api/v6/location-search-results?filter%5Bsearch%5D%5Bair_quality%5D=any&filter%5Bsearch%5D%5Bbbox%5D=32.937%2C39.898%2C32.942%2C39.9&filter%5Bsearch%5D%5Bdrive_time%5D=any&filter%5Bsearch%5D%5Belectric_amperage%5D=any&filter%5Bsearch%5D%5Bmax_vehicle_length%5D=any&filter%5Bsearch%5D%5Bprice%5D=any&filter%5Bsearch%5D%5Brating%5D=any&page%5Bnumber%5D=1&page%5Bsize%5D=500&sort=recommended',
        'https://thedyrt.com/api/v6/location-search-results?filter%5Bsearch%5D%5Bair_quality%5D=any&filter%5Bsearch%5D%5Bbbox%5D=32.937%2C39.898%2C32.942%2C39.9&filter%5Bsearch%5D%5Bdrive_time%5D=any&filter%5Bsearch%5D%5Belectric_amperage%5D=any&filter%5Bsearch%5D%5Bmax_vehicle_length%5D=any&filter%5Bsearch%5D%5Bprice%5D=any&filter%5Bsearch%5D%5Brating%5D=any&page%5Bnumber%5D=1&page%5Bsize%5D=500&sort=recommended'
    ]

    campgrounds = scrape_multiple_pages(urls)
    print(f"Scraped {len(campgrounds)} campgrounds")
