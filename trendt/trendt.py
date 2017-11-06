import sys
import argparse
from . import __program__, __description__

class trendt:
    apis = ['github']

    # List all the available APIs
    def list_apis(self):
        print('Hello!')

def main(args = sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog = __program__,
        description = __description__
    )

    # Common program arguments
    parser.add_argument(
        '-f', '--from',
        help='set the start date of the search in dd/mm/yyyy format',
        type=str,
        default=None
    )

    parser.add_argument(
        '-t', '--to',
        help='set the end date of the search in dd/mm/yyyy format',
        type=str,
        default=None
    )

    parser.add_argument(
        '--list-apis',
        help='list the available APIs',
        action='store_true'
    )

    # General program functionality
    parser.add_argument(
        'keywords',
        help='specific keywords to search, comma seperated for multiple',
        type=str,
        nargs='?'
    )


    # Allow --exclude and --only options, but not together.
    apis = parser.add_mutually_exclusive_group()
    apis.add_argument(
        '--exclude',
        help = 'exclude a specific API from the search',
        type = str
    )

    apis.add_argument(
        '--only',
        help = 'use only a specific API',
        type = str
    )

    parser.add_argument(
        '-v',
        '--verbose',
        help='be verbose',
        action='store_true'
    )

    args = parser.parse_args(args)

    if args.keywords:
        pass
    elif args.list_apis:
        pass
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
