import sys
sys.path.append("~/Documents/tweet-collector/fake_collector")
import time
import datetime
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
    def __init__(self, app_type):
        self.app_type = app_type 
        self.bearer_token = json.load(open(dir.TOKENS_PATH))[f'{app_type}_bearer_token']
        self.endpoint_url = 'https://api.twitter.com/2/users/'      #https://api.twitter.com/2/users/:id/tweets full endpoint
        self.headers = {'Authorization': f'Bearer {self.bearer_token}'}

    def get_user_timeline(self, user: str):
        
        next_token = None
        query_params = {
                'max_results': 100,
                'pagination_token': next_token
               }

        while True:
            time.sleep(1.5)
            url = f"{self.endpoint_url}{user}/tweets"

            print(f"{self.app_type} app getting response")

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

            tweets = [{"id": tweet['id'], "text": tweet['text']} for tweet in response_json['data']]

            print(f"{self.app_type} app got {len(tweets)} tweets for user {user}")

            try:
                next_token = response_json['meta']['next_token']
                query_params['pagination_token'] = next_token
            except:
                next_token = None
                query_params['pagination_token'] = next_token
                break
        
        
        return None

    
if __name__ == "__main__":
    user_tweets = UserLatestTweetsCollectorV2(app_type='academic')
    tweets = user_tweets.get_user_timeline("20632528")
