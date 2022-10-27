from drivers.configs.directories import Directories
import pickle, os, re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class NewsScorer():
    
    def __init__(self):
        """ 
        A newly created NewsOutletScorer object is equiped with the list of 60 common news outlets and the democratic/republican trust scores for each of such news outlet.
        """
        self.dir = Directories()
        
        #Common US News Outlets
        self.news = self.__read_news(self.dir.NEWS_OUTLETS_PATH, "news_outlets.txt")
        
        #Democrats/Republican Trust Scores
        self.trustscores = self.__read_trustscores(self.dir.NEWS_OUTLETS_PATH, "dem_rep_trustscores.csv")
        self.__format_trustscores()
        self.__min_max_scale_trustscores()
        
        #User Exposure to News
        self.users_news_exposure = {}
        
    @staticmethod
    def __read_news(path, filename):
        """reads the news sources file and returns it as a lst.

        Args:
            path (dir): directory location for news sources.
            filename (str): filename of the news_sources file.

        Returns:
            lst: list of 60 news sources
        """
        news = {}
        with open(path / filename, "r") as reader:
            lines = reader.readlines()
            for line in lines:
                news[line.strip()] = 0
        return news
    
    def __read_trustscores(self, path, filename):
        """Helper method to retrieve the news_scores.

        Args:
            path (str): path to directory
            filename (str): the filename

        Returns:
            Dataframe: 60 common news outlets and the respective trust-scores for Democrates and Republicans.
        """
            
        return pd.read_csv(path / filename)
    
    
    def __min_max_scale_trustscores(self):
        X = self.trustscores[['dem_trustscore', 'rep_trustscore']]
        scaler = MinMaxScaler()
        self.trustscores[['dem_trustscore', 'rep_trustscore']] = scaler.fit(X)
        self.trustscores[['dem_trustscore', 'rep_trustscore']] = scaler.transform(X)
    
    
    def __format_trustscores(self):
        self.trustscores['dem_rep_trustscores'] = self.trustscores.dem_rep_trustscores.apply(lambda x: [float(re.sub(r"[^\d.]", "", i)) for i in x.split(",")])
        self.trustscores['dem_trustscore'] = self.trustscores.dem_rep_trustscores.apply(lambda x: x[0])
        self.trustscores['rep_trustscore'] = self.trustscores.dem_rep_trustscores.apply(lambda x: x[1])
        try:
            columns_to_drop = ['dem_rep_trustscores', 'Unnamed: 0']
            self.trustscores = self.trustscores.drop(columns=columns_to_drop)
        except KeyError:
            print(f"KeyError occured when dropping columns: {columns_to_drop}".format())
    
    def __read_user_recent_tweets(self, path, filename):
        with open(path / filename, "rb") as f:
            users_loaded_batch = pickle.load(f)
        return users_loaded_batch
    
    def read_users_recent_tweets(self, directory):
        recent_tweets_batches = []
        files = [file for file in  os.listdir(directory)]
        for file in files:
            recent_tweet_batch = self.__read_user_recent_tweets(directory, file)
            recent_tweets_batches.append(recent_tweet_batch)
        return recent_tweets_batches
    
    
    def __find_news_per_user_batch(self, user_batch):
        """Helper method to find_news_per_user.

        Args:
            user_batch (lst): list of user objects
        """
        for key, user in user_batch.items():
            self.users_news_exposure[key] = []
            for tweet in user:
                if "entities" in tweet.keys():
                    if 'urls' in tweet['entities'].keys():
                        if "expanded_url" in tweet['entities']['urls'][0]:
                            for news in self.news.keys():
                                if news in tweet['entities']['urls'][0]['expanded_url']:
                                    self.users_news_exposure[key].append(news)    
    
    
    def find_news_per_user_batches(self, batches):
        for batch in batches:
            self.__find_news_per_user_batch(batch)
    
    
    def get_data_summary(self):
        df = pd.DataFrame(self.users_news_exposure.items())
        df[2] = df[1].apply(lambda x: len(x[:]))
        return df[2].describe(), print(f"{len(df[df[2]>0])}/{len(df)}".format())
        
    

    
    def calculate_user_political_score(self):
        self.user_trustscores = {}

        for user_id, vals in self.users_news_exposure.items():
            #To avoid division by zero error
            if len(vals)==0:
                self.user_trustscores[user_id] = [0,0]
                continue
            
            dem_trust, rep_trust = 0, 0
            for val in vals:
                dem_trust += float(self.trustscores[self.trustscores['news_outlet']==val]['dem_trustscore'])
                rep_trust += float(self.trustscores[self.trustscores['news_outlet']==val]['rep_trustscore'])
            
            dem_trust_avg = dem_trust/len(vals)
            rep_trust_avg = rep_trust/len(vals)
            
            self.user_trustscores[user_id] = [dem_trust_avg, rep_trust_avg]
        
    
    def get_trustscores(self):
        try: 
            type(self.user_trustscores)
        except:
            self.calculate_user_political_score()

        return self.user_trustscores
    
