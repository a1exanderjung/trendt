import sys, logging, argparse
from chalk import log
from halo import Halo
from . import __program__, __description__
from .apis import __all__ as __apis__
from .apis import *

# Trend/t
#
# A "simple" program
class trendt:
    available_apis = []
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

        # Stop the spinner, initialising is done
        self.spinner.stop()

        # Parse arguments
        self.args = self.parser.parse_args(_args)

    # Search based on keywords
    def search(self, _keywords=None, _exclude=None, _only=None, _from=None, _to=None):
        # Assign key-values
        args = vars(self.args)

        # Lets fill in the gaps
        if _keywords is None:
            _keywords = args['keywords']
        if _exclude is None:
            _exclude = args['exclude']
        if _only is None:
            _only = args['only']
        if _from is None:
            _from = args['from']
        if _to is None:
            _to = args['to']

        # Parse date format
        if _from is not None or _to is not None:
            pass

        # This if-statement is mutually exclusive by argparse
        if _exclude is not None and len(_exclude) > 0:
            for api in _exclude:
                del self.available_apis[api]

        elif _only is not None and _only in self.available_apis:
            _api = self.available_apis[_only]
            self.available_apis = {
                _only: _api
            }

        # Lets do this search!
        for api in self.available_apis:
            self.available_apis[api].search(_keywords, _from, _to, 0)

    # Load apis
    def load_apis(self):
        _apis = {}

        # Iterate through all available apis and instantiate
        for api in self.available_apis:
            _module = globals()[api]
            _class = getattr(_module, api)
            _apis[api] = _class()
            _apis[api].init(self.args, self.parser, self.verbose)

        # Re assign
        self.available_apis = _apis

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
