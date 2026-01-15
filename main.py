from cli import CLIArgumentParser
from scraper.tolkien_gateway_scraper import TolkienGatewayScraper
from parser.article_parser import ArticleParser
import sys
import pandas

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
        summary = parser.get_summary(args.summary)
        print(summary)
    elif args.table:
        table = parser.get_table(args.table, args.number)
        table_name = args.table + '.csv'
        table.to_csv(table_name, index=False)
        print(table)
    elif args.count_words:
        parser.get_words(args.count_words)
    elif args.analyze_relative_word_frequency:
        if args.chart:
            parser.get_relative_word_frequency(args.mode, args.count, path_to_chart=args.chart)
        else:
            parser.get_relative_word_frequency(args.mode, args.count)
    elif args.auto_count_words:
        parser.get_words_many_times(args.auto_count_words, args.depth, args.wait)





main()