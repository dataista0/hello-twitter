#!/usr/bin/python
# -*- coding: utf-8 -*-#
import argparse
import logging
import json
import string
import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

FORMAT = '[%(asctime)s][%(levelname)-5s][%(name)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger("stream_listener")

try:
    from auth_data import CUSTOMER_KEY, CUSTOMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
except:
    logger.error('You should `mv auth_data.py.example auth_data.py && vim auth_data.py` with your access data.')
    logger.error('Read this: dev.twitter.com/oauth/overview')
    raise

def parse_args():
    """ parse command line arguments. """
    parser = argparse.ArgumentParser(description="twitter stream listener: connects to public stream and dumps tweets to a json file.")
    parser.add_argument("-q", "--query", help="search terms: use comma (,) for an OR and space ( ) for an AND. ")
    parser.add_argument("-o", "--output-file", help="optional. defaults to ${PWD}/dump-<<query>>.json.", default=None)
    return parser.parse_args()

class PublicStreamListener(StreamListener):
    """ connect to twitter stream api with a query and dump tweets to file.

    @note: the file format is: one json dictionary (tweet) per line (the full file is not a valid object)
    """

    def __init__(self, output_file, query):
        if output_file is None:
            output_file = 'dump-%s.json'
        valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
        self.output_file = ''.join(one_char if one_char in valid_chars else "_" for one_char in output_file)

        logger.info("Listener created for query '%s' dumping to file %s", query, self.output_file)

    def on_data(self, data):
        """ dump a tweet to the output file.
        @param data: a json dictionary (as a string)
        @return boolean: return False to close the connection (when a bad tweet is received we close it for precaution).
        """
        try:
            tweet = json.loads(data)
            logger.info("Dumping tweet: '%s' (@%s)", tweet['text'], tweet['user']['screen_name'])
        except:
            logger.error("Recieved the tweet: %s, closing the connection for precaution.", tweet)
            return False
        try:
            with open(self.output_file, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            logger.exception("Error on_data: %s", str(e))

        return True

    def on_error(self, status_code):
        #returning False disconnects the stream
        logger.error("on_error was called with status_code=%s", status_code)
        return False if status_code == 420 else True

if __name__ == '__main__':
    args = parse_args()

    auth = OAuthHandler(CUSTOMER_KEY, CUSTOMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, PublicStreamListener(args.output_file, args.query))
    twitter_stream.filter(track=[args.query])