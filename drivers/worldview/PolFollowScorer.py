from drivers.configs.directories import Directories
import pickle, os
import pandas as pd
dir = Directories()


class PolFollowScorer():
    
    def __init__(self, fake=True):
        self.dir = Directories()
        
        #Depending on whether one wants the data for the fake or true user sample.
        if fake:
            self.directory = self.dir.FAKE_USERS_FOLLOWING_PATH
        else:
            self.directory = self.dir.TRUE_USERS_FOLLOWING_PATH
        
        
        self.politicians = self.__read_politicians(dir.DATA_PATH / "legislators", "legislators527_twitterid_ideology.csv")
        self.politicians_twitter_ids = self.__read_politicians_ids(dir.DATA_PATH / "legislators", "legislators-current-twIDs.csv")
        self.users_politicians_followed = {}
    
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
                    
    def describe_users(self):
        return pd.DataFrame(self.users_politicians_followed).describe()
