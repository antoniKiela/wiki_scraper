from wiki_scraper.scraper.base_scraper import BasicScraper
import re 
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO ## bo df = pd.read_html(str(table))[0] bylo deprecated

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
    
    # --summary
    def get_first_paragraph(self, soup):
        content = soup.find("div", id="mw-content-text")

        for p in content.find_all("p"):
            if p.find_parent("blockquote"):
                continue

            text = p.get_text()
            if text:
                return text

    # --table --number
    def get_tables(self, soup):
        content = soup.find("div", id="mw-content-text")
        if not content:
            return []

        tables = content.find_all("table")

        dataframes = []
        for table in tables:
            try:
                df = pd.read_html(StringIO(str(table)))[0]
                dataframes.append(df)
            except ValueError:
                continue

        return dataframes

    def get_nth_table(self, soup, n=0):
        tables = self.get_tables(soup)

        if n < 0 or n >= len(tables):
            raise IndexError(
                f"Table index {n} out of range (found {len(tables)} tables)"
            )

        return tables[n]


    # --count-words
    def get_all_text(self, soup):
        content = soup.find("div", id="mw-content-text")
        text = content.get_text(separator=" ")
        words = re.findall(r"[A-Za-zÀ-ÿ]+", text.lower()) 
        # not .split because then 'Ring' and 'Ring:' gives two different words
        # This regex means "a string of at least one character without numbers, special characters etc."


        return words

    # --auto-count-words
    def get_all_links(self, soup):
        content = soup.find("div", id="mw-content-text")
        if not content:
            return []

        links = set()

        for a in content.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/wiki/") and ':' not in href[len("/wiki/"):]:
                links.add(href)

        return links

    # --analyze-relative-word-frequency
    def get_language(self):
        return 'en'

        