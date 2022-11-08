from drivers.configs.directories import Directories
import pickle, os, json
import pandas as pd
from datetime import datetime


class PolFollowScorer():
    """__summary__: Creates an object that can map out which politicians a given twitter user is following and calculate an average ideology score of these politicians.
    This can be used as a proxy for what political stance the twitter has, relying on the assumption that twitter user in general follow people that the aspire and agree with.
    
    To get the scoring of users one simply has to instantiate an PolFollowScorer object and run the method score_users(). Remember to save he results to a file with the write_to_json() method.
    """
    def __init__(self, fake=True):
        """Initiates the object and stores either the fake or true users depending on the boolean value specified.
        
        self.politicians contains key=twitter_id values=(name, ideology_score, leadership_score, description, party, gender, state, type)

        Args:
            fake (bool, optional): Determines whether it will pull fake or true users. Defaults to True.
        """
        self.dir = Directories()
        self.fake = fake
        self.today = str(datetime.today())[:10]
        
        #Depending on whether one wants the data for the fake or true user sample.
        if fake:
            self.directory = self.dir.FAKE_USERS_FOLLOWING_PATH
        else:
            self.directory = self.dir.TRUE_USERS_FOLLOWING_PATH
        
        
        self.politicians = self.__read_politicians(self.dir.DATA_PATH / "legislators", "legislators527_twitterid_ideology.csv")
        self.politicians_twitter_ids = self.__read_politicians_ids(self.dir.DATA_PATH / "legislators", "legislators-current-twIDs.csv")
        self.users_politicians_followed = {}
        self.users_ideology_score = {}
    
    def read_user_followings(self, path, filename):
        with open(path / filename, "rb") as f:
            users_following_ids = pickle.load(f)
        return users_following_ids
    
    def __read_politicians_ids(self, path, filename):
        pol_twitter_ids = set(pd.read_csv(path / filename).twitter_ids)
        return pol_twitter_ids
    
    def __read_politicians(self, path, filename):
        self.politicians = {}
        for row in pd.read_csv(path / filename).iterrows():
            row = row[-1]
            self.politicians[row['twitter_id']] = [row.full_name, row.ideology, row.leadership, row.description, row.party, row.gender, row.state, row.type]
        
        return self.politicians
        
    
    def __get_users_followings(self):
        directory = self.directory
        users_following_pickles = []

        for file in os.listdir(directory):
            with open(directory / file, "rb") as f:
                users_following_ids = pickle.load(f)
                users_following_pickles.append(users_following_ids)
        
        return users_following_pickles
    
    
    def find_politicians_followed(self):
        """The mothership method that finds what politicians each user is following.
        """
        users_following_pickles = self.__get_users_followings()
        
        for pickle in users_following_pickles:
            
            for key, user in pickle.items():
                self.users_politicians_followed[key] = []
                for following in user.following_ids:
                    if following in self.politicians_twitter_ids:
                        self.users_politicians_followed[key].append(following)
        
        return self.users_politicians_followed
                    
    @DeprecationWarning
    def describe_users(self):
        return pd.DataFrame(self.users_politicians_followed).describe()

    
    def score_users(self):
        """Proxy-scoring the ideology of the users based on the govtrack ideology-score (0 strong democratic - 1 strong republican) of the current politicians in congress and the house of representatives.
        """
        
        #gets the lst of politicians followed.
        self.find_politicians_followed()
        
    
        for key, politicians_followed in self.users_politicians_followed.items():
            
        
            number_of_pols_followed = len(politicians_followed)
            if number_of_pols_followed!=0:
                agg_score = 0
                
                for id in politicians_followed:
                    politician_ideology_score = self.politicians[id][1]
                    agg_score += politician_ideology_score
                    
                score = agg_score / len(politicians_followed)
                self.users_ideology_score[key] = [score, number_of_pols_followed, politicians_followed]
            else:
                self.users_ideology_score[key] = None
            
                
    def write_to_json(self):
        
        """Writes the results into a json file.
        """
        path = self.dir.DATA_PATH / "driver_scores"
        
        if self.fake:
            filename = "polfollow_fake_users_"+self.today+".json" 
        else:
            filename = "polfollow_true_users_"+self.today+".json"
        
        with open(path / filename, "w") as fp:
            json.dump(self.users_ideology_score, fp)