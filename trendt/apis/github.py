import requests
import urllib
from .api import api, NoKeywordError, MissingOAuthToken

class github(api):
    args = None
    parser = None
    verbose = False
    search_apis = {
        'commits': {
            'url': 'https://api.github.com/search/commits',
            'params': {
                'q': '%s'
            }
        }
    }
    pagination_params = {
        'order': 'asc',
        'per_page': 100,
        'page': 1
    }

    # Initialise the GitHub API
    def init(self, _args=None, _parser=None, _verbose=False):
        # Thanks for the vars -- we'll keep those!
        self.args = _args
        self.parser = _parser
        self.verbose = _verbose

        # Bespoke API arguments
        self.parser.add_argument(
            '--github-oauth-token',
            help='Your OAuth token to be used against GitHub\'s API',
            type=str
        )

        self.parser.add_argument(
            '--save-commit-message',
            help='Include the commit message in the output',
            action='store_true'
        )

        # (bad) Re-parse args to get oauth token
        self.args = vars(self.parser.parse_args(_args))

    # Search GitHub
    def search(self, _keywords=None, _from=None, _to=None, _offset=0):
        if _keywords is None:
            raise NoKeywordsException

        # If this method has been called, we need the oauth token
        if self.args['github_oauth_token'] is None:
            raise MissingOAuthToken

        # Update offset
        _pagination = self.pagination_params
        _pagination['page'] = _offset

        # Update keywords
        _search = self.search_apis['commits']
        _query = _search['params']['q'] % _keywords

        # Enable ranges if specified
        if _from is not None and _to is not None:
            _query = 'committer-date:' + _from + '..' + _to + '+' + _query
        elif _from is not None:
            _query = 'committer-date:>=' + _from + '+' + _query
        elif _to is not None:
            _query = 'committer-date:<=' + _to + '+' + _query

        _search['params']['q'] = _query

        # Create final search query
        params = urllib.urlencode(dict(_pagination.items() + _search['params'].items()))

        # GitHub conventions.../
        params = params.replace('%3A', ':')
        params = params.replace('%2B', '+')

        r = requests.get(_search['url'] + '?' + params, headers={
            'Accept': 'application/vnd.github.cloak-preview',
            'Authorization': 'token ' + self.args['github_oauth_token']
        })

        raw_data = []

        print(r.json())
