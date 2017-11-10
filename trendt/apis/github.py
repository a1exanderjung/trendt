import requests, re, urllib, time
from dateutil.parser import parse
from tqdm import tqdm
from datetime import datetime, timedelta
from .api import api, _date_format, output_dir, NoKeywordError, MissingOAuthToken

from halo import Halo
class github(api):
    name = 'GitHub'
    total_count = 0
    max_offset = 0
    url = 'https://api.github.com/search/commits'
    epoch_start = '2000-01-01'
    pagination_params = {
        'order': 'asc',
        'per_page': 100,
        'page': 1
    }

    # Add additional arguments for the GitHub API
    def register(self, _args = None, _parser = None):
        super(github, self).register(_args, _parser)

        # Bespoke API arguments
        self.parser.add_argument(
            '--github-oauth-token',
            help='Your OAuth token to be used against GitHub\'s API',
            type=str
        )

    # Initialise the GitHub API
    def init(self):
        super(github, self).init()

        # If this method has been called, we need the oauth token
        if self.args['github_oauth_token'] is None:
            raise MissingOAuthToken

    # Search GitHub
    def search(self, _keywords = None, _from = None, _to = None, _offset = 0):
        if _keywords is None:
            raise NoKeywordsException

        # Enable a search range
        if _from is None:
            _from = parse(self.epoch_start)
        elif _to is None:
            _to = datetime.now()

        _diff = (_to - _from).days

        print('Requesting results...')
        for i in tqdm(range(_diff)):
            _date = _from.strftime(_date_format)

            self.request(_keywords, _date)
            self.save()

            _from = _from + timedelta(days = 1)

    # Make a particular request to the API for a particular day
    def request(self, _keywords = None, _date = None, _offset = 0):
        pagination = self.pagination_params
        pagination['page'] = _offset + 1 # offset = 0 but page = 1
        query = _keywords

        # Request for a particular date
        if _date is not None:
            query = 'committer-date:' + _date + '..' + _date + '+' + query

        query = dict(pagination.items() + {'q' : query}.items())
        response = self.go(self.url, query)
        raw_data = response.json()

        self.collect(_date = _date, _total = int(raw_data['total_count']))

    # Make an actual request
    def go(self, _url = None, _params = {}):
        # Serialise the final search query
        request = _url + '?' + urllib.urlencode(_params)

        # GitHub conventions...
        request = request.replace('%3A', ':')
        request = request.replace('%2B', '+')

        if self.verbose:
            print('Requesting %s...' % request)

        # Make the request!
        response = requests.get(request, headers = {
            'Accept': 'application/vnd.github.cloak-preview',
            'Authorization': 'token ' + self.args['github_oauth_token']
        })
        raw_data = response.json()

        # We've probably hit a rate limit
        if 'items' not in raw_data.keys():
            if 'X-RateLimit-Reset' in response.headers:
                reset_at = datetime.fromtimestamp(float(response.headers['X-RateLimit-Reset']))

                # Wait until reset
                diff = (reset_at - datetime.now()).total_seconds()

                if diff > 0:
                    # + 5 for good measure
                    diff = int(diff + 5)
                    countdown_text = 'Waiting %d seconds due to rate limiting...'

                    ratelimit = Halo(
                        text = countdown_text % diff,
                        spinner = 'dots'
                    )
                    ratelimit.start()

                    for i in range(diff):
                        ratelimit.text = countdown_text % (diff - i)
                        try:
                            time.sleep(1)
                        except IOError:
                            pass

                    ratelimit.stop()

            # Try again?
            response = self.go(_url, _params)

        return response
