from random import random
from modules.tweet_collector import *
import os, re, pandas as pd

main_path = os.getcwd()

politifact = pd.read_csv(main_path+"/data/fakenews_sources/politifact_scape_2609.csv")

sample = politifact.sample(25, random_state=42).reset_index()

print(sample.head(5))



def clean_claims(sample):
    #Cleaning step 1 - getting rid of \n appearances and weird spaces
    sample['claim'] = sample.claim.apply(lambda x: x.strip())

    #Cleaning from all special characters - note the \w'\w is to avoid removing the ' in don't, won't they've etc.
    sample['claim'] = sample.claim.apply(lambda x: re.sub(r"[^a-zA-Z0-9 \w'\w]", '', x))

    #Removing "Says" in the beginning of a statement around 1000 claim quotes in the sample have this sentence structure. Fine to remove as the quote after is the essence of the claim.
    sample['claim'] = sample.claim.apply(lambda x: re.sub(r"^Says", '', x))


clean_claims(sample)

print()
print(sample.head(5))


