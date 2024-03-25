import concurrent

import requests
from bs4 import BeautifulSoup
from constants import Constants
from concurrent.futures import ThreadPoolExecutor, as_completed

class MusicScraper:

    def __init__(self, url=Constants.homeUrl):
        self.get_soup(url)

    def get_soup(self, url):
        # Fetch the content from the URL and create a BeautifulSoup object
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get the attributes from the JSON 'contains' line
    def attribute_builder(self, element_dict):

        # Extracts the attributes to search for from the JSON constant
        return_data = {}
        for attr in element_dict.get('contains'):

            # Note you cant add text as an attribute to search for
            # You can't search for the scrape_target attribute as it is the variable to be returned
            if attr == element_dict.get("scrape_target") or attr == "text":
                continue

            return_data[attr] = element_dict.get(attr)

        return return_data
    
    # Get the intended scrape element
    def extract_scrape_target(self, element, scrape_target):

        if scrape_target == 'text':
            return element.text.strip()
        elif scrape_target == 'href':
            return element.get('href')
        elif isinstance(scrape_target, list):
            return [element.text.strip(), element.get('href')]
        else:
            return None

    def find_element(self, element_dict):

        # Collect information at this JSON level
        element_type = element_dict['type']
        contains_attrs = self.attribute_builder(element_dict)
        special = element_dict.get('special')
        string_search = None

        # If the element has text, and that text is not None, then that text can be searched for
        if element_dict.get("text"):
            string_search = element_dict.get("text")

        # Find elements based on the specified attributes
        elements = self.soup.find_all(element_type, attrs=contains_attrs, string=string_search)

        # Handle cases where multiple elements need to be processed i.e on home page with list of songs
        if special == 'many':
            results = []
            # Specifically for home screen where at this point it is not at the bottom element

            if element_dict.get("inner"):

                for element in elements:
                    inner_data = element_dict['inner']

                    # Important line here to set the soup to the current element being recursed over.
                    self.soup = element

                    result = self.find_element(inner_data)

                    if result:
                        results.append(result)

            # Whereas this accounts for both the download links on song page and the maximum page number
            else:
                for element in elements:
                    results.append(self.extract_scrape_target(element, element_dict.get("scrape_target")))

            return results

        # Recursively process inner elements
        inner_data = element_dict.get('inner')
        if inner_data:
            return self.find_element(inner_data)

        else:
            # If this else is reached, it means that the recursion has reached the bottom of the dictionary and now the
            # target can be scraped.
            if elements:
                element = elements[0]
                scrape_target = element_dict.get('scrape_target')
                return self.extract_scrape_target(element, scrape_target)

        return None

    # General entry point for class to scrape a page. This is the only method that should be called from outside the class
    def general_scrape(self, element_dict, reset=False, url=Constants.homeUrl):

        # Tells the class to reset the soup object to the new URL
        if reset:
            self.get_soup(url)

        return self.find_element(element_dict)


class ScraperManager:

    # Create a scrape object
    def __init__(self):
        self.scraper = MusicScraper()

    # Scrape the home page for the song list data and the maximum page number
    def scrape_home_page(self, scrapingDict=Constants.scrapingDict['HomePage']):

        maxPageData = self.scraper.general_scrape(scrapingDict['PageNavigationData'])
        homeURLData = self.scraper.general_scrape(scrapingDict['SongListData'])

        return {
            "indexPageURLs": homeURLData,
            "maxPage": max([int(i.replace(',', '')) for i in maxPageData if i.replace(',', '').isdigit()])
        }

    def scrape_index_page(self, indexURL, scrapingDict=Constants.scrapingDict['HomePage']):

        indexPageData = self.scraper.general_scrape(scrapingDict['SongListData'], reset=True, url=indexURL)
        return {
            "indexPageURLs": indexPageData
        }
    def scrape_song_page(self, songURL, scrapingDict=Constants.scrapingDict['SongPage']):

        titleData = self.scraper.general_scrape(scrapingDict['TitleData'], reset=True, url=songURL)
        dateData = self.scraper.general_scrape(scrapingDict['DateData'])
        downloadLinkData = self.scraper.general_scrape(scrapingDict['DownloadLinkData'])

        return {
            "title": titleData,
            "date": dateData,
            "downloadLink": downloadLinkData,
            "url" : songURL
        }


    def scrape_index_songs(self, urls, scrapingDict=Constants.scrapingDict['SongPage']):

        songData = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.scrape_song_page, url, scrapingDict) for url in urls]

            for future in concurrent.futures.as_completed(futures):
                songData.append(future.result())

        return songData

    def flatten_quick_scrape(self, scrapingDict):

        flattened_dict = {}
        for key, value in scrapingDict.items():
            if isinstance(value, dict):
                if "quick_scrape_val" in value:
                    flattened_dict.update(value)
                else:
                    flattened_inner = self.flatten_quick_scrape(value)
                    flattened_dict[key] = flattened_inner
            else:
                flattened_dict[key] = value
        return flattened_dict

    def scrape_50_indexes(self, quick_scrape=True):

        # Method to cut decscending through the JSON dictionary, instead look for first instance of "quick_scrape_val"
        # and scrape using the dictionary at that level. If quick_scrape_val is set to many and the dict doesn't
        # contain a special=many, add a special=many to the dictionary
        scrapingDict = Constants.scrapingDict
        if quick_scrape:

            for page in scrapingDict:
                for detail in scrapingDict[page]:
                    scrapingDict[page][detail] = self.flatten_quick_scrape(scrapingDict[page][detail])

        homeIndexURLs = self.scrape_home_page(scrapingDict['HomePage'])
        songData = self.scrape_index_songs(homeIndexURLs['indexPageURLs'], scrapingDict['SongPage'])
        songDataList = [songData]

        # Create a thread pool
        with ThreadPoolExecutor() as executor:
            # Submit tasks for scraping index pages
            futures = [executor.submit(self.scrape_index_page, f"{Constants.homeUrl}/page/{i}", scrapingDict['HomePage']) for i in range(2, 51)]

            # Collect results as tasks complete
            for future in as_completed(futures):
                songURLs = future.result()['indexPageURLs']
                songData = self.scrape_index_songs(songURLs, scrapingDict['SongPage'])
                songDataList.append(songData)

        return songDataList

# Example usage

scraper_manager = ScraperManager()
scraper_manager.scrape_50_indexes()





