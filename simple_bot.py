#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Taken mostly from here: http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

Reads a file a tweets a line each SLEEP_MINS minutes.

"""
import time, sys, logging
import tweepy

# Minutes to sleep between tweets
SLEEP_MINS = 15

FORMAT = '[%(asctime)s][%(levelname)-5s][%(name)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger("simple_bot")

try:
    from auth_data import CUSTOMER_KEY, CUSTOMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
except:
    logger.error('You should `mv auth_data.py.example auth_data.py && vim auth_data.py` with your access data.')
    logger.error('Read this: dev.twitter.com/oauth/overview')
    raise

if __name__ == '__main__':
    try:
        argfile = str(sys.argv[1])
        filename=open(argfile,'r')
        f=filename.readlines()
        filename.close()
    except:
        logger.info("Usage: ./simple_bot.py <<input-file>>")
        logger.info("Usage: input-file must contain one tweet per line")
        exit(0)
    else:
        logger.info("File %s correctly read with %d tweets", len(f))

    auth = tweepy.OAuthHandler(CUSTOMER_KEY, CUSTOMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)


    for line in f:
        logger.info("Tweeting: %s", line)
        api.update_status(line)
        logger.info("Sleeping %s mins", SLEEP_MINS)
        time.sleep(SLEEP_MINS * 60) #Tweet every SLEEP_MINS mins

    logger.info("That's it. Bye.")
    exit(0)