class api:
    def init(self, _args=None, _parser=None):
        raise NotImplementedError()

    def search(self, keywords=None, offset=0):
        raise NotImplementedError()

    class NoKeywordException(Exception):
        def __init__(self, message, foo, *args):
            self.message = 'No keyword(s) have been specified!'
            super(api.NoKeywordsException, self).__init__(message, foo, *args)
