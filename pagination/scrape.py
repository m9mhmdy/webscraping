"""Scrape data from paginated websites"""
import helpers

### Configuration ###
# Create a new scraping session
session = helpers.ScrapingSession()

# The first page (in the pagination section) URL
HOMEPAGE = ''

# A prefix that maps relative URLs to absolute ones
DOMAIN = ''

# The XPath selectors used to extract
# the URLs of both: pages & items on each page
NAV_SELECTOR   = ''
ITEMS_SELECTOR = ''


def get_pages_urls():
    """Return a list of the website pages URLs."""
    # Parse the home page
    tree  = session.make_tree(HOMEPAGE)
    
    # Handle any parsing errors
    if tree is None:
        return None

    # Extract the URLs using lxml and XPath
    pages = [HOMEPAGE] + \
            [DOMAIN+a for a in tree.xpath(NAV_SELECTOR, smart_strings=False)]

    return pages

def extract_items_urls(page):
    """Return a list of items URLs found at `page`."""
    # Parse the page
    tree = session.make_tree(page)

    # Handle any parsing errors
    if tree is None:
        return None

    # Extract the URLs using lxml and XPath
    items = [DOMAIN+a for a in tree.xpath(ITEMS_SELECTOR, smart_strings=False)]

    return items

def scrape_item_data(item):
    """Return a list of data fields extracted from `item` page"""
    data_dict = {
        'field1':'xpathselector',
        'field2':'xpathselector',
        'field3':'xpathselector',
        'field4':'xpathselector',
        'field5':'xpathselector'
    }

    # Parse the item page
    tree = session.make_tree(item)

    # Handle any parsing errors
    if tree is None:
        return None

    # Extract the data fields using lxml and XPath
    for field, selector in data_dict.items():
        try:
            field_data = tree.xpath(selector, smart_strings=False)[0].strip()
            data_dict[field] = field_data
        except:
            # Handle any missing data fields
            data_dict[field] = ''

    return list(data_dict.values())
