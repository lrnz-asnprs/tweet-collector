import sys
sys.path.append("/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector")
import time
import datetime
from fake_collector.modules.user_profile_collector import UserProfileCollector
from fake_collector.utils.TwythonConnector import TwythonConnector
from twython import TwythonRateLimitError
from fake_collector.utils.TwitterUser import TwitterUser
from fake_collector.configs.directory_config import Directories
from typing import List
import json
import requests


#ACADEMIC API BEARER_TOKENS
dir = Directories()

class UserLatestTweetsCollectorV2:
    def __init__(self, app_type: str):
        """
        Param app_type: elevated or academic
        """
        self.app_type = app_type 
        self.bearer_token = json.load(open(dir.TOKENS_PATH))[f'{app_type}_bearer_token']
        self.endpoint_url = 'https://api.twitter.com/2/users/'
        self.headers = {'Authorization': f'Bearer {self.bearer_token}'}

    def get_user_timeline(self, user: TwitterUser):
        
        next_token = None
        #'context_annotations', 'entities', 'reply_settings' 'source', 'possibly_sensitive', 'attachments', 
        tweet_fields = ['author_id', 'created_at', 'geo', 'id', 
                        'lang', 'public_metrics', 'possibly_sensitive', 
                        'text']
        tweet_fields = ','.join(tweet_fields)

        query_params = {
                'max_results': 100,
                'tweet.fields': tweet_fields,
                'pagination_token': next_token,
               }

        print(f'{self.app_type} app - trying user {user.user_name}')

        while True:
            time.sleep(1)
            url = f"{self.endpoint_url}{user.user_id}/tweets"

            response = requests.request('GET', url, headers=self.headers, params=query_params)

            # rate_url = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
            # rate_limit_status = requests.request('GET', rate_url, headers=self.headers, params={'resources':'friends'})
            # rate_limit_json = rate_limit_status.json()

            if response.status_code == 429:
                print(f'{self.app_type} app {int(time.time())} - Hitting request limit, waiting.')
                time.sleep(900)
                print(f"{self.app_type} app resume connection")
                continue
            if response.status_code != 200:
                print('Error', response.status_code)
                #raise Exception(response.status_code, response.text)
                time.sleep(15)

            response_json = response.json()
            
            # Create tweet list
            tweets = [({key : tweet.get(key) for key in tweet}) for tweet in response_json['data']]
            
            # Add tweets to users tweet list
            user.add_recent_tweets(tweets)

            try:
                next_token = response_json['meta']['next_token']
                query_params['pagination_token'] = next_token
            except:
                next_token = None
                query_params['pagination_token'] = next_token
                break
        
        
        return None

    
if __name__ == "__main__":
   
    tweet_collector = UserLatestTweetsCollectorV2(app_type='academic')

    # Load the user profiles
    user_profile_collector = UserProfileCollector()
    user_profiles = user_profile_collector.load_user_profiles_as_list()

    for i in range(100):
        user = user_profiles[i]
        tweet_collector.get_user_timeline(user)
        print(f"Got {len(user.recent_tweets)} tweets for user {user.user_name}")

