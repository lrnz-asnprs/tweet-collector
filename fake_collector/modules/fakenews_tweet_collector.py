import sys, os
import re, pandas as pd
from datetime import datetime
from fake_collector import collect_tweets
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
sys.path.append("../tweet-collector")
from definitions import ROOT_DIR

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


politifact = pd.read_csv(ROOT_DIR+"/data/fakenews_sources/politifact_scape_2609.csv")

print(os.getcwd())

sample = politifact.sample(10, random_state=40).reset_index()

print(sample.head(1))



# Methods to clean 
def set_text_character_limit(character_limit, text):
    tweet_tokenizer = TweetTokenizer()
    word_tokens = tweet_tokenizer.tokenize(text) 
    
    sentence = ""
    for word in word_tokens:
        if len((sentence + " " + word).strip())<character_limit:
            sentence +=  " " + word
    
    return sentence.strip()



def set_character_limit(character_limit):
    sample['claim'] = sample.claim.apply(lambda x: set_text_character_limit(character_limit, x))
    
def remove_excluded_words(sample):
    stop_words = set(stopwords.words('english'))
    
    tweet_tokenizer = TweetTokenizer()
    word_tokens = tweet_tokenizer.tokenize(sample)
    #stopword removal
    word_tokens = [w for w in word_tokens if not w.lower() in stop_words]
    #special characters
    word_tokens = [w for w in word_tokens if not re.match(r"[^A-Za-z0-9]", w)]
    
    return " ".join(word_tokens)

def clean_claims(sample):
    # #Cleaning step 1 - getting rid of \n appearances and weird spaces
    sample['claim'] = sample.claim.apply(lambda x: x.strip())

    # Removing "Says" in the beginning of a statement around 1000 claim quotes in the sample have this sentence structure.
    # Fine to remove as the quote after is the essence of the claim.
    sample['claim'] = sample.claim.apply(lambda x: re.sub(r'^Says', '', x).strip())
    
    # remove stopwords - done in order to avoid query errors such as:
    # "There were errors processing your request: Ambiguous use of and as a keyword. Use a space to logically join two clauses, or \"and\" to find occurrences of and in text
    sample['claim'] = sample.claim.apply(lambda x: remove_excluded_words(x))
    

def reshape_date_format(sample):
    sample['date'] = sample.date.apply(lambda x: str(datetime.strptime(x, '%B %d, %Y').isoformat()+"Z"))
    
    
#Cleaning and preparation
clean_claims(sample)
reshape_date_format(sample)
set_character_limit(140)


print(sample.head(5))


path = ROOT_DIR+"/data/fakenews_tw_output/"

for index, row in sample.T.iteritems():
    query, start_time, end_time, topic, truth_value = row.claim, row.date, str(datetime.today().isoformat()).split("T")[0]+"T00:00:00Z", row.topic, row.truth_value,
    
    print(start_time)
    print(end_time)
    print(query)
    
    file_name = "_".join([str(index), topic, truth_value, start_time.split("T")[0]]) + ".json"
    query += " -politifact"
    collect_tweets(query, start_time, end_time, file_name, path)
