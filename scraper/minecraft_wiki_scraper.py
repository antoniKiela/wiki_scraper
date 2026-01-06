from wiki_scraper.scraper.base_scraper import BasicScraper
import re 
from bs4 import BeautifulSoup

class MinecraftWikiScraper(BasicScraper):
    def __init__(self):
        super().__init__(
            base_URL="https://minecraft.wiki/",
            request_timeout=30,
            user_agent="MinecraftWikiScraper 1.0 (college project)",
            rate_limit=0.5
        )

    def make_url(self, phrase):
        url = self.base_URL + "w/"
        new_phrase = phrase.replace(" ", "_")
        url = url + new_phrase
        return url
    
    def get_first_paragraph(self, phrase):
        soup = self.fetch_page(phrase)

        meta_description = soup.find('meta', attrs={'name': 'description'})
        return meta_description.get('content')

    def get_all_text(self, phrase):
        pass 

    def get_tables(self, phrase):
        pass 

    def get_nth_table(self, phrase):
        pass 

    def extract_table_data(self, table):
        pass 