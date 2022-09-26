# -*- coding: utf-8 -*-
"""
Created on Feb 20, 2019
@author: lajello

https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
"""
import requests
import json
import time
import bz2

#ACADEMIC keys
bearer_token_academic = json.load(open("tokens.json"))['bearer_token']

class CrawlError(Exception):
    all_error_codes = {-1: 'Unknown error', 0: 'User not existent', 1: 'Error during crawling'}

    def __init__(self, message, error_code):
        super().__init__(message)
        if error_code in self.all_error_codes:
            self.error_code = error_code
        else:
            self.error_code = -1


class TwitterCrawlerV2:
    def __init__(self, bearer_token=None):
        #self.file_header = '{"batches":['
        #self.file_footer = '\n]}'
        
        if bearer_token is None:
            self.bearer_token = 'x'
        else:
            self.bearer_token = bearer_token
        self.endpoint_url = 'https://api.twitter.com/2/tweets/search/all'
        self.headers = {'Authorization': f'Bearer {bearer_token}'}

    def get_tweets(self, query, fileout, max_results=10, start_time=None, end_time=None, 
                   tweet_fields=None, user_fields=None, expansions=None,
                   verbose=True, numlines_per_file=300, start_filecount=None):
        if not tweet_fields:
            #'context_annotations', 'entities', 'reply_settings' 'source', 'possibly_sensitive', 'attachments', 
            tweet_fields = ['author_id', 'created_at', 'geo', 'id', 
                            'in_reply_to_user_id', 'lang', 'public_metrics', 'referenced_tweets', 
                            'text', 'withheld', 'conversation_id']
            tweet_fields = ','.join(tweet_fields)
        if not user_fields:
            #'entities', 'pinned_tweet_id', 'protected', 'withheld'
            user_fields = ['created_at', 'description', 'id', 'location', 'name', 
                           'profile_image_url',  'public_metrics', 'url', 'username', 'verified']
            user_fields = ','.join(user_fields)
        if not expansions:
            expansions = ['in_reply_to_user_id', 'author_id']
            expansions = ','.join(expansions)
        next_token = None
        query_params = {'query': query,
                'tweet.fields': tweet_fields,
                'user.fields' : user_fields,
                'max_results': max_results,
                'start_time': start_time,
                'end_time': end_time,
                'expansions': expansions,
                'next_token':next_token
               }
        next_token = None
        oldest_timestamp = None
        
        
        total_tweet_count = 0
        numlines = 0
        if start_filecount:
            filecount = start_filecount
        else:
            filecount = 0
        fout = open(f'{filecount:05d}_{fileout}', 'wt', encoding='utf-8')
        while True:
            time.sleep(1.5)
            response = requests.request('GET', self.endpoint_url, headers=self.headers, params=query_params)
            if response.status_code == 429:
                print(f'{int(time.time())} - Hitting request limit, waiting.')
                time.sleep(30)
                continue
            if response.status_code != 200:
                print('Error', response.status_code, oldest_timestamp)
                #raise Exception(response.status_code, response.text)
                time.sleep(60)
            response_json = response.json()
            try:
                next_token = response_json['meta']['next_token']
            except:
                next_token = None
            try:
                oldest_timestamp = response_json['data'][-1]['created_at']
            except:
                oldest_timestamp = None
            query_params['next_token'] = next_token
            try:
                total_tweet_count += response_json['meta']['result_count']
            except:
                total_tweet_count += 0
            json.dump(response_json, fout)
            fout.write('\n')
            numlines+=1

            if numlines >= numlines_per_file:
                print(f'crawled {numlines} batches until {oldest_timestamp}')
                fout.close()
                filecount+=1
                numlines = 0
                fout = open(f'{filecount:05d}_{fileout}', 'wt', encoding='utf-8')
                
            if next_token is None:
                print('No more pages.')
                try:
                    fout.close()
                except:
                    pass
                break


def get_climate():
    bearer_token = bearer_token_academic
    crawler = TwitterCrawlerV2(bearer_token)
    print('Crawler successfully initialized')
    #query = 'global warming OR climate change OR climate emergency OR climate crisis OR #globalwarming OR #climatechange OR #climateemergency OR #climatecrisis'
    query = 'nuclear OR nuclear power OR nuclear energy -(nuclear weapons OR nuclear bombs OR nuclear warheads OR nuclear war OR nuclear submarines)'
    start_time = '2022-08-01T00:00:00Z'
    end_time = '2022-09-01T00:00:00Z'
    fileout = 'nuclear_tweets_aug22.json'
    crawler.get_tweets(query, fileout, max_results=500, start_time=start_time, 
                       end_time=end_time, numlines_per_file=1000, start_filecount=7)


print("Date: aug22")
