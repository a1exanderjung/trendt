# Trend/t

Trend/t: A simple tool to discover programming usage trends on GitHub over time.  It builds an output of references to a particular set of keywords over a defined period of time.  This can be used to plot a time-usage graph.

## Installation

To permenantly install `trendt` onto your system,

1. Install `git` and ensure it is available on your platform `PATH`,
2. Install `Python 2.7` and `pip`
3. Clone and `cd` into this repository and use `setup.py` to install:
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

`trendt` makes use of public APIs to perform its search and overall data aggregation.  However, in some instances, such as with GitHub, these APIs require authentication.  The following section describes additional parameters and measures.

#### GitHub

Data made available by GitHub comes through their public APIs, particularly focusing on searching repository commit history for the keywords specified into `trendt` .

To use `trendt` with GitHub, you will need a [personal access token](https://github.com/settings/tokens/new) from GitHub which can be aquired from your settings page.  The only scopes required for `trendt` are those from "repo".

Once you have the OAuth token, you can initialise `trendt` with it by using the `--github-oauth-token` flag.

## Motivation

The purpose of this program is to substantiate claims of programming paradigms, software libraries, tools or conventions by popularity over time.  
