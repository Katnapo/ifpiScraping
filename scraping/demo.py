# main.py
from service import ScraperManager

def main():
    scraper_manager = ScraperManager()
    song_data_list = scraper_manager.scrape_50_indexes()

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