from abc import ABC, abstractmethod
import time

import requests
from bs4 import BeautifulSoup

class BasicScraper(ABC):
    def __init__(self, base_URL, request_timeout, user_agent, rate_limit):
        self.base_URL = base_URL
        self.request_timeout = request_timeout
        self.user_agent = user_agent
        self.rate_limit = rate_limit

        self.session = requests.Session() 
        self.session.headers.update({
            'User-Agent' : self.user_agent
        })

        self.last_request_time = 0

    def wait_if_needed(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.rate_limit:
            time_to_wait = self.rate_limit - time_since_last
            time.sleep(time_to_wait) 

        self.last_request_time = time.time()

    def fetch_page(self, phrase):
        self.wait_if_needed()

        url = self.make_url(phrase)

        try:
            response = self.session.get(
                url, 
                timeout=self.request_timeout
            )
            response.raise_for_status()

            return BeautifulSoup(response.content, 'html.parser')
        
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Can't download the site {url}: {e}")

    def close(self):
        if self.session:
            self.session.close()

    # Converts phrase to full URL of the article
    @abstractmethod
    def make_url(self, phrase):
        pass

    # Returns text of first paragraph
    @abstractmethod
    def get_first_paragraph(self, phrase):
        pass 

    # Returns all of the text in article
    @abstractmethod
    def get_all_text(self, phrase):
        pass 

    # Returns all of the tables in the article in good format
    @abstractmethod
    def get_tables(self, phrase):
        pass 

    # Return n-th table in good format
    @abstractmethod
    def get_nth_table(self, phrase):
        pass 

    @abstractmethod
    def get_all_links(self, soup):
        pass

    @abstractmethod
    def get_language(self):
        pass

        