# main.py
from service import ScraperManager
from database import get_db

def main():
    scraper_manager = ScraperManager()
    db = next(get_db())
    song_data_list = scraper_manager.scrape_50_indexes(db)

    # Process the scraped data as needed
    for index, song_data in enumerate(song_data_list):
        print(f"Data from index page {index}:")
        for song in song_data:
            print(f"Title: {song['title']}")
            print(f"Date: {song['date']}")
            print(f"Download Link: {song['download_link']}")
            print(f"URL: {song['url']}")
            print("---")

if __name__ == "__main__":
    main()