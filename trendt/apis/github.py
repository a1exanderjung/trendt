import requests
from .api import api
# from dotenv import load_dotenv

class github(api):
    url = 'https://api.github.com/search/code?c=%s+in:both+fork:true&order=asc&page=%d&per_page=100'
    oauth_token = None

    # Initialise the GitHub API
    def init(self, _args=None, _parser=None):
        _parser.add_argument(
            '--github-oauth-token',
            help='An OAuth token to be used against GitHub\'s API',
            type=str
        )

    def search(self, _keywords=None, _from=None, _to=None, _offset=0):
        if _keywords is None:
            raise api.NoKeywordsException

        url = self.url
        headers = {'Authorization': 'token ' + self.oauth_token}

        r = request(url, headers=headers)

    class NoKeywordException(Exception):
        def __init__(self, message, foo, *args):
            self.message = 'You have not provided an OAuth token for GitHub!'
            super(api.NoKeywordsException, self).__init__(message, foo, *args)
