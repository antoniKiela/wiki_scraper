from wiki_scraper.scraper.base_scraper import BasicScraper
from bs4 import BeautifulSoup
from pathlib import Path
import json
import time

class ArticleParser:
    def __init__(self, scraper):
        self.scraper = scraper 

    def get_soup(self, phrase, use_local_html_file_instead):
        if use_local_html_file_instead == True:
            phrase = phrase + '.html'
            with open(phrase, 'r', encoding='utf-8') as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, 'html.parser')
        else:
            soup = self.scraper.fetch_page(phrase)
        
        return soup

    # --summary
    def get_summary(self, phrase, use_local_html_file_instead=False):
        soup = self.get_soup(phrase, use_local_html_file_instead)

        return self.scraper.get_first_paragraph(soup)

    # --table
    def get_table(self, phrase, number, first_row_is_header, use_local_html_file_instead=False):
        soup = self.get_soup(phrase, use_local_html_file_instead)

        df = self.scraper.get_nth_table(soup, number - 1)

        # Automatic table parsing by pd.read_html for this website creates correct column heads so no need for implementing first_row_is_header

        return df

    # --count-words
    def get_words(self, phrase, use_local_html_file_instead=False):
        soup = self.get_soup(phrase, use_local_html_file_instead)

        words = self.scraper.get_all_text(soup)
        counts = {}
        for w in words:
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1

        path = Path("./word-counts.json")
        if path.exists():
            total = json.loads(path.read_text(encoding="utf-8"))
        else:
            total = {}

        for w, c in counts.items(): 
            total[w] = total.get(w, 0) + c

        path.write_text( 
            json.dumps(total, ensure_ascii=False, indent=2), 
            encoding="utf-8"
        )

        return soup

    # --auto-count-words
    def get_words_many_times(self, phrase, depth, wait_time, use_local_html_file_instead=False):
        print(phrase.replace(" ", "_") + str(depth))
        soup = self.get_words(phrase, use_local_html_file_instead)
        links = self.scraper.get_all_links(soup)
        
        if depth == 0:
            return

        for link in links:
            time.sleep(wait_time)
            self.get_words_many_times(link.replace("/wiki/", ""), depth - 1, wait_time)
        
