from re import I
from fake_collector.configs.directory_config import Directories
from fake_collector.modules.fakenews_tweet_collector import FakeNewsTweetCollector
import pandas as pd

dir = Directories()

sample = pd.read_csv(str(dir.DATA_PATH)+"/fakenews_sources/all_politifact_1210nodup_fromnotopdup.csv")


#print(sample[(sample['Unnamed: 0']>19990) & (sample['Unnamed: 0']<20001)])

sample = sample[sample['Unnamed: 0']>37376]
sample = sample.set_index("Unnamed: 0")

fn = FakeNewsTweetCollector(sample)

#without character limit set to 140 (length of truncated sentences)
fn.preprocess_data()

print("sample size:", len(fn.get_data()))

#print(fn.sample)

fn.get_fakenews_tweets(index=(0,-1))

#fn.get_fakenews_tweets(index=(19999,46750))
