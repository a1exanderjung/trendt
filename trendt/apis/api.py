import os
from halo import Halo

output_dir = '~/.trendt/'
date_format = 'yyyy-mm-dd'
_date_format = '%Y-%m-%d'

class api(object):
    name = 'generic'
    data = {}
    args = None
    parser = None
    verbose = False
    spinner = None
    last_date = None
    output_file = None

    # Provide parent parser
    def register(self, _args=None, _parser=None):
        # Thanks for the vars -- we'll keep those!
        self.args = _args
        self.parser = _parser

    # Initialise the API with program arguments
    def init(self):
        # Re-parse args for our new API arguments
        self.args = vars(self.parser.parse_args(self.args))

        # Are we being verbose?
        self.verbose = self.args['verbose']

        if self.args['output'] is not None:
            output_dir = self.args['output']

        if '~' in output_dir:
            output_dir = os.path.expanduser(output_dir)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.output_file = output_dir + self.name + '.csv'

        with open(self.output_file, 'w') as f:
            f.write('data,references\n')

    # Perform a search and parse results at offset
    def search(self, _keywords=None, _offset=0):
        raise NotImplementedError()

    # Collect a result
    def collect(self, _date = None, _total = 0, _message = None):
        # Do we have results already for this bin?
        if _date in self.data:
            self.data[_date] = self.data[_date] + _total

        # Shall we start?
        else:
            self.data[_date] = _total

    # Save current results
    def save(self):
        _recent = sorted(self.data.keys())[-1]
        with open(self.output_file, 'a') as f:
            f.write('%s,%d\n' % (_recent, self.data[_recent]))

class NoKeywordError(Exception):
    def __init__(self, message, foo, *args):
        self.message = 'No keyword(s) have been specified!'
        super(api.NoKeywordsException, self).__init__(message, foo, *args)

class MissingOAuthToken(Exception):
    def __init__(self, message, foo, *args):
        self.message = 'You have not provided an OAuth token for GitHub!'
        super(api.NoKeywordsException, self).__init__(message, foo, *args)
