import json


def read_lst_of_json_objects(path):
    """_summary_: This method is made to read the list of json objects that the tweet_collecter.py (Lucas script) creates.

    Args:
        path (str): This is the path of the json file you want to read.

    Returns:
        lst: Returns a lst of json object. Do not try to load them all at once. It will kill the memory on your computer.
    """
    file = open(path,'r')
    tweets = []
    for line in open(path, 'r'):
        tweets.append(json.loads(line))
        
    return tweets