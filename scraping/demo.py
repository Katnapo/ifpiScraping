# main.py
from scraping.service import ScraperManager
from scraping.database import get_db

def main():
    scraper_manager = ScraperManager()
    db = next(get_db())
    scraper_manager.scrape_50_indexes(db)

if __name__ == "__main__":
    main()