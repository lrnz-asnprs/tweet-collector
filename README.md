# The Fugazi Project

The fugazi project aims to translate psychological drivers of misinformation into quantifiable measures appplicable on observational data from Twitter.


The repository comprise two major components 1) Data collection, which primarily refers to the fake_collector directory, and 2) Analytics and operationalization implementations, which is in the drivers and falsity_prediction directory.


## Fake Collector

The fake_collector directory comprise two main modules that provides means to 1) fetch fact-checked fake news on twitter, and 2) add additional user specific data such as ID of who a user is following and recent tweets.

fakenews_tweet_collector.py comprise the FakeNewsTweetCollector class which can be applied to fetch fake news. One will have to add ones twitter api tokens to a tokens.json in order to utilize the script. Moreover, one will need give the Politifact (or other fact-checked news sources) as pandas dataframe as input.

```python

sample = pd.read_csv("the_politifact_fake_news_file.csv")

fn = FakeNewsTweetCollector(sample)

fn.get_fakenews_tweets()

```

## Drivers

### Illusory Truth
### Source Cues

### Emotions

### Worldview

We measure Worldview based on the news sources that our twitter users share. In particular, we use the ALlsides.com ratings for the political bias of news sources to access the political ideology of users. We then validate our approach by assessing with polticians that the users follow. Here we apply the Govtrack ratings of politicians the get a score an ideology score from 0-1 of all the members congress (i.e., 117th congress).

Below are examples provided for how one can run each class.

To run the NewsScorer250
```python

from drivers.worldview.NewsScorer250 import NewsScorer250

ns = NewsScorer250()

ns.full_run()

ns.write_to_json()

```



To run the PolFollowScorer
```python

from drivers.worldview.PolFollowScorer import PolFollowScorer

pfs = PolFollowScorer()

pfs.score_users()


pfs.write_to_json()

```


