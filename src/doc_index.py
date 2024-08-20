'''
This file contains code for creating and querying a Lucene index.  Many parts
of it are adapted from the example code in the test files that come with
PyLucene.
'''

import csv
import os

import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.document import \
    Document, Field, StoredField, StringField, TextField
from org.apache.lucene.index import \
    IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import NIOFSDirectory


def get_store(data_directory):
    '''
    Return a Lucene object representing the index stored on disk in the
    specified directory (there are many classes of storage, I just picked one,
    I don't know the differences among them).
    '''
    store = NIOFSDirectory(Paths.get(data_directory))


def get_analyzer():
    '''
    Return a Lucene object used for analyzing text.  I think this one will do
    stemming and stopword removal for English text.
    '''
    analyzer = StopAnalyzer(EnglishAnalyzer.ENGLISH_STOP_WORDS_SET)

    
def populate_index(data_directory, csv_filename, create=True):
    '''
    Populate a Lucene index using the tweets in the specified CSV file.  This
    indexes the text for searching, and stores the other fields that are needed
    for the API's term-search functionality.

    The fields stored (all as strings) are:
    text - text of the tweet
    id - unique ID of the tweet
    date - YYYY-MM-DD date on which the tweet was posted
    time - HH:MM:SS time at which the tweet was posted (local time)
    author_handle - username of user who posted the tweet
    like_count - number of likes the tweet received
    place_id - ID of where the tweet was posted from (or "None")

    Arguments:
    data_directory (str) - full path of the directory that contains the CSV
      file of tweets and where the index will be written
    csv_filename (str) - name of the CSV file of tweets within the directory
    create (bool) - whether creating a new index or adding to an existing one
    '''
    try:
        # TODO: this might need to pass a "classpath" argument to make it work
        lucene.initVM()
    except ValueError:
        # this happens when the JVM is already running in the process
        pass
    store = get_store(data_directory)
    analyzer = get_analyzer()

    config = IndexWriterConfig(analyzer)
    if create:
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    with open(os.path.join(data_directory, csv_filename)) as f:
        csv_reader = csv.DictReader(f, delimiter='\t')
        for line in csv_reader:
            doc = Document()
            # this is the only TextField (indexed for searching)
            doc.add(TextField('text', line['text']))
            # the rest of the fields are just stored for retrieval (this could
            # be changed if we also wanted to look up documents by these)
            doc.add(StoredField('id', line['id']))
            datestring, timestring = line['created_at'].split()
            # for now, ignore time zone (all of them are either EDT or EST)
            timestring = timestring.split('-')[0]
            doc.add(StoredField('date', datestring))
            doc.add(StoredField('time', timestring))
            doc.add(StoredField('author_handle', line['author_handle']))
            doc.add(StoredField('like_count', line['like_count']))
            # this counts "None" as its own place ID, could be changed if
            # that's not the desired behavior
            doc.add(StoredField('place_id', line['place_id']))
            writer.addDocument(doc)

    store.close()
    writer.close()


def query_index(query, data_directory):
    '''
    Search for the specified query using the Lucene index that exists in the
    specified data directory.
    (TODO) Return a list of documents, each represented as a dictionary,
    containing the fields listed in populate_index.
    '''
    store = get_store(data_directory)
    searcher = IndexSearcher(DirectoryReader.open(store))
    query = QueryParser('text', get_analyzer()).parse('value')
    # this requires specifying a maximum number of documents to return, so this
    # value is larger than the current total number of documents
    top_docs = searcher.search(query, 999999)
    self.closeStore(store)
    # TODO figure out how to extract the documents from top_docs and turn
    # them into dictionaries
    ...


# TODO this is not the best place to put this ...
if __name__ == '__main__':
    from constants import DATA_DIRECTORY, TWEETS_FILENAME
    populate_index(DATA_DIRECTORY, TWEETS_FILENAME)
