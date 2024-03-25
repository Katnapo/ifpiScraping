import concurrent.futures
from utils import fetch_html
from parser import find_elements
from constants import Constants
from database import save_song_data, save_max_page  # Import the save_song_data function

class MusicScraper:
    def __init__(self, url=Constants.homeUrl):
        self.html = fetch_html(url)

    def general_scrape(self, element_dict, reset=False, url=Constants.homeUrl):
        """
        General entry point for scraping a page based on the provided dictionary structure.

        Args:
            element_dict: The dictionary containing the search criteria.
            reset (optional): Whether to reset the HTML content by fetching from a new URL. Defaults to False.
            url (optional): The URL to fetch HTML from if reset is True. Defaults to Constants.homeUrl.

        Returns:
            The found elements or extracted values based on the dictionary structure.
        """
        if reset:
            self.html = fetch_html(url)
        return find_elements(self.html, element_dict)

class ScraperManager:
    def __init__(self):
        self.scraper = MusicScraper()

    def scrape_home_page(self, scraping_dict=Constants.scraping_dict['HomePage']):
        """
        Scrape the home page for the song list data and maximum page number.

        Args:
            scraping_dict (optional): The dictionary containing the search criteria for the home page.
                Defaults to Constants.scraping_dict['HomePage'].

        Returns:
            A dictionary containing the index page URLs and the maximum page number.
        """
        max_page_data = self.scraper.general_scrape(scraping_dict['PageNavigationData'])
        home_url_data = self.scraper.general_scrape(scraping_dict['SongListData'])

        max_page = max([int(i.replace(',', '')) for i in max_page_data if i.replace(',', '').isdigit()])

        return {
            "index_page_urls": home_url_data,
            "max_page": max_page
        }

    def scrape_index_page(self, index_url, scraping_dict=Constants.scraping_dict['HomePage']):
        """
        Scrape an index page for the song URLs.

        Args:
            index_url: The URL of the index page to scrape.
            scraping_dict (optional): The dictionary containing the search criteria for the index page.
                Defaults to Constants.scraping_dict['HomePage'].

        Returns:
            A dictionary containing the song URLs on the index page.
        """
        index_page_data = self.scraper.general_scrape(scraping_dict['SongListData'], reset=True, url=index_url)
        return {
            "index_page_urls": index_page_data
        }

    def scrape_song_page(self, song_url, scraping_dict=Constants.scraping_dict['SongPage']):
        """
        Scrape a song page for the title, date, and download link.

        Args:
            song_url: The URL of the song page to scrape.
            scraping_dict (optional): The dictionary containing the search criteria for the song page.
                Defaults to Constants.scraping_dict['SongPage'].

        Returns:
            A dictionary containing the song title, date, download link, and URL.
        """
        title_data = self.scraper.general_scrape(scraping_dict['TitleData'], reset=True, url=song_url)
        date_data = self.scraper.general_scrape(scraping_dict['DateData'])
        download_link_data = self.scraper.general_scrape(scraping_dict['DownloadLinkData'])

        return {
            "title": title_data,
            "date": date_data,
            "download_link": download_link_data,
            "url": song_url
        }

    def scrape_index_songs(self, urls, scraping_dict=Constants.scraping_dict['SongPage']):
        """
        Scrape multiple song pages in parallel.

        Args:
            urls: A list of song page URLs to scrape.
            scraping_dict (optional): The dictionary containing the search criteria for the song pages.
                Defaults to Constants.scraping_dict['SongPage'].

        Returns:
            A list of dictionaries containing the scraped song data.
        """
        song_data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.scrape_song_page, url, scraping_dict) for url in urls]

            for future in concurrent.futures.as_completed(futures):
                song_data.append(future.result())

        return song_data

    def scrape_50_indexes(self, quick_scrape=True):
        """
        Scrape the home page and the first 50 index pages for song data.

        Args:
            quick_scrape (bool, optional): Whether to use a quick scrape method. Defaults to True.

        Returns:
            List[Dict[str, Any]]]: A list of dicts containing the scraped song data from the home page
                and the first 50 index pages.
        """

        scraping_dict = Constants.scraping_dict
        if quick_scrape:
            for page in scraping_dict:
                for detail in scraping_dict[page]:
                    scraping_dict[page][detail] = flatten_quick_scrape(scraping_dict[page][detail])

        home_index_urls = self.scrape_home_page(scraping_dict['HomePage'])
        song_data = self.scrape_index_songs(home_index_urls['index_page_urls'], scraping_dict['SongPage'])
        save_song_data(song_data)  # Save the song data to the database
        save_max_page(home_index_urls['max_page'])
        song_data_list = [song_data]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.scrape_index_page, f"{Constants.homeUrl}/page/{i}", scraping_dict['HomePage']) for
                i in range(2, 51)]

            for future in concurrent.futures.as_completed(futures):
                song_urls = future.result()['index_page_urls']
                song_data = self.scrape_index_songs(song_urls, scraping_dict['SongPage'])
                save_song_data(song_data)  # Save the song data to the database
                song_data_list.append(song_data)

        return song_data_list

def flatten_quick_scrape(scraping_dict):
    """
    Flatten a nested dictionary structure by extracting the "quick_scrape_val" values.

    Args:
        scraping_dict: The nested dictionary structure to flatten.

    Returns:
        A flattened dictionary containing the "quick_scrape_val" values.
    """
    flattened_dict = {}
    for key, value in scraping_dict.items():
        if isinstance(value, dict):
            if "quick_scrape_val" in value:
                flattened_dict.update(value)
            else:
                flattened_inner = flatten_quick_scrape(value)
                flattened_dict[key] = flattened_inner
        else:
            flattened_dict[key] = value
    return flattened_dict