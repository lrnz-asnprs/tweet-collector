# Worldview

## news_sources 

### 60 news sources Dem/Rep Trust Scores
File: dem_rep_trustscores.json
script: NewsScorer60.py
Content: Measure for how much each 1000 american survey respondants trust in 60 common news medias
Source: from source of the Elites paper

### Dem/Rep News Sources Ideology Scores

File: dem_rep_news.json
Script: Newsscorer250.py
Content: 250 news sources labelled from on a scale from: strong democratic - lean democratic - centrist - lean republican - strong republican
Source: Aarhus paper on what drives spreading of Fake News.


### Dem/Rep Leaning Fake News
File: dem_rep_fakenews_sources.json
Content: ~40 dem/rep pro fakenews sources.
Source: Aarhus paper. 



## Politicians Followed

### current legislators' political position Dem/Rep gradient

file: legislators527_twitterid_ideology.csv
note: Fortunately, the govtrack_ids where included legislators-current-twIDS.csv. Therefore the ideology scores from senetors_ideology.csv and house_ideology.csv could be matched with the main doc with the twitter IDs of the full congress. 


script: PolFollowScorer.py

``` python

pfs = PolFollowScorer()

pfs.politicians
```
Output: key=twitter_id values=(name, ideology_score, leadership_score, description, party, gender, state, type):
'43910797': ['Sherrod Brown',0.1349708912284275,0.7782556635536014,'progressive Democratic leader', 'Democrat','M','OH','sen']

