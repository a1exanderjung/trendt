from halo import Halo

class api:
    name = 'Generic API'
    spinner = None

    # Initialise the API with program arguments
    def init(self, _args=None, _parser=None, _verbose=False):
        raise NotImplementedError()

    # Perform a search and parse results at offset
    def search(self, _keywords=None, _offset=0):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    # Provide a little indication that trendt is doing something
    def searching(self, _searching=True):
        self.spinner = Halo(text='Searching ' + self.name  + '...', spinner='dots')
        if _searching:
            self.spinner.start()
        else:
            self.spinner.stop()

class NoKeywordError(Exception):
    def __init__(self, message, foo, *args):
        self.message = 'No keyword(s) have been specified!'
        super(api.NoKeywordsException, self).__init__(message, foo, *args)

class MissingOAuthToken(Exception):
    def __init__(self, message, foo, *args):
        self.message = 'You have not provided an OAuth token for GitHub!'
        super(api.NoKeywordsException, self).__init__(message, foo, *args)
