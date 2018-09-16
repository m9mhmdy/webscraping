"""Useful functions to help with web scraping tasks"""
import requests
from lxml import etree

### Configuration ###
HEADERS = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}


class ScrapingSession(requests.Session):
    def __init__(self):
        requests.Session.__init__(self)

    def send_get(self, url):
        """Request webpages.

        Send a GET request to a webpage and return the response object.

        Parameters
        ----------
        url : str
            The webpage URL
        
        Returns
        -------
        requests.models.Response
            The response object
        """
        try:
            response = self.get(url, headers=HEADERS, timeout=20)
        except:
            # Handle timeout exceptions
            try:
                print(f"The request to ({url}) wasn't successful\nLet's try again")
                response = self.get(url, headers=HEADERS, timeout=20)
                print("Fixed it==========\n")
            except:
                print("Still not successful\nSkipping that url\n==========\n")
                return None

        # Handle non-valid responses
        status_code = response.status_code      # issue of 404, 302 ..etc
        content     = response.content.strip()  # issue of '\n\n' pages
        if not content or status_code!=200:
            response = None

        return response

    def make_tree(self, url):
        """Parse webpages.

        Parse a webpage source using lxml and return the parse tree.

        Parameters
        ----------
        url : str
            The webpage URL
        
        Returns
        -------
        lxml.etree._Element
            The parse tree
        """
        # Request the webpage source
        response = self.send_get(url)

        # Handle non-valid responses
        if response is None:
            return None

        # Parse the response content
        try:
            # If XML
            tree = etree.fromstring(response.content)
        except:
            try:
                # If HTML
                tree = etree.HTML(response.content)
            except:
                tree = None

        return tree
