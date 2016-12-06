#!/usr/bin/python
# -*- coding: utf-8 -*-

import spark
import tweepy
import os
import time

consumer_token = os.environ['TWITTER_C_TOKEN']
consumer_secret = os.environ['TWITTER_C_SECRET']
access_token = os.environ['TWITTER_A_TOKEN']
access_secret = os.environ['TWITTER_A_SECRET']


auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def tweet_random():
    api.update_status(spark.forecast())

for i in range(0):
    print spark.forecast().encode('utf-8')

while True:
    tweet_random()
    time.sleep(60*5)
