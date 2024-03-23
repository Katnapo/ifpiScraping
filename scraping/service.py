import requests
from bs4 import BeautifulSoup

class Constants:
    # Scraping constants (JSON data)
    scrapingDict = {
        # ... (same as before) ...
    }

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(url)

    def get_soup(self, url):
        # Fetch the content from the URL and create a BeautifulSoup object
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def find_element(self, element_data):
        contains = element_data.get('contains')
        element_type = element_data['type']
        special = element_data.get('special')

        # Find elements based on the specified attributes
        if contains:
            elements = self.soup.find_all(element_type, {k: v for k, v in element_data.items() if k in contains})
        else:
            elements = self.soup.find_all(element_type)

        # Handle cases where multiple elements need to be processed
        if special == 'many':
            results = []
            for element in elements:
                inner_data = element_data['inner']
                result = self.find_element(inner_data)
                if result:
                    results.extend(result)
            return results

        # Handle cases where elements need to be processed after a specific element
        elif special == 'after':
            results = []
            for inner_element_data in element_data['inner']:
                result = self.find_element(inner_element_data)
                if result:
                    results.extend(result)
            return results

        # Process the found elements
        elif elements:
            element = elements[0]
            scrape_target = element_data.get('scrape_target')
            if scrape_target == 'text':
                return element.text.strip()
            elif scrape_target == 'href':
                return element.get('href')
            elif isinstance(scrape_target, list):
                return [element.text.strip(), element.get('href')]

            # Recursively process inner elements
            inner_data = element_data.get('inner')
            if inner_data:
                return self.find_element(inner_data)

        return None

    def scrape_song_page(self):
        song_page_data = Constants.scrapingDict['SongPage']

        # Scrape the song page data
        title = self.find_element(song_page_data['TitleData'])
        date = self.find_element(song_page_data['DateData'])
        download_link = self.find_element(song_page_data['DownloadLinkData'])

        return {
            'title': title,
            'date': date,
            'download_link': download_link
        }

    def scrape_home_page(self):
        home_page_data = Constants.scrapingDict['HomePage']

        # Scrape the home page data
        song_list = self.find_element(home_page_data['SongListData'])
        page_navigation = self.find_element(home_page_data['PageNavigationData'])

        return {
            'song_list': song_list,
            'page_navigation': page_navigation
        }

# Example usage
song_page_scraper = WebScraper('https://example.com/song-page')
song_page_data = song_page_scraper.scrape_song_page()
print(song_page_data)

home_page_scraper = WebScraper('https://example.com')
home_page_data = home_page_scraper.scrape_home_page()
print(home_page_data)