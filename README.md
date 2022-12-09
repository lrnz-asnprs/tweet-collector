# The Fugazi Project

The fugazi project aims to translate psychological drivers of misinformation into quantifiable measures appplicable on observational data from Twitter.


The repository comprise two major components 1) Data collection, which primarily refers to the fake_collector directory, and 2) Analytics and operationalization implementations, which is in the drivers and falsity_prediction directory.


## Fake Collector

The fake_collector directory comprise two main modules that provides means to 1) fetch fact-checked fake news on twitter, and 2) add additional user specific data such as ID of who a user is following and recent tweets.

fakenews_tweet_collector.py comprise the FakeNewsTweetCollector class which can be applied to fetch fake news. One will have to add ones twitter api tokens to a tokens.json in order to utilize the script. Moreover, one will need give the Politifact (or other fact-checked news sources) as pandas dataframe as input.

```python

sample = pd.read_csv("fake_news.csv")

fn = FakeNewsTweetCollector(sample)

fn.get_fakenews_tweets()

```


## Drivers

### Illusory Truth
### Source Cues

### Emotions

### Partisanship

