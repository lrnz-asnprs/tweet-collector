import json
import logging
import time
import requests
from twython import Twython
import sys

class TwythonConnector:
    def __init__(self):
        tokens = json.load(open("tokens.json"))
        self.app_key = tokens["app_key"]
        self.app_secret = tokens["app_secret"]
        self.access_token = None
        self.twitter_connection = None

    def make_connection(self):
        self.twitter_connection = Twython(self.app_key, self.app_secret, oauth_version=2)
        self.access_token = self.twitter_connection.obtain_access_token()
        self.twitter_connection = Twython(self.app_key, access_token=self.access_token)
        # add rate limiting, error handling, sleeping etc


if __name__ == "__main__":
    print("Starting connection")
    twitter_app = TwythonConnector()
    twitter_app.make_connection()
    print("Established connection")
    twitter_app.get_user_info(272065025)
    twitter_app.get_user_follower_ids(272065025)