"""
Module to handle the HTML data acquisition from websites
"""
from bs4 import BeautifulSoup
import urllib.request

class HtmlAPI(object):
    """
    DESCRIPTION: module to fetch html from website
    ATTRIBUTES:
        - url (str)
    METHODS:
        - fetch_html
    """
    def __init__(self):
        self.url = 'https://www.google.com/'

    def fetch_html(self, uri=''):
        """
        DESCRIPTION: get HTML from given url
        INPUT: uri (str/optional)
        OUTPUT: page_html (bs4)
        """
        fetch_url = self.url + uri

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        header = {'User-Agent': user_agent}

        request = urllib.request.Request(fetch_url, headers=header)
        response = urllib.request.urlopen(request)
        page_html = BeautifulSoup(response)

        return page_html
