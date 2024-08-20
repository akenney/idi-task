import os
import re

# construct path to the directory containing the CSV file of tweets
# (this is a hacky way to do this)
DATA_DIRECTORY = re.sub('/src$', '/data', os.path.split(__file__)[0])
#TWEETS_FILENAME = 'correct_twitter_201904.tsv'
TWEETS_FILENAME = 'correct_twitter_202102.tsv'
