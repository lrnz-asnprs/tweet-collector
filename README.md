# The Fugazi Project

The fugazi project aims to translate psychological drivers of misinformation into quantifiable measures derived from observational data from Twitter.


The repository comprise two major components 1) Data collection, which primarily refers to the fake_collector directory, and 2) Analytics and operationalization implementations, which is in the drivers and falsity_prediction directory.


## Data sets

The two main data sets for our research are available within the tweet-collector repository under the data directory:

+ politifact\_claims.csv contains the 20,174 fact-checked claims and details that follow with it. 
+ falsebelief\_users.csv contains the sample of 19,463 users who have shared the highest quantity of misinformation on Twitter. The respective calculated features for driver and false beliefs scores are included. 


## Fake Collector

The fake_collector directory comprise two main modules that provides means to 1) fetch fact-checked fake news on twitter, and 2) add additional user specific data such as ID of who a user is following and recent tweets.

fakenews_tweet_collector.py comprise the FakeNewsTweetCollector class which can be applied to fetch fake news. One will have to add ones twitter api tokens to a tokens.json in order to utilize the script. Moreover, one will need give the Politifact (or other fact-checked news sources) as pandas dataframe as input.

```python

sample = pd.read_csv("the_politifact_fake_news_file.csv")

fn = FakeNewsTweetCollector(sample)

fn.get_fakenews_tweets()

```


