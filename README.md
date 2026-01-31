# Wiki Scraper Projekt

## Struktura Repozytorium

### Plik Główny
- **wiki_scraper.py** – Główny punkt wejścia aplikacji. Musi być uruchamiany z katalogu głównego projektu.

### Moduły

#### cli.py - Obsługuje parsowanie argumentów wiersza poleceń za pomocą `argparse`.

#### `scraper/` – Framework Scrapowania
- **base_scraper.py** – Definiuje abstrakcyjną klasę `BasicScraper`, która stanowi schemat dla wszystkich scrapujących klas dziedziczących.
- **tolkien_gateway_scraper.py** – Implementuje klasę `TolkienGatewayScraper`, dziedziczącą po `BasicScraper`, do obsługi strony Tolkien Gateway.

#### `parser/` – Parsowanie Artykułów
- **article_parser.py** – Implementuje klasę `ArticleParser`, która przyjmuje obiekt scrapera i uniwersalnie implementuje funkcje dla wszystkich scraperów.

### Testy
- **wiki_scraper_integration_test.py** – Test integracyjny programu. Używa lokalnego pliku `Bilbo.html`, aby przetestować funkcjonalność `--summary "Bilbo"` bez łączenia się z internetem. **Musi być uruchamiany z katalogu głównego.**
- **wiki_scraper_unit_tests.py** – Zbiór testów jednostkowych dla pojedynczych metod w programie. **Musi być uruchamiany z katalogu głównego.**
- **Bilbo.html** - Plik html zdobyty ze strony 'https://tolkiengateway.net/wiki/Bilbo_Baggins', wykorzystywany do testów lokalnych 

### Analiza Językowa (`LanguageAnalysis/`)
- **language_analysis.ipynb** – Notatnik Jupyter zawierający analizę językową.
- **Słowniki w formacie .json:**
  - `Bad-word-counts.json` – Został wygenerowany za pomocą funkcji `--count-words` w `wiki_scraper.py`.
  - `Big-word-counts.json` – Został wygenerowany za pomocą funkcji `--count-words` w `wiki_scraper.py`.
  - Pozostałe słowniki (`*.json`) – Zostały utworzone poprzez parsowanie gotowych tekstów z plików PDF dostępnych w internecie, przy użyciu funkcji podobnej do `--count-words`.

## Uwagi i Wymagania

### Środowisko i Uruchamianie
1.  **Ścieżki uruchamiania:**
    - `wiki_scraper.py`, `wiki_scraper_integration_test.py`, `wiki_scraper_unit_tests.py` **muszą** być uruchamiane z katalogu głównego projektu, aby importy modułów działały poprawnie.
    - `language_analysis.ipynb` **musi** być uruchamiany z poziomu katalogu `LanguageAnalysis/`.

### Konwencje Językowe i Licencje
1.  **Język w repozytorium:**
    - Wszystkie komunikaty commitów są w **języku angielskim**.
    - Wszystkie komentarze w kodzie źródłowym i nazwy plików są w **języku angielskim** w celu zachowania spójności.
    - Jedynie zawartość katalogu `LanguageAnalysis/` jest w **języku polskim**.

2.  **Licencja i Zgoda:**
    - Strona **Tolkien Gateway** udostępnia treść na licencji **CC BY-SA 4.0**, co pozwala na jej wykorzystanie w tym projekcie edukacyjnym.
    - Plik `robots.txt` strony Tolkien Gateway nie zabrania wykorzystywania naszych scraperów.
