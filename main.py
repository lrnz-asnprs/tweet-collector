from drivers.worldview.PolFollowScorer import PolFollowScorer
from drivers.worldview.NewsScorer250 import NewsScorer250


nos = NewsScorer250()

nos.full_run(batches=False)

nos.write_to_json()
