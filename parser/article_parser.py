from wiki_scraper.scraper.base_scraper import BasicScraper
from bs4 import BeautifulSoup

class ArticleParser:
    def __init__(self, scraper):
        self.scraper = scraper 

    def get_soup(self, phrase, use_local_html_file_instead):
        if use_local_html_file_instead == True:
            with open(phrase, 'r', encoding='utf-8') as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, 'html.parser')
        else:
            soup = self.scraper.fetch_page(phrase)
        
        return soup

    def get_summary(self, phrase, use_local_html_file_instead=False):
        soup = self.get_soup(phrase, use_local_html_file_instead)

        return self.scraper.get_first_paragraph(soup)

