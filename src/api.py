'''
This file contains code for a Flask API for executing term searches.
'''

from collections import Counter

from flask import Flask, jsonify, make_response

#from doc_index import query_index
from constants import DATA_DIRECTORY


app = Flask(__name__)
# trailing slashes in URLs are optional
app.url_map.strict_slashes = False


def query_index(query, data_directory):
    # this is dummy data:
    return [
        {
            'text': "I like Britney Spears' music",
            'id': '12345',
            'date': '2021-01-03',
            'time': '12:34:56',
            'author_handle': 'musicfan',
            'like_count': 2,
            'place_id': 'None'
        }
    ]


@app.route('/term/<term>/info')
def get_term_info(term):
    '''
    Return information about the specified search term:
    {
      "tweets_per_day": {
        "YYYY-MM-DD": number of tweets with the term on that date
        for all dates that had any tweets with the term
      },
      "times": list of (str) HH:MM:SS timestamps (in local time) of all tweets
        with the term
      "average_likes": (float) average number of likes on tweets with the term,
      "place_ids": list of unique (str) place IDs of tweets with the term,
      "unique_users": (integer) number of users who posted tweets with the term,
      "top_users": list of (str) user handles who posted the most tweets with
        the term (will contain multiple users only if they all posted the same
        number of tweets with the term)
    }
    '''
    documents = query_index(term, DATA_DIRECTORY)
    info = {}
    info['tweets_per_day'] = dict(Counter(doc['date'] for doc in documents))
    likes = [doc['like_count'] for doc in documents]
    info['average_likes'] = sum(likes) / len(likes) if likes else 0
    info['place_ids'] = list(set(doc['place_id'] for doc in documents))
    info['times'] = [doc['time'] for doc in documents]
    users_to_n_tweets = Counter(doc['author_handle'] for doc in documents)
    info['unique_users'] = len(users_to_n_tweets)
    max_tweets = max(users_to_n_tweets.values(), default=0)
    info['top_users'] = [user for (user, n_tweets) in users_to_n_tweets.items()
                         if n_tweets == max_tweets]
    return jsonify(info)


@app.route('/')
def docs():
    docs_text = 'This is an API for querying a collection of tweets about Britney Spears.\n'
    for rule in app.url_map.iter_rules():
        if rule.endpoint in globals():
            docstring = globals()[rule.endpoint].__doc__
            if docstring:
                docs_text += '\n' + '-'*40 + '\n'
                docs_text += 'Path: ' + rule.rule + '\n'
                docs_text += 'Methods: ' + ', '.join(rule.methods)
                docs_text += docstring
    response = make_response(docs_text)
    response.mimetype = 'text/plain'
    return response
