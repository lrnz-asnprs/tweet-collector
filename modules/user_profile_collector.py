from utils.TwythonConnector import TwythonConnector
import json
import logging

class UserProfileCollector:
    def __init__(self) -> None:
        pass

    def get_user_info(self, user_id, twitter_connection: TwythonConnector):
        user_info = self.twitter_connection.show_user(user_id=user_id)
        json.dump(user_info, open("{}/{}.json".format("data/users", user_id), "w"))

    def get_user_follower_ids(self, user_id, twitter_connection: TwythonConnector):
        user_followers = []
        try:
            user_followers = self.twitter_connection.get_followers_ids(user_id=user_id)
            user_followers = user_followers["ids"]
        except:
            logging.exception("Exception in follower_ids for user : {}".format(user_id))
        return user_followers

    # following
    def fetch_user_friends_ids(self, user_id, twitter_connection: TwythonConnector):
        user_friends = []

        try:
            user_friends = self.twitter_connection.get_friends_ids(user_id=user_id)
            user_friends = user_friends["ids"]
        except:
            logging.exception("Exception in follower_ids for user : {}".format(user_id))

        return user_friends