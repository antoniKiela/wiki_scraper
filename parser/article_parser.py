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

    def get_table(self, phrase, number, first_row_is_header, use_local_html_file_instead=False):
        soup = self.get_soup(phrase, use_local_html_file_instead)

        df = self.scraper.get_nth_table(soup, number - 1)

        # Automatic table parsing by pd.read_html for this website creates correct column heads so no need for implementing first_row_is_header

        return df
