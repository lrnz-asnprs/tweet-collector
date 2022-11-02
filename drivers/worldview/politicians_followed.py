from drivers.configs.directories import Directories
import pickle, os
import pandas as pd
dir = Directories()


class PoliticiansFollowedScorer():
    
    def __init__(self):
        self.dir = Directories()
        self.politicians_twitter_ids = None
        self.users_politicians_followed = {}
    
    def read_user_followings(self, path, filename):
        with open(path / filename, "rb") as f:
            users_following_ids = pickle.load(f)
        return users_following_ids
    
    def read_politicians_ids(self, path, filename):
        pol_twitter_ids = set(pd.read_csv(path / filename).twitter_ids)
        return pol_twitter_ids
    
    def get_users_followings(self, directory):
      
        users_following_pickles = []

        for file in os.listdir(directory):
            with open(directory / file, "rb") as f:
                users_following_ids = pickle.load(f)
                users_following_pickles.append(users_following_ids)
        
        return users_following_pickles
    
    
    def find_politicians_followed(self, users_following_pickles):
        self.users_politicians_followed = {}

        for pickle in users_following_pickles:
            print(len(pickle))
            for key, user in pickle.items():
                c = 0
                for following in user.following_ids:
                    if following in self.politicians_twitter_ids:
                        c+=1
                
                self.users_politicians_followed[key] = c
                
    def describe_users(self):
        return pd.DataFrame(self.users_politicians_followed).describe()
