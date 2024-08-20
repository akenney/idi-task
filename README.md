# Overview

This is a submission for the Internet Democracy Initiative's [take-home assignment]([https://docs.google.com/document/d/1BGro-7cGty90IhFWNmV3EhxyBv3AWzJecIaoOoRcc5w/): a system for storing and querying a dataset of tweets about Britney Spears.  I did not have time to build a fully functioning system; the Docker and Flask aspects work, but the Lucene aspects have not been run because the installation and setup for Lucene/PyLucene turned out to be much more complicated than I anticipated, so I wrote code to approximate what I think would work if I could run it.  I did spend more than eight hours on this task if you include all of the trying to get Lucene working.


# Design decisions

## Document index

I did a bit of online searching about software for indexing text documents for term-searching, and decided to use [Lucene](https://lucene.apache.org/core/), which seems to be commonly used, and has a Python package ([PyLucene](https://lucene.apache.org/pylucene/features.html)).  I still think this is probably a good choice, but maybe not for an eight-hour project.  Installing it required (among other things) manually modifying the Makefile and figuring out that I needed to downgrade Python's `setuptools` package.

## API

I used Flask to make a very simple API.  It returns data as JSON, which is a common and user-friendly format.

The description of the querying is phrased as "If we search for a term, like “music,” we would like to know ...", which suggests that searching for a term is an atomic concept and the user always wants to know the same information about each search term.  For this reason, I chose to make a single API endpoint that returns all of this information.  However, this could easily be split into multiple separate endpoints if that were more appropriate for the actual use cases.

## Containerization

I used [Docker](https://docs.docker.com/guides/docker-overview/), primarily for the purpose of having a smooth process for installation and setup, but I didn't actually have time to get most of that into the Dockerfile, so Docker isn't adding much currently.


# Data

Either data file `correct_twitter_201904.tsv` or `correct_twitter_202102.tsv` can be used (the data source is selected in `constants.py`).  For the 2021 file, there were a few places where the text of a tweet contained an unescaped `U+000A` linefeed character, which caused the file not to parse correctly, so I just removed those characters in the file.


# Usage

## Prerequisites

Install [Docker](https://docs.docker.com/engine/install/).

## Running the system

In the directory containing the Dockerfile:

```
docker build -t app .
docker run -d -p 8000:8000 app
```

The app should then be running at http://0.0.0.0:8000/.

## Querying the data

Specify the search term in the URL - for example, to search for the term "music", use the URL http://0.0.0.0:8000/term/music/info.  (Currently it is using dummy data so the response will be the same regardless of what search term you use.)


# Limitations

Some things I would have done differently if given more time (in addition to getting the existing parts working):
- Other options than Lucene for indexing and storing the documents should be researched.  The usage of Lucene could also be improved, I didn't have time to learn much about its functionality.
- The API should cache responses.
- There should be error handling, and proper handling of cases that could cause the responses to be very large.
- The document index and the API should maybe be in separate Docker containers.
- There should be tests for the index-populating, index-querying, and API functionality.
- The API documentation could be prettier, maybe generated using Swagger or something.

