### Notes


#### test_run_27-09
+ was run with the random_state set to 40 


#### test_run_27-09
+ More and better results than in the case with the first test_run.


## TESTING
Trying the first larger data run and compares results

### 1) Checkng the flow at volume (hundreds of queries - folder 05-10_RUN)

#### parameters:
No character limit set at 140
lower bound of mininum 4 words search phrases
indexes 0,100
run with " U " replaced with " U.S. " as it appears in the original claim text. Maybe better to avoid this special character "."


indexes: 0,100 (only climate change topics)
start: 29,747 
end: 36,912
tweets: ~7,000 tweets
time: ~4.2 min


indexes: 1000, 1303 (abortion as topic for this subset of tweets)
start: 36,912
end: 99,613
tweets: ~63,000
time 22.4 min



### 2) SECOND CHECK- with and without character limit

Specifically:
test_sample_42 = sample.sample(100, random_state=42)

#### parameters:
character limit set at 140 and one run where characterlimit is not set
lower bound of mininum 4 words search phrases
random_state =  42
run with " U " replaced with " U.S. " as it appears in the original claim text. Maybe better to avoid this special character "."


#### More details:

WITH CHARACTER LIMIT
start: 99,613
end: 129,600
tweets: 29,987


WITHOUT CHARACTER LIMIT
start: 129,600
end: 159,496
tweets: 29.896

difference is only ~100 tweets.



## Full Run

### 3) take_off_0510 (The Iberian take off 05-01-22)

Running on all titles (with more than 5 words in the query) from file:
Part 1) data/fakenews_sources/politifact_scrape_7t_03102022.csv 
Part 2) data/fakenews_sources/all_politifact_0710nodub.csv


In the Part 1 file there has been done no filtering for duplicate texts. There seem to be quite a few overlapping within some topics (i.e., Environment and Climate Change).
In part 2, some filtering was executed to avoid overlaps/duplicates. A remove duplicates was applied allowing duplicate texts. bu deleting the ones with identical aspects for ['claim', 'stated_on', 'origin']. Thus further filtering of duplicates still needs to be done to avoid duplicate data. The reason for the more including approach is to have the full data and see if the difference in stated_on (start_date for the twitter_crawler input) might yield different and better results.

##### topics and indexes fetched
    - abortion, ukraine, Covid-19, elections, environment, climate-change, terrorism (first section with indexes 0-5000)
    - then remaining topics untill index 20,000
    - still missing indexes 20,000-43,000 to have the complete fetch of all

#### Parameters: 
    - No character limit
    - " U " replaces " U.S. " substitution made (the tweet token)
    - lower limit of 5 words for a query (To avoid "CO2 Pollutants" and very short fake news claims that would get results not related to the fake news.)
    - Runtimes (about 15h for part 1 --> but only because it stalled many times and had to be reset / reinitialized, 25 hours for part 2 (15,000 claims)).
    - All query had an added "-politfact" in the end. This was tested in the initial test-phase and was found to be efficient to avoid the tweets that where referencing the 
    - All 



#### Notes from the run:

- "Joe Biden Kamala Harris support abortion moment birth 2022-10-05T00:00:00Z" (The freeze stuck - no error message appearing)
- Error with 1595, 1596 - "Microsoft Bill Gates created 1999 video game called Omikron" Stuck with an error 400 (error in the query) but possibly because of overloading or bad wifi (in Madrid Airbnb when it was run)
- We still might have to do some filtering for in queries. The query below might not do  (query "video shows russian war ukraine" for example)
- 2,586,743 Tweets pulled of 10,000,000 in the end of the run.


