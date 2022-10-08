import sys
sys.path.append("/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector")
import requests
import json
import time
import bz2
import os
from fake_collector.configs.directory_config import Directories
from fake_collector.utils.TwitterUser import TwitterUser
from typing import List
# from fake_collector.modules.user_profile_collector import UserProfileCollector


#ACADEMIC API BEARER_TOKENS
dir = Directories()

class CrawlError(Exception):
    all_error_codes = {-1: 'Unknown error', 0: 'User not existent', 1: 'Error during crawling'}

    def __init__(self, message, error_code):
        super().__init__(message)
        if error_code in self.all_error_codes:
            self.error_code = error_code
        else:
            self.error_code = -1


class UserFollowingCollectorV2:
    def __init__(self, app_type):   
        self.app_type = app_type 
        self.bearer_token = json.load(open(dir.TOKENS_PATH))[f'{app_type}_bearer_token']
        self.endpoint_url = 'https://api.twitter.com/2/users/'
        self.headers = {'Authorization': f'Bearer {self.bearer_token}'}

    def get_friends(self, user: TwitterUser):
    
        next_token = None
        query_params = {
                'max_results': 1000,
                'pagination_token': next_token
               }
        print(f"{self.app_type} app: trying user ", user.user_name)

        while True:
            time.sleep(1.5)
            url = f"{self.endpoint_url}{user.user_id}/following"
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
            friends = [user['id'] for user in response_json['data']]

            print(f"{self.app_type} app got friends {len(friends)} for user {user.user_name}")

            user.add_following_ids(friends)

            try:
                next_token = response_json['meta']['next_token']
                query_params['pagination_token'] = next_token
            except:
                next_token = None
                query_params['pagination_token'] = next_token
                break

        return
    

if __name__ == "__main__":

    twitter_friends = UserFollowingCollectorV2()
    users = ['272065025', '18676177', '1442906958', '477030336', '1138844680521736193', '3188245080', '15136500']

    twitter_friends.get_friends(users=users)