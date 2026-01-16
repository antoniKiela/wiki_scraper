from scraper.tolkien_gateway_scraper import TolkienGatewayScraper
from parser.article_parser import ArticleParser

import sys

scraper = TolkienGatewayScraper()
parser = ArticleParser(scraper)

# Test
# --summary "Bilbo" 

try:
    summary = parser.get_summary('Bilbo', use_local_html_file_instead=True)
except FileNotFoundError as e:
    sys.exit(1)

expected_start = "Bilbo Baggins was a Hobbit who lived in The Shire"

expected_end = "and brought the One Ring of Sauron back into knowledge."

if not summary.strip().startswith(expected_start):
    sys.exit(1)

if not summary.strip().endswith(expected_end):
    sys.exit(1)