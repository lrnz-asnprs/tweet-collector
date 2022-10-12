from re import I
from fake_collector.configs.directory_config import Directories
from fake_collector.modules.fakenews_tweet_collector import FakeNewsTweetCollector
import pandas as pd

dir = Directories()

sample = pd.read_csv(str(dir.DATA_PATH)+"/fakenews_sources/all_politifact_0710nodub.csv")


fn = FakeNewsTweetCollector(sample)

#without character limit set to 140 (length of truncated sentences)
fn.preprocess_data()

print("sample size:", len(fn.get_data()))

fn.get_fakenews_tweets(index=(19999,20000))
