"""
@Gyrst 
Created on 30-09-2022


Reasoning and considerations for data preprocessing steps
1) Stops words need to be removed as "and", "or" words become ambigious for the API. See error text here {"errors": [{"parameters": {"query": ["Hillary Clinton and millennials have the same positions on climate change abortion rights immigration reform gay rights and college affordability Donald Trump doesn't -politifact"]}, "message": "There were errors processing your request: Ambiguous use of and as a keyword. Use a space to logically join two clauses, or \"and\" to find occurrences of and in text (at position 121), Ambiguous use of and as a keyword. Use a space to logically join two clauses, or \"and\" to find occurrences of and in text (at position 17)"}], "title": "Invalid Request", "detail": "One or more parameters to your request was invalid.", "type": "https://api.twitter.com/2/problems/invalid-request"}
2) Twitter queries are not case sensitive - https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
3) Academic API Query Length is 1024 characters https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
4) Retweets texts are typically truncated after 140 characters https://developer.twitter.com/en/docs/twitter-api/premium/data-dictionary/overview#:~:text=In%20the%20case%20of%20Tweets,become%20truncated%20and%20thus%20incomplete.
5) We might want to avoid removing commas or punctuation when between digits

"""
import sys, os
import re, pandas as pd
from datetime import datetime
from fake_collector.modules.tweet_collector import collect_tweets
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from fake_collector.configs.directory_config import Directories

dir = Directories()

print(dir.DATA_PATH, "datapath")

class FakeNewsTweetCollector():
    
    
    def __init__(self, politifact_dataframe):
        self.sample = politifact_dataframe
             



    
    @staticmethod 
    def set_text_character_limit(character_limit, text):
        """ Set a character limit cutting the setence at the next full word.

        
        
        Args:
            character_limit (int): The character limit
            text (str): The text input that the limit should apply on

        Returns:
            str: the modified possibly shorter text.
        """
        tweet_tokenizer = TweetTokenizer()
        word_tokens = tweet_tokenizer.tokenize(text) 
        
        sentence = ""
        for word in word_tokens:
            if len((sentence + " " + word).strip())<character_limit:
                sentence +=  " " + word
        
        return sentence.strip()



    def set_character_limit(self, character_limit):
        """ Takes in a dataframe modifies the textual data to fit the specified character limit.

        Args:
            character_limit (int): Number of characters allowed.
            sample (dataframe): the dataframe being modified
        """
        self.sample['claim'] = self.sample.claim.apply(lambda x: self.set_text_character_limit(character_limit, x))
    
    
    @staticmethod
    def remove_excluded_words(text):
        """ Word tokenization of the text using the TweetTokenizer that allows to get ride of special characters
            in general, but not in cases of when placed in between numbers (e.g., 10,000, 75.5 percent etc.).
            Likewise it ignores the removal of apostrophes (e.g., don't, doesn't, they've, won't etc.)

        Args:
            text (str): Text being modified.

        Returns:
            str: The modified text result.
        """
        stop_words = set(stopwords.words('english'))
        
        tweet_tokenizer = TweetTokenizer()
        word_tokens = tweet_tokenizer.tokenize(text)
        #stopword removal
        word_tokens = [w for w in word_tokens if not w.lower() in stop_words]
        #special characters
        word_tokens = [w for w in word_tokens if not re.match(r"[^A-Za-z0-9]", w)]
        
        return " ".join(word_tokens)



    def clean_claims(self):
        """ Three step cleaning procedure. 
            1) strips the whitespaces and "\\n" newslines.
            2) It removes the "Says" in the beginning of sentences. 
            3) Removes stopwords and special characters.

        Args:
            sample (dataframe): The dataframe being modified.
        """
        
        
        # #Cleaning step 1 - getting rid of \n appearances and weird spaces
        self.sample['claim'] = self.sample.claim.apply(lambda x: x.strip())

        # Removing "Says" in the beginning of a statement around 1000 claim quotes in the sample have this sentence structure.
        # Fine to remove as the quote after is the essence of the claim.
        self.sample['claim'] = self.sample.claim.apply(lambda x: re.sub(r'^Says', '', x).strip())
        
        # remove stopwords - done in order to avoid query errors such as:
        # "There were errors processing your request: Ambiguous use of and as a keyword. Use a space to logically join two clauses, or \"and\" to find occurrences of and in text
        self.sample['claim'] = self.sample.claim.apply(lambda x: self.remove_excluded_words(x))
        

    def reshape_date_format(self):
        """ Takes in a dataframe and reshapes the the date into the datetime format needed for the TweetCollector
            (e.g., "2022-08-01T00:00:00Z")
            
        Args:
            sample (dataframe): the dataframe input.
        """
        self.sample['stated_on'] = self.sample.stated_on.apply(lambda x: str(datetime.strptime(x, '%B %d, %Y').isoformat()+"Z"))

    def get_data(self):
        return self.sample
    
    def show_data(self):
        print(self.sample)
    
    def drop_unused_indexes(self):
        
        columns_to_drop = ['Unnamed: 0.1', 'index', 'Unnamed: 0']
        
        for col in columns_to_drop: 
            try:
                self.sample = self.sample.drop(columns=col, axis=1)
            except:
                print("Could not drop column", col)
    
    
    def preprocess_data(self, character_limit=None):
        
        """ This function runs all the necessary cleaning steps to make the data ready for the TweetCollector to query 
            the fakenews that appeared on twitter.
        """
        try:
            #reshape dateformat
            self.reshape_date_format()
            
            #clean the fake news claim / title line
            self.clean_claims()
            
            #drop unnecessary columns of old indexes.
            self.drop_unused_indexes()
            
            #set character limit to the size of retweets (140 characters) before text is truncated for example if specified.
            if character_limit != None:
                self.set_character_limit(character_limit=character_limit)
        except:
            print("Something went wrong. Might be that the preprocessing already has been applied.")
            

    def get_fakenews_tweets(self, output_path=str(dir.DATA_PATH)+"/fakenews_tw_output/", disable_fetch=False):
        """ This function uses the input sample dataframe to make requests to the twitter API 
            applying the collect_tweet method from the module tweet_collecter with class TweetCollector.

        Args:
            sample (dataframe): dataframe with the fakenews content
            output_path (str, optional): Defaults to str(dir.DATA_PATH)+"/fakenews_tw_output/" if nothing else specified.
        """
        for index, row in self.sample.T.iteritems():
            query, start_time, end_time, topic, truth_value = row.claim, row.stated_on, str(datetime.today().isoformat()).split("T")[0]+"T00:00:00Z", row.topic, row.truth_value,
            
            print(start_time)
            print(end_time)
            print(query)
            
            file_name = "_".join([str(index), topic, truth_value, start_time.split("T")[0]]) + ".json"
            query += " -politifact"
            
            if not disable_fetch:
                collect_tweets(query, start_time, end_time, file_name, output_path)
                

