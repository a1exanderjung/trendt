# Trend/t

A simple tool to discover programming usage trends across major opensource platforms and Q&A sites over time.  It builds a raw output of accumulated usage over the defined period as both a time-usage graph and raw data samples for the related search keywords.

## Installation

To permenantly onto your system,

1. Install `git` and ensure it is available on your platform `PATH`,
2. Install `Python 2.7` and `pip`
3. Clone and cd into directory and use python setup to install:
  ```
  $ python setup.py install
  ```

## Running

Once installed, running `trendt` or `trendt --help` will yield:

```
usage: trendt [-h] [-f FROM] [-t TO] [-o OUTPUT] [--list-apis]
              [--exclude {github} | --only {github}] [-v]
              [--github-oauth-token GITHUB_OAUTH_TOKEN]
              [keywords]

Trend/t: A simple tool to discover programming usage trends on GitHub over time.

positional arguments:
  keywords              specific keywords to search, comma seperated for
                        multiple

optional arguments:
  -h, --help            show this help message and exit
  -f FROM, --from FROM  set the start date of the search in yyyy-mm-dd format
  -t TO, --to TO        set the end date of the search in yyyy-mm-dd format
  -o OUTPUT, --output OUTPUT
                        specify an output folder, default is ~/.trendt/
  --list-apis           list the available APIs
  --exclude {github}    exclude specific API from the search
  --only {github}       use only a specific API for the search
  -v, --verbose         be verbose
  --github-oauth-token GITHUB_OAUTH_TOKEN
                        Your OAuth token to be used against GitHub's API
```

### APIs

`trendt` makes use of various public APIs to perform its search and overall data aggregation.  However, in some instances, such as with GitHub, these APIs require authentication.  The following section describes additional parameters and measures.

#### GitHub

You will need a [personal access token](https://github.com/settings/tokens/new) from GitHub which can be aquired from your settings page.  The only scopes required for `trendt` are those from "repo".

Once you have the OAuth token, you can initialise `trendt` with it by using the `--github-oauth-token` flag.
