# Notes

The following sections contains notes from the original fetches made. Through out the testing phase and the full runs made we kept the original indexing to be able to go back and filter out in the already fetched data, if necessary. This became necessary later during the full run. Several consideration and steps to ensure high quality data was put in place during the data fetching. The following Notes Section goes over many of these consideration made.


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
    - All query had an added "-politfact" in the end. This was tested in the initial test-phase and was found to be efficient to avoid the tweets that where referencing the politifact link. These people know it is fake news presumably.



#### Notes from the run:

- "Joe Biden Kamala Harris support abortion moment birth 2022-10-05T00:00:00Z" (The freeze stuck - no error message appearing)
- Error with 1595, 1596 - "Microsoft Bill Gates created 1999 video game called Omikron" Stuck with an error 400 (error in the query) but possibly because of overloading or bad wifi (in Madrid Airbnb when it was run)
- We still might have to do some filtering for in queries. The query below might not do  (query "video shows russian war ukraine" for example)
- 2,586,743 Tweets pulled of 10,000,000 in the end of the run.




### Take-off 12-10 

Running the next batch of claims (claims with the original indexing of 20,000 or higher)

#### general notes and reflections for improvement:

- Discussion Laurenz and Gustav on what topics and how to filter for duplicates.
- Takes in the politifact_0710notopicdup as input (the file with no topic duplicates used for the 05-10 take off run)
- First filtering for facebook posts, instagram posts, and viral video. Viral Video we decided to exclude as the titles for these are "video showing tank attacking Ukrainian solder" --> description of the video, and not the textual content from the original fake news. Thus we want to exclude this to make sure that our data has high integrity and quality.
- New filitering of the files to exclude duplicate claims. In the first run a "lavish" filtering was used. Only filtering for duplicates on the data that had duplicate topic tag. In this new approach for take-off 12-10, we ensure that quotes only are represented once in the data, making sure that we take the oldest date of the quotes, meaning that is a quote has three duplicates in the data two with the different dates, different origin, but refering to the same claim. We would keep the first instance of the claim. The one that happened on the first date. and then the first sender. often more people have spread the fake news. Politifact them both tags "Donald Trump" and "Facebook Posts". In this case we would keep the Donald Trump one as the other has been filtered out.


We also apply this filtering on the existing data that already had been fetched. by only keeping the files fetched that match the indexes obtained from our new filtered dataset. This is done using the script dub_filtering.py (available in the modules/utils folder)

#### Params:
    - same as for earlier run 05-10.



### 17-10 running for short sentences (5-8 words) the 5to8 run (8exclusive) added together with the nodub-1210_plus7

This run comprise 4 < fn.sample.words_in_claim <= 7 

#### params 

- running with the set of indexes that contain 5-8 (8 exclusive) words: This set comprise 4276 claims.
- same params as earlier runs. but now using the easy function where only stopwords "and" "or" are excluded as well as other special characters.
- Made check if results vary when one uses doesn't or doesn t -> which seems to have no effect whatsoever
- Made new filtering method with function easy=True for FakeNewsCollector preprocessing method. There seems to be a hickup with th U.S. becomes U.S. S - maybe related to the new formatting with only "and", "or" removal. Probably of minor influence though.


#### The 5to8 descrepancy
- The run went through succesfully --> however it was revealed that a gap of 76 claims/json-files existed between the the original nodub-1210 run and the new
- nodub-1210 has 19663 claims
- nodub-1210-plus7 + 5to8 files has 19587 claims
- A 76 gap
- The reason was found and revealed in the 5to8_descrepancy.ipynb notebook. showing that the original nodub-1210 somehow included some files on less than 5 words (fn.sample.words_in_claim<5). Seemingly from the initial fetch of 5000 quotes. Here where 93 quotes with less than 5 words that somehow got in.
- Thus the new file folder of nodub_take_off_1210_5to8 is the purest and doesn't contain such files.


