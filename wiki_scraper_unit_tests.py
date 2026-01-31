from bs4 import BeautifulSoup

from cli import CLIArgumentParser

from scraper.tolkien_gateway_scraper import TolkienGatewayScraper

# Testy cli.py
def test_summary(parser):
    args = parser.parse_arguments(["--summary", "Bilbo"])
    assert args.summary == "Bilbo"
    assert args.table is None
    assert args.count_words is None


def test_table_with_number(parser):
    args = parser.parse_arguments([
        "--table", "Fellowship of the Ring",
        "--number", "2"
    ])
    assert args.table == "Fellowship of the Ring"
    assert args.number == 2


def test_count_words(parser):
    args = parser.parse_arguments(["--count-words", "Balrog"])
    assert args.count_words == "Balrog"


def test_analyze_relative_word_frequency(parser):
    args = parser.parse_arguments([
        "--analyze-relative-word-frequency",
        "--mode", "article",
        "--count", "10"
    ])
    assert args.analyze_relative_word_frequency is True
    assert args.mode == "article"
    assert args.count == 10


def test_auto_count_words(parser):
    args = parser.parse_arguments([
        "--auto-count-words", "Gandalf",
        "--depth", "2"
    ])
    assert args.auto_count_words == "Gandalf"
    assert args.depth == 2


def test_cli():
    parser = CLIArgumentParser()
    test_summary(parser)
    test_table_with_number(parser)
    test_count_words(parser)
    test_analyze_relative_word_frequency(parser)
    test_auto_count_words(parser)

    print("Cli.py poprawne")

# Testy tolkien_gateway_scraper.py
def test_tables_exist(scraper, soup):
    tables = scraper.get_tables(soup)
    assert isinstance(tables, list)
    assert len(tables) > 0

def test_first_table_not_empty(scraper, soup):
    table = scraper.get_nth_table(soup, 0)
    assert table is not None
    assert not table.empty

def test_links_extraction(scraper, soup):
    links = scraper.get_all_links(soup)
    assert isinstance(links, set)
    assert len(links) > 0
    assert all(link.startswith("/wiki/") for link in links)

def test_language(scraper):
    assert scraper.get_language() == "en"

def test_scraper():
    with open("Bilbo.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    scraper = TolkienGatewayScraper()

    test_tables_exist(scraper, soup)
    test_first_table_not_empty(scraper, soup)
    test_links_extraction(scraper, soup)
    test_language(scraper)

    print("tolkien_gateway_scraper.py poprawne")


if __name__ == "__main__":
    test_cli()
    test_scraper()


