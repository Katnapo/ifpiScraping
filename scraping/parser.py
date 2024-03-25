from bs4 import BeautifulSoup

def extract_scrape_target(element, scrape_target):
    """
    Extract the intended scrape target from an HTML element.

    Args:
        element: The HTML element to extract the scrape target from.
        scrape_target: The scrape target attribute ('text', 'href', or a list of these).

    Returns:
        The extracted scrape target value, or None if not found.
    """
    if scrape_target == 'text':
        return element.text.strip()
    elif scrape_target == 'href':
        return element.get('href')
    elif isinstance(scrape_target, list):
        return [element.text.strip(), element.get('href')]
    else:
        return None

def find_elements(html, element_dict):
    """
    Find HTML elements based on the provided dictionary structure.

    Args:
        html: The HTML content to search in.
        element_dict: The dictionary containing the search criteria.

    Returns:
        The found elements or extracted values based on the dictionary structure.
    """
    soup = BeautifulSoup(html, 'html.parser')
    element_type = element_dict['type']
    contains_attrs = attribute_builder(element_dict)
    special = element_dict.get('special')
    string_search = element_dict.get('text')

    elements = soup.find_all(element_type, attrs=contains_attrs, string=string_search)

    if special == 'many':
        results = []
        if element_dict.get('inner'):
            for element in elements:
                inner_data = element_dict['inner']
                inner_html = str(element)
                result = find_elements(inner_html, inner_data)
                if result:
                    results.append(result)
        else:
            for element in elements:
                results.append(extract_scrape_target(element, element_dict.get('scrape_target')))
        return results

    inner_data = element_dict.get('inner')
    if inner_data:
        return find_elements(str(soup), inner_data)
    else:
        if elements:
            element = elements[0]
            scrape_target = element_dict.get('scrape_target')
            return extract_scrape_target(element, scrape_target)

    return None

def attribute_builder(element_dict):
    """
    Build a dictionary of attributes to search for based on the provided dictionary structure.

    Args:
        element_dict: The dictionary containing the search criteria.

    Returns:
        A dictionary of attributes to search for.
    """
    return_data = {}
    for attr in element_dict.get('contains'):
        if attr == element_dict.get('scrape_target') or attr == 'text':
            continue
        return_data[attr] = element_dict.get(attr)
    return return_data