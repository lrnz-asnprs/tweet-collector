import os, re, pandas as pd
from datetime import datetime
from modules.tweet_collector import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

main_path = os.getcwd()

politifact = pd.read_csv(main_path+"/data/fakenews_sources/politifact_scape_2609.csv")

sample = politifact.sample(10, random_state=40).reset_index()

print(sample.head(5))


def remove_stopwords(sample):
    stop_words = set(stopwords.words('english'))
  
    word_tokens = word_tokenize(sample)
    
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    
    filtered_sentence = []
    
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return " ".join(filtered_sentence)

def clean_claims(sample):
    #Cleaning step 1 - getting rid of \n appearances and weird spaces
    sample['claim'] = sample.claim.apply(lambda x: x.strip())

    #Cleaning from all special characters - note the \w'\w is to avoid removing the ' in don't, won't they've etc.
    sample['claim'] = sample.claim.apply(lambda x: re.sub(r'[^a-zA-Z0-9 \w\'\w]', '', x))

    # Removing "Says" in the beginning of a statement around 1000 claim quotes in the sample have this sentence structure.
    # Fine to remove as the quote after is the essence of the claim.
    sample['claim'] = sample.claim.apply(lambda x: re.sub(r'^Says', '', x).strip())
    
    # remove stopwords - done in order to avoid query errors such as:
    # "There were errors processing your request: Ambiguous use of and as a keyword. Use a space to logically join two clauses, or \"and\" to find occurrences of and in text
    sample['claim'] = sample.claim.apply(lambda x: remove_stopwords(x))


def reshape_date_format(sample):
    sample['date'] = sample.date.apply(lambda x: str(datetime.strptime(x, '%B %d, %Y').isoformat()+"Z"))
    
    
#Cleaning and preparation
clean_claims(sample)
reshape_date_format(sample)



print(sample.head(5))


# We have to remove stop words from the queries
# {"errors": [{"parameters": {"query": ["Hillary Clinton and millennials have the same positions on climate change abortion rights immigration reform gay rights and college affordability Donald Trump doesn't -politifact"]}, "message": "There were errors processing your request: Ambiguous use of and as a keyword. Use a space to logically join two clauses, or \"and\" to find occurrences of and in text (at position 121), Ambiguous use of and as a keyword. Use a space to logically join two clauses, or \"and\" to find occurrences of and in text (at position 17)"}], "title": "Invalid Request", "detail": "One or more parameters to your request was invalid.", "type": "https://api.twitter.com/2/problems/invalid-request"}

#twitter queries are not case sensitive - https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

for index, row in sample.T.iteritems():
    query, start_time, end_time, topic, truth_value = row.claim, row.date, str(datetime.today().isoformat()).split("T")[0]+"T00:00:00Z", row.topic, row.truth_value,
    
    print(start_time)
    print(end_time)
    print(query)
    
    file_name = "_".join([str(index), topic, truth_value, start_time.split("T")[0]]) + ".json"
    query += " -politifact"
    get_tweets(query, start_time, end_time, file_name)
    