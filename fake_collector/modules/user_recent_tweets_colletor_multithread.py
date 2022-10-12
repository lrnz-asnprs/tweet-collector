from concurrent.futures import thread
import sys
sys.path.append("~/Documents/tweet-collector")
import time
import datetime
from fake_collector.utils.TwythonConnector import TwythonConnector
from twython import TwythonRateLimitError
from fake_collector.utils.TwitterUser import TwitterUser
from typing import List
from multiprocessing import Process
from fake_collector.modules.user_profile_collector import UserProfileCollector
from fake_collector.modules.user_following_collector_v2 import UserFollowingCollectorV2
from fake_collector.modules.user_following_collector import UserFollowingCollector
import queue
import threading
import time


