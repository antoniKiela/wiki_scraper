from cli import CLIArgumentParser
from scraper.tolkien_gateway_scraper import TolkienGatewayScraper
from parser.article_parser import ArticleParser
import sys
import pandas
from pathlib import Path

def main():
    # Parse arguments
    argument_parser = CLIArgumentParser()
    args = argument_parser.parse_arguments()

    # Choose wiki
    wiki = 'tolkien_gateway'
    if args.wiki:
        wiki = args.wiki

    if wiki == 'tolkien_gateway':
        scraper = TolkienGatewayScraper()
    else:
        print("No wiki found", file=sys.stderr)

    # Initiate parser
    parser = ArticleParser(scraper)

    if args.summary:
        try:
            summary = parser.get_summary(args.summary)
            print(summary)
        except ConnectionError as e:
            print("No page found", file=sys.stderr)
    elif args.table:
        try:
            table = parser.get_table(args.table, args.number)
            table_name = args.table + '.csv'
            table.to_csv(table_name, index=False)
            print(table)
        except ConnectionError as e:
            print("No page found", file=sys.stderr)
    elif args.count_words:
        try:
            parser.get_words(args.count_words)
        except ConnectionError as e:
            print("No page found", file=sys.stderr)
    elif args.analyze_relative_word_frequency:
        if Path("word-counts.json").exists():
            if args.chart:
                parser.get_relative_word_frequency(args.mode, args.count, path_to_chart=args.chart)
            else:
                parser.get_relative_word_frequency(args.mode, args.count)
        else:
            print("No word-counts.json file is in current directory", file=sys.stderr)
    elif args.auto_count_words:
        try:
            parser.get_words_many_times(args.auto_count_words, args.depth, args.wait)
        except ConnectionError as e:
            print("No page found", file=sys.stderr)





main()