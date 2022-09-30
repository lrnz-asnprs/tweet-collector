import json
import logging
import time
import requests
from twython import Twython
import sys

class TwythonConnector:
    def __init__(self):
        tokens = json.load(open("../../tokens.json"))
        self.app_key = tokens["app_key"]
        self.app_secret = tokens["app_secret"]
        self.access_token = tokens["access_token"] # might need to change it back
        self.access_token_secret = tokens["access_token_secret"]
        self.twitter_connection = None

    def make_connection(self):
        self.twitter_connection = Twython(self.app_key, self.app_secret, oauth_version=2)
        self.access_token = self.twitter_connection.obtain_access_token()
        self.twitter_connection = Twython(self.app_key, access_token=self.access_token)
        # add rate limiting, error handling, sleeping etc
    
    # Needs fixing, because of cumbersome authenticatioin process http://2017.compciv.org/guide/topics/python-nonstandard-libraries/twython-guide/twitter-twython-app-auth.html#use-twython-to-start-the-oauth1-authentication-process
    def make_connection_v1(self):
        self.twitter_connection = Twython(self.app_key, self.app_secret)
        auth = self.twitter_connection.get_authentication_tokens()
        OAUTH_TOKEN = auth['oauth_token']
        OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
        self.twitter_connection = Twython(self.app_key, self.app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        # Check if successful
        print(self.twitter_connection.verify_credentials())


if __name__ == "__main__":

    print("Starting connection V1")
    twitter_app = TwythonConnector()
    twitter_app.make_connection_v1()
    print("established connection")

    rate_limit_stats = twitter_app.twitter_connection.get_application_rate_limit_status()
    print(rate_limit_stats["resources"]["friends"]["/friends/ids"])

    print(twitter_app.twitter_connection)
    twitter_app.twitter_connection.get_friends_ids(user_id=272065025)

    rate_limit_stats = twitter_app.twitter_connection.get_application_rate_limit_status()
    print(rate_limit_stats["resources"]["friends"]["/friends/ids"])