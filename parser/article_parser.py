from wiki_scraper.scraper.base_scraper import BasicScraper
from bs4 import BeautifulSoup
from pathlib import Path
import json
import time
from wordfreq import top_n_list, zipf_frequency
import matplotlib.pyplot as plt
import pandas as pd
import random

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
        
    def get_relative_word_frequency(self, mode, count, path_to_chart="", get_better_table=False,):
        # Article table
        with open("word-counts.json", "r", encoding="utf-8") as f:
            article_counts = json.load(f)

        article_series = pd.Series(article_counts, dtype=float)
        if not article_series.empty:
            article_series /= article_series.max()

        if get_better_table == True:
            article_series = article_series[article_series > 0.05]

        # Language table
        language = self.scraper.get_language()

        language_freqs = {}
        language_words = top_n_list(language, max(10000, count))
        for word in language_words:
            language_freqs[word] = zipf_frequency(word, language)

        language_series = pd.Series(language_freqs, dtype=float)
        if not language_series.empty:
            language_series /= language_series.max()

        # Getting the words for table. (Half from language, half from article)
        half = count // 2

        sample_article = random.sample(
            list(article_series.index),
            min(half, len(article_series))
        )

        sample_language = random.sample(
            list(language_series.index),
            min(count - half, len(language_series))
        )

        words = list(set(sample_article + sample_language))

        # Creating final table
        df = pd.DataFrame({"word": words})
        df["frequency in article"] = df["word"].map(article_series)
        df["frequency in wiki language"] = df["word"].map(language_series)

        if mode == "article":
            df = df.sort_values(by="frequency in article", ascending=False)
        elif mode == "language":
            df = df.sort_values(by="frequency in wiki language", ascending=False)

        # Creating chart if necesarry
        if path_to_chart:
            df.set_index("word").plot(kind="bar", figsize=(10, 5))
            plt.title("Relative word frequency comparison")
            plt.ylabel("Normalized frequency")
            plt.tight_layout()
            plt.savefig(path_to_chart)
            plt.close()

        return df


