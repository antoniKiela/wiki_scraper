import sys
from pathlib import Path

import pandas

from cli import CLIArgumentParser
from parser.article_parser import ArticleParser
from scraper.tolkien_gateway_scraper import TolkienGatewayScraper


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
        return

    # Initiate parser
    parser = ArticleParser(scraper)

    if args.summary:
        try:
            summary = parser.get_summary(args.summary)
            print(summary)
        except ConnectionError:
            print("No page found", file=sys.stderr)
    
    elif args.table:
        try:
            table = parser.get_table(args.table, args.number)
            table_name = args.table + '.csv'
            table.to_csv(table_name, index=False)
            print(table)
        except ConnectionError:
            print("No page found", file=sys.stderr)
    
    elif args.count_words:
        try:
            parser.get_words(args.count_words)
        except ConnectionError:
            print("No page found", file=sys.stderr)
    
    elif args.analyze_relative_word_frequency:
        if Path("word-counts.json").exists():
            if args.chart:
                table = parser.get_relative_word_frequency(
                    args.mode, args.count, path_to_chart=args.chart
                )
            else:
                table = parser.get_relative_word_frequency(args.mode, args.count)
            print(table)
        else:
            print(
                "No word-counts.json file is in current directory",
                file=sys.stderr
            )
    
    elif args.auto_count_words:
        try:
            parser.get_words_many_times(
                args.auto_count_words, args.depth, args.wait
            )
        except ConnectionError:
            print("No page found", file=sys.stderr)

    scraper.close()

if __name__ == "__main__":
    main()