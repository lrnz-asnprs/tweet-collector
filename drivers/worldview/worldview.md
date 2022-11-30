# Worldview

## news_sources 

### 60 news sources Dem/Rep Trust Scores
File: dem_rep_trustscores.json
script: NewsScorer60.py
Content: Measure for how much each 1000 american survey respondants trust in 60 common news medias
Source: from source of the Elites paper

### Dem/Rep News Sources Ideology Scores

www.allsides.com/media-bias/ (Maybe note why there is a difference in the length --> Osmund et al. say 260 news, however there are only 250 available on the website.) 

While AllSides combines different methods for estimating ideological bias (e.g., editorial reviews, third-party judgments), SM Section 7 shows that their ratings correlate highly – Pearson’s r = .90 – with network-based measures of ideological alignment of media sites (Bakshy, Messing and Adamic 2015). See SM Section 7 and Figure SM 2b for the 20 most shared real news domains.


File: dem_rep_news.json
Script: Newsscorer250.py
Content: 250 news sources labelled from on a scale from: strong democratic - lean democratic - centrist - lean republican - strong republican
Source: Aarhus paper on what drives spreading of Fake News.
### Dem/Rep Leaning Fake News

Currently we dont use this one
File: dem_rep_fakenews_sources.json
Content: ~40 dem/rep pro fakenews sources.
Source: Aarhus paper. 


### Run with NewsScorer250 on all our users and their recent tweets 08-11-2022

True Users
NaN vals 2482
Actual values for data points 2718
Total dataset 5200
True users coverage 0.5226923076923077
mean true users ideology score 0.2885464332384139

Fake users
NaN vals 958
Actual values for data points 18505
Total dataset ~19500
Fake users coverage 0.9507784000411036
mean fake users ideology score 0.5241563714283359



## Politicians Followed

### current legislators' political position Dem/Rep gradient

file: legislators527_twitterid_ideology.csv
note: Fortunately, the govtrack_ids where included legislators-current-twIDS.csv. Therefore the ideology scores from senetors_ideology.csv and house_ideology.csv could be matched with the main doc with the twitter IDs of the full congress. 


script: PolFollowScorer.py

```python
#Assuming one runs it from the main.py (the parent layer of directory)
from drivers.worldview.PolFollowScorer import PolFollowScorer

pfs = PolFollowScorer()

pfs.politicians
```

Output: key=twitter_id values=(name, ideology_score, leadership_score, description, party, gender, state, type):
'43910797': ['Sherrod Brown',0.1349708912284275,0.7782556635536014,'progressive Democratic leader', 'Democrat','M','OH','sen']


To run:
```python

from drivers.worldview.PolFollowScorer import PolFollowScorer

pfs = PolFollowScorer()

pfs.score_users()


if save_results:
    pfs.write_to_json()

```

### Results from the 08-11-2022 run on politicians followed:

Fake users:

- Users that follow at least one politicians in congress 17851
- total amount of users 19463
- coverage 0.917176180444946
- mean score 0.45578289247487164 for all users with a least one politician followed

Lower than expected surely. 81 users get the score 0.0 (This is resulting from following only Bernie Sanders), 54 get the score 1.0 (as a result of only following Ted Cruz)


True Users:

- Users that follow at least one politicians in congress 1648
- total amount of users 5000
- coverage 0.3296
- 486 follow bernie only, and only 2 follow Ted Cruz
- mean score 0.13216067268600176


## Correlation between politicians followed govtrack ideology score and the newscorer ideology scores (The RUN 08-11-2022)

pearson 0.9004959101165257, p-value =  0.0
