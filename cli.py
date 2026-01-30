import argparse


class CLIArgumentParser:
    def __init__(self):
        self.parser = self.create_parser()

    def create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog='wiki_scraper',
            description='Scrape and analyze data from wikis.',
            epilog=(
                "Examples:\n"
                "  wiki_scraper --summary \"Bilbo Baggins\"\n"
                "  wiki_scraper --table \"Fellowship of the Ring\" --number 3\n"
                "  wiki_scraper --count-words \"Balrog\"\n"
                "  wiki_scraper --analyze-relative-word-frequency --count 10 --chart output.png\n"
                "  wiki_scraper --auto-count-words \"Gandalf\" --depth 2 --wait 2.0\n"
            ),
            formatter_class=argparse.RawTextHelpFormatter
        )

        main_group = parser.add_argument_group('Main commands (required, choose one)')
        action_group = main_group.add_mutually_exclusive_group(required=True)
        
        action_group.add_argument(
            "--summary",
            metavar='ARTICLE',
            help='Extract first paragraph from article\n'
        )

        action_group.add_argument(
            "--table",
            metavar='ARTICLE',
            help='Extract table from article (requires --number)\n'
        )

        action_group.add_argument(
            "--count-words",
            metavar='ARTICLE',
            help='Count words in article\n'
        )

        action_group.add_argument(
            "--analyze-relative-word-frequency",
            action="store_true",
            help='Analyze word frequencies\n' 
        )
        
        action_group.add_argument(
            "--auto-count-words",
            metavar='START_ARTICLE',
            help='Count words across linked articles (requires --depth)\n' 
        )

        table_group = parser.add_argument_group('Table options')
        table_group.add_argument(
            "--number", 
            type=int,
            metavar='N',
            help='Table number to extract (use with --table)\n'
        )
        table_group.add_argument(
            "--first-row-is-header",
            action="store_true",
            help='Use first row as table header (use with --table)\n'
        )

        analysis_group = parser.add_argument_group('Analysis options')
        analysis_group.add_argument(
            "--mode",
            choices=["article", "language"],
            help='Sort mode for frequency analysis\n'
        )
        analysis_group.add_argument(
            "--count",
            type=int,
            metavar='N',
            help='Number of words to display\n'
        )
        analysis_group.add_argument(
            "--chart",
            metavar='FILENAME',
            help='Save chart to file\n'
        )

        auto_group = parser.add_argument_group('Auto-count options')
        auto_group.add_argument(
            "--depth",
            type=int,
            metavar='N',
            help='Link traversal depth (use with --auto-count-words)\n'
        )
        auto_group.add_argument(
            "--wait",
            type=float,
            default=1.0,
            metavar='SECONDS',
            help='Delay between requests\n'
        )

        general_group = parser.add_argument_group('General options')
        general_group.add_argument(
            "--wiki",
            default="tolkien_gateway",
            help='Wiki to use. For default set on "tolkien_gateway"\n'
        )

        return parser

    def parse_arguments(self, args_list=None):
        args = self.parser.parse_args(args_list)
        self._validate_argument_dependencies(args)
        return args
    
    def _validate_argument_dependencies(self, args):
        if args.number is not None and args.table is None:
            self.parser.error("--number requires --table")
            
        if args.first_row_is_header and args.table is None:
            self.parser.error("--first-row-is-header requires --table")
        
        if args.depth is not None and args.auto_count_words is None:
            self.parser.error("--depth requires --auto-count-words")
        
        analyze_opts = [('--mode', args.mode),
                       ('--count', args.count),
                       ('--chart', args.chart)]
        
        for opt_name, opt_val in analyze_opts:
            if opt_val is not None and not args.analyze_relative_word_frequency:
                self.parser.error(f"{opt_name} requires --analyze-relative-word-frequency")

        if args.table and not args.number:
            self.parser.error(
                    "--table requires:\n"
                    "  --number"
                )
        
        if args.analyze_relative_word_frequency:
            if not (args.mode and args.count):
                self.parser.error(
                    "--analyze-relative-word-frequency requires:\n"
                    "  --mode, --count"
                )

        if args.auto_count_words:
            if not (args.depth and args.wait):
                self.parser.error(
                    "--auto-count-words requires:\n"
                    "  --depth, --wait"
                )
        
        return args