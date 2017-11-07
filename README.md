# Trend/t

A simple tool to discover programming usage trends across major opensource platforms and Q&A sites over time.  It builds a raw output of accumulated usage over the defined period as well as a time-usage graph and raw data samples for the related search keywords.

## Building & Running

To get started, ensure you have [Docker](https://docker.com) installed.  You can then use the [`Makefile`](/Makefile) to initialise docker into a basic terminal shell with `trendt` installed.  Run `make start` for access to:

```
usage: trendt [-h] [-f FROM] [-t TO] [--list-apis]
              [--exclude {github} | --only {github}] [-v]
              [--github-oauth-token GITHUB_OAUTH_TOKEN]
              [keywords]

Trend/t: A simple tool to discover programming usage trends across major
opensource platforms and Q&A sites over time.

positional arguments:
  keywords              specific keywords to search, comma seperated for
                        multiple

optional arguments:
  -h, --help            show this help message and exit
  -f FROM, --from FROM  set the start date of the search in dd/mm/yyyy format
  -t TO, --to TO        set the end date of the search in dd/mm/yyyy format
  --list-apis           list the available APIs
  --exclude {github}    exclude specific API from the search
  --only {github}       use only a specific API for the search
  -v, --verbose         be verbose
  --github-oauth-token GITHUB_OAUTH_TOKEN
                        An OAuth token to be used against GitHub's API
```

If you wish to install this permenantly, clone and cd into directory and use python setup to install, like so:

```
$ python setup.py install
```
