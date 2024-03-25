import requests
def fetch_html(url):
    """
    Fetch the HTML content from a given URL.

    Args:
        url: The URL to fetch HTML from.

    Returns:
        The HTML content of the fetched URL.

    Raises:
        requests.exceptions.RequestException: If an error occurs while fetching the URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        raise e