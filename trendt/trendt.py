import sys, logging, argparse
from dateutil.parser import parse
from chalk import log
from halo import Halo
from . import __program__, __description__
from .apis import __all__ as __apis__
from .apis.api import output_dir, date_format, NoKeywordError, MissingOAuthToken
from .apis import *

# Trend/t
#
# A "simple" program
class trendt:
    available_apis = []
    verbose = False
    parser = None
    spiner = None
    args = None
    log = None

    # Constructor loads API submodules
    def __init__(self, _args):
        # Initialise logging
        self.log = logging.getLogger(__name__)
        self.log.addHandler(log.ChalkHandler())

        # Pretty spinners!
        self.spinner = Halo(
            text = 'Initialising...',
            spinner = 'dots'
        )
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
            help = 'set the start date of the search in %s format' % date_format,
            type = str,
            default = None
        )
        self.parser.add_argument(
            '-t', '--to',
            help = 'set the end date of the search in %s format' % date_format,
            type = str,
            default = None
        )
        self.parser.add_argument(
            '-o',
            '--output',
            help = 'specify an output folder, default is %s' % output_dir,
            default = output_dir,
            type = str
        )

        # Program functions
        self.parser.add_argument(
            '--list-apis',
            help = 'list the available APIs',
            action = 'store_true'
        )

        # General program functionality (or positional arguments)
        self.parser.add_argument(
            'keywords',
            help = 'specific keywords to search, comma seperated for multiple',
            type = str,
            nargs = '?'
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
            help = 'be verbose',
            action = 'store_true'
        )

        # Register available APIs
        # We do this first as each api contains sub commands and flags
        self.register_apis()

        # Stop the spinner, initialising is done
        self.spinner.stop()

        # Parse arguments
        self.args = vars(self.parser.parse_args(_args))
        self.verbose = self.args['verbose']
        _exclude = self.args['exclude']
        _only = self.args['only']
        _from = self.args['from']
        _to = self.args['to']

        # This if-statement is mutually exclusive by argparse
        if _exclude is not None and len(_exclude) > 0:
            for api in _exclude:
                del self.available_apis[api]

        elif _only is not None and _only in self.available_apis:
            _api = self.available_apis[_only]
            self.available_apis = {
                _only: _api
            }

        # Parse date format
        if _from is not None:
            self.args['_from'] = parse(_from)
        else:
            self.args['_from'] = None

        if _to is not None:
            self.args['_to'] = parse(_to)
        else:
            self.args['_to'] = None

        # Initialise available apis
        self.init_apis()

    # Search based on keywords
    def search(self):
        for api in self.available_apis:
            try:
                self.available_apis[api].search(
                    _keywords = self.args['keywords'],
                    _from = self.args['_from'],
                    _to = self.args['_to']
                )
            except (MissingOAuthToken, NoKeywordError, NotImplementedError) as err:
                self.log.error(err.message)

    # Register an API
    def register_apis(self):
        _apis = {}

        # Iterate through all available apis and add parser
        for api in self.available_apis:
            _module = globals()[api]
            _class = getattr(_module, api)
            _apis[api] = _class()
            _apis[api].register(
                _args = self.args,
                _parser = self.parser
            )

        # Re assign
        self.available_apis = _apis

    # Initialise apis
    def init_apis(self):
        # Re-iterate through all available apis and instantiate
        for api in self.available_apis:
             self.available_apis[api].init()

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

    if t.args['keywords']:
        t.search()
    elif t.args['list_apis']:
        t.list_apis()
    else:
        t.print_help()

if __name__ == '__main__':
    main()
