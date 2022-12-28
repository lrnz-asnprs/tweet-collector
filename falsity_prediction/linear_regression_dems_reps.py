import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector')

from models.regression_models import RandomForestRegressionModel, LinearRegressionModel
from models.classification_models import RandomForestClassificationModel
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from fake_collector.configs.directory_config import Directories
from fake_collector.utils.load_fake_true_users import load_all_fake_users_df
from falsity_prediction.model_config.features_config import DRIVER_CONTINUOUS_USER_FEATURES, GENERAL_CONTINUOUS_USER_FEATURES, DRIVER_BINARY_USER_FEATURES, FEATURES_TO_DRIVER_NAME
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from preprocessing.user_preprocessor import UserPreprocessor
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, classification_report, accuracy_score, recall_score, precision_score, f1_score
import math
from model_helpers import load_user_driver_data, save_feature_importance_plot_forest, split_in_quantile_chunks, split_in_ranges
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col

"""
Model type: simple or grid_search
Continuous features: DRIVER_CONTINUOUS_USER_FEATURES
target: aggregate_falsity_score or average_falsity_score
save: true or false
"""

dir = Directories()

# Load user features
user_df = load_user_driver_data()


# Split in 3 different groups
user_df = split_in_quantile_chunks(user_df, 'average_falsity_score', 2)

user_df = user_df[user_df['news_count'] >= 5]

DRIVER_CONTINUOUS_USER_FEATURES = [driver for driver in DRIVER_CONTINUOUS_USER_FEATURES if driver != 'ideology_score']



# Preprocess user features
user_preprocessor = UserPreprocessor(continuous_columns = DRIVER_CONTINUOUS_USER_FEATURES)
user_df_prepocessed = user_preprocessor.fit_transform(user_df)

# Get republicans and democorats
republicans = user_df_prepocessed[user_df_prepocessed['ideology_score'] > 0.5]
democrats = user_df_prepocessed[user_df_prepocessed['ideology_score'] <= 0.5]

# split into x and y
X_rep, y_rep = republicans[DRIVER_CONTINUOUS_USER_FEATURES], republicans[['average_falsity_score']]
X_dem, y_dem = democrats[DRIVER_CONTINUOUS_USER_FEATURES], democrats[['average_falsity_score']]
X_all, y_all = user_df_prepocessed[DRIVER_CONTINUOUS_USER_FEATURES], user_df_prepocessed[['average_falsity_score']]

# Prepare model, add constant
X_rep = sm.add_constant(X_rep)
X_dem = sm.add_constant(X_dem)
X_all = sm.add_constant(X_all)

# results
rep_result = sm.OLS(y_rep, X_rep).fit()
dem_result = sm.OLS(y_dem, X_dem).fit()
all_result = sm.OLS(y_all, X_all).fit()

print("Republicans")
print(rep_result.summary())

print("Democrats")
print(dem_result.summary())

print("All")
print(all_result.summary())

summary = summary_col([rep_result, dem_result],stars=True,float_format='%0.4f',
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'R2':lambda x: "{:.4f}".format(x.rsquared)})
