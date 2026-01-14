from wiki_scraper.scraper.base_scraper import BasicScraper
import re 
from bs4 import BeautifulSoup
import pandas as pd

class TolkienGatewayScraper(BasicScraper):
    def __init__(self):
        super().__init__(
            base_URL="https://tolkiengateway.net/wiki/",
            request_timeout=30,
            user_agent="TolkienGatewayScraper 1.0 (college project)",
            rate_limit=0.5
        )

    def make_url(self, phrase):
        url = self.base_URL
        new_phrase = phrase.replace(" ", "_")
        url = url + new_phrase
        return url
    
    def get_first_paragraph(self, phrase):
        soup = self.fetch_page(phrase)

        content = soup.find("div", id="mw-content-text")

        for p in content.find_all("p"):
            if p.find_parent("blockquote"):
                continue

            text = p.get_text()
            if text:
                return text


    


    def get_all_text(self, phrase):
        pass 

    def get_tables(self, phrase):
        soup = self.fetch_page(phrase)
        tables = soup.find_all('table')
        
        dataframes = []
        for table in tables:
            rows = table.find_all('tr')
            table_data = []
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                cell_data = [cell.get_text(strip=True) for cell in cells]
                if cell_data:
                    table_data.append(cell_data)
            
            if table_data:
                df = pd.DataFrame(table_data)
                dataframes.append(df)
        
        return dataframes

    def get_nth_table(self, phrase, n=0):
        tables = self.get_tables(phrase)
        if 0 <= n < len(tables):
            return tables[n]
        return None