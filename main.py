from fake_collector.modules.user_recent_tweets_collector_v2 import UserLatestTweetsCollectorV2


uwc = UserLatestTweetsCollectorV2(app_type='academic')

ids = ['2788918126', '2244994945']


uwc.get_user_timeline("2244994945")

print("something")