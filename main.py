from drivers.worldview.PolFollowScorer import PolFollowScorer
from drivers.worldview.NewsScorer250 import NewsScorer250


nos = NewsScorer250(fake=False)

nos.full_run()

nos.write_to_json()
