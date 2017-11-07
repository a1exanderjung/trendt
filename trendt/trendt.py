import sys, logging, argparse
from chalk import log
from halo import Halo
from os.path import join, dirname
from . import __program__, __description__
from .apis import __all__ as __apis__
from .apis import *

# Trend/t
#
# A "simple" program
class trendt:
    available_apis = []
    enabled_apis = []
    dateformat = 'dd/mm/yyyy'
    verbose = False
    parser = None
    spiner = None
    args = None
    log = None

    # Constructor loads API submodules
    def __init__(self, _args):
        # Initialise logging
        self.log = logging.getLogger(__name__)
        # self.log.addHandler(log.ChalkHander())

        # Pretty spinners!
        self.spinner = Halo(text='Initialising...', spinner='dots')
        self.spinner.start()

        # Actual useful program stuff
        self.args = _args

        self.available_apis = __apis__

        # Create the main argument parser
        self.parser = argparse.ArgumentParser(
            prog = __program__,
            description = __description__
        )

        # Common program arguments
        self.parser.add_argument(
            '-f', '--from',
            help='set the start date of the search in ' + self.dateformat + ' format',
            type=str,
            default=None
        )
        self.parser.add_argument(
            '-t', '--to',
            help='set the end date of the search in ' + self.dateformat + ' format',
            type=str,
            default=None
        )
        self.parser.add_argument(
            '--list-apis',
            help='list the available APIs',
            action='store_true'
        )

        # General program functionality (or positional arguments)
        self.parser.add_argument(
            'keywords',
            help='specific keywords to search, comma seperated for multiple',
            type=str,
            nargs='?'
        )

        # Allow --exclude and --only API options, but not together.
        apis = self.parser.add_mutually_exclusive_group()
        apis.add_argument(
            '--exclude',
            help = 'exclude specific API from the search',
            type = str,
            choices = self.available_apis
        )
        apis.add_argument(
            '--only',
            help = 'use only a specific API for the search',
            type = str,
            choices = self.available_apis
        )

        # Last but not least, verbose output
        self.parser.add_argument(
            '-v',
            '--verbose',
            help='be verbose',
            action='store_true'
        )

        # Load available APIs
        self.load_apis()

        # Parse arguments
        self.args = self.parser.parse_args(self.args)

        self.spinner.stop()

        # self.be_verbose(args.verbose)

    # Search based on state
    def search(self):
        self.search(
            self.args['keywords'],
            self.args['exclude'],
            self.args['only'],
            self.args['from'],
            self.args['to']
        )

    # Search based on keywords
    def search(self, _keywords, _exclude=[], _only=None, _from=None, _to=None):
        # Load .env
        dotenv_path = join(dirname(__file__), '.env')

        # Parse date format
        if _from is not None or _to is not None:
            pass

        # Load APIs based on preference
        self.load_apis(_exclude, _only)

        # Lets do this search!
        for api in self.search_apis:
            pass

    # Load apis
    def load_apis(self):
        __apis = {}

        # Iterate through all available apis and instantiate
        for api in self.available_apis:
            __module = globals()[api]
            __class = getattr(__module, api)
            __apis[api] = __class()
            __apis[api].init(self.args, self.parser)

        # Re assign
        self.available_apis = __apis

    # Dynamically load available apis based on user preference
    def use_apis(self, _exclude=[], _only=None):
        apis = self.apis

        if _exclude is not None and len(_exclude) > 0:
            pass

        elif _only is not None:
            pass

        for api in self.apis:
            print('.apis.' + api)
            # self.apis[api] = __import__('.apis.' + api)

    # List all the available APIs
    def list_apis(self):
        print(apis)

    # Set whether the program should be verbose or not
    def be_verbose(self, _verbose):
        self.verbose = _verbose

    # Print help proxy
    def print_help(self):
        self.parser.print_help()

# Make Main Great Again!
#
# @params   args
def main(args = sys.argv[1:]):
    t = trendt(args)

    if t.args.keywords:
        t.search()
    elif t.args.list_apis:
        t.list_apis()
    else:
        t.print_help()

if __name__ == '__main__':
    main()
