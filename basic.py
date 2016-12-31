#!/usr/bin/python
# -*- coding: utf-8 -*-#

"""Minimal functional tests on twitter API libraries."""

import sys
from random import choice
from argparse import ArgumentParser

import twitter
import tweepy

try:
    from auth_data import CUSTOMER_KEY, CUSTOMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
except:
    print 'You should `mv data.py.example data.py && vim data.py` with your access data.'
    print 'Read this: dev.twitter.com/oauth/overview'
    raise

_TWITTER_API = None
_TWEEPY_API = None

def get_twitter_api():
    """Lazy initializer / getter for _TWITTER_API, a connection to twitter with python-twitter."""
    global _TWITTER_API
    if not _TWITTER_API:
        _TWITTER_API = twitter.Api(consumer_key=CUSTOMER_KEY,
                                   consumer_secret=CUSTOMER_SECRET,
                                   access_token_key=ACCESS_TOKEN_KEY,
                                   access_token_secret=ACCESS_TOKEN_SECRET)
    return _TWITTER_API

def get_tweepy_api():
    """Lazy initializer / getter for _TWEEPY_API, a connection to twitter with tweepy."""
    global _TWEEPY_API
    if not _TWEEPY_API:
        auth = tweepy.OAuthHandler(CUSTOMER_KEY, CUSTOMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        _TWEEPY_API = tweepy.API(auth)
    return _TWEEPY_API

def statuses(screen_name='julianpeller'):
    """Print and return 20 statuses of @screen_name."""
    statuses = get_twitter_api().GetUserTimeline(screen_name=screen_name)
    print 'api.GetUserTimeline(%s) returned %s statuses' % (screen_name, len(statuses))
    for status in statuses:
        print status.text
    return statuses

def post_update(update="apiPostUpdate()"):
    """Post @update as julianpeller."""
    get_twitter_api().PostUpdate(update)

def friends():
    """Print and return the user's friends."""
    friends = get_twitter_api().GetFriends()
    print 'api.GetFriends() returned %s friends' % len(friends)
    for friend in friends:
        print friend.name
    return friends

def random_tweets(n=10):
    """Print @n random tweets from the friends of the user."""
    print 'random_tweets(%d)' % n
    friends_list = friends()
    timelines = {}
    tweets = []
    while len(tweets) < n:
        friend = choice(friends_list)
        if not friend.name in timelines:
            timelines[friend.name] = statuses(friend.name)
        tweet = choice(timelines[friend.name])
        while tweet in tweets:
            tweet = choice(timelines[friend.name])
        tweets.append(tweet)
        print 'T %d - %s: %s' % (len(tweets), friend.name, tweet.text)
    return tweets

def test_get_timeline():
    """Print the last tweets in user's timeline."""
    api = get_tweepy_api()
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print tweet.text

def test_query(query='python'):
    """Print the last general tweets related with a @query."""
    max_tweets = 10
    print 'test_query_tweets(%s) will print the %d latest tweets with topic %s' % (query, max_tweets, query)
    searched_tweets = []
    last_id = -1
    api = get_tweepy_api()
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                print 'no new tweets'
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            print 'tweepy error'
            break
    for i, tweet in enumerate(searched_tweets):
        print i, tweet.text

def test_twitter_statuses():
    """Print last 20 statuses of user."""
    statuses()

def main():
    """Main."""
    functions = [str(module_element).replace("test_", "") for module_element in globals() if module_element.startswith("test_")]
    parser = ArgumentParser(description='Test basic twitter functionality.')
    parser.add_argument('test',type=str, choices=functions)

    args = parser.parse_args()
    globals()["test_" + args.test]()

if __name__ == '__main__':
    main()
