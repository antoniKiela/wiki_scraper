# wiki_scraper

`wiki_scraper` is a command-line tool for scraping and analyzing content from wiki pages.
The current implementation targets [Tolkien Gateway](https://tolkiengateway.net/wiki/) and supports:

- extracting an article summary (first paragraph),
- extracting a selected table and saving it to CSV,
- counting words in an article and storing cumulative counts,
- recursively counting words across linked wiki pages,
- comparing article word frequency against general English frequency.

## Project structure

- `wiki_scraper.py` - entry point; parses arguments, runs commands, handles errors.
- `cli.py` - CLI parser and argument validation.
- `scraper/base_scraper.py` - abstract scraper interface + HTTP session/rate limiting.
- `scraper/tolkien_gateway_scraper.py` - Tolkien Gateway implementation.
- `parser/article_parser.py` - command logic (summary/table/word analysis).

## Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`
- `pandas`
- `matplotlib`
- `wordfreq`
- `lxml` (recommended backend for `pandas.read_html`)

Install dependencies:

```bash
pip install requests beautifulsoup4 pandas matplotlib wordfreq lxml
```

## Usage

Run:

```bash
python wiki_scraper.py <COMMAND> [OPTIONS]
```

Only one main command can be used at a time.

### 1. Get summary

```bash
python wiki_scraper.py --summary "Bilbo Baggins"
```

Returns the first non-empty paragraph from the article content.

### 2. Extract table

```bash
python wiki_scraper.py --table "The Hobbit" --number 1
```

- Prints the selected table to stdout.
- Saves it as `<article>.csv` (for example `The Hobbit.csv`).

### 3. Count words in one article

```bash
python wiki_scraper.py --count-words "Balrog"
```

- Extracts all words from article content (`mw-content-text` section).
- Normalizes to lowercase and keeps alphabetic words.
- Updates `word-counts.json` in the current directory (cumulative counts).

### 4. Count words recursively through links

```bash
python wiki_scraper.py --auto-count-words "Gandalf" --depth 1 --wait 1.0
```

- Starts from one article.
- Follows internal `/wiki/...` links.
- Goes through links using DFS
- Counts words on each visited page and accumulates into `word-counts.json`.

### 5. Analyze relative word frequency

Requires an existing `word-counts.json` file.

```bash
python wiki_scraper.py --analyze-relative-word-frequency --mode article --count 10
```

Optional chart export:

```bash
python wiki_scraper.py --analyze-relative-word-frequency --mode language --count 20 --chart output.png
```

The command returns a table with:

- `word`
- `frequency in article`
- `frequency in wiki language`

where both frequency columns are normalized to `[0, 1]`.

## Output files

- `word-counts.json` - cumulative word counts from `--count-words` and `--auto-count-words`.
- `<article>.csv` - exported table from `--table`.
- `<chart-file>` (optional) - PNG chart from frequency analysis.

## Validation rules and constraints

- `--table` requires `--number`.
- `--number` is valid only with `--table`.
- `--depth` is valid only with `--auto-count-words`.
- `--analyze-relative-word-frequency` requires both `--mode` and `--count`.
- `--mode`, `--count`, `--chart` are valid only with `--analyze-relative-word-frequency`.
- Only one wiki is currently supported: `tolkien_gateway`.

## Error handling

- Network/HTTP problems are reported as `No page found`.
- Missing `word-counts.json` for analysis prints:
  `No word-counts.json file is in current directory`.
- Invalid table index raises an out-of-range error from scraper logic.

## Notes

- The scraper uses a dedicated HTTP session with custom `User-Agent` and built-in rate limiting (`0.5s`).
- Word counting is cumulative: running commands multiple times updates existing totals.
- Recursive word counting does not track visited pages, so the same page may be processed more than once when reached via different paths.
