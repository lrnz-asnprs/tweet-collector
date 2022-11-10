import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector')

from models.regression_models import RandomForestModel, LinearRegressionModel
import pickle
from sklearn.preprocessing import MinMaxScaler
from fake_collector.configs.directory_config import Directories
from fake_collector.utils.load_fake_true_users import load_all_fake_users_df
from falsity_prediction.model_config.features_config import DRIVER_CONTINUOUS_USER_FEATURES, GENERAL_CONTINUOUS_USER_FEATURES
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from preprocessing.user_preprocessor import UserPreprocessor

"""
Script for model training and evaluation
"""

dir = Directories()

# Load user features
user_features_dir = dir.USERS_PATH / 'fake_users'
with open(user_features_dir / 'fake_users_driver_features.pickle', 'rb') as f:
    user_features = pickle.load(f)

user_features = user_features.reset_index().rename(columns={'index':'user_id'})
user_features['user_id'] = user_features['user_id'].astype(str)

# Load initial user df
fake_users = load_all_fake_users_df()
fake_users['user_id'] = fake_users['user_id'].astype(str)

# Merge features into initial user df
user_df = fake_users.merge(user_features, on='user_id')

# Test on different groups
user_df = user_df[user_df['fake_group'] !='very_high']

# Preprocess user features
user_preprocessor = UserPreprocessor(continuous_columns=DRIVER_CONTINUOUS_USER_FEATURES + GENERAL_CONTINUOUS_USER_FEATURES)

user_df_prepocessed = user_preprocessor.fit_transform(user_df)

# Select X and y features
X, y = user_df_prepocessed[DRIVER_CONTINUOUS_USER_FEATURES + GENERAL_CONTINUOUS_USER_FEATURES], user_df_prepocessed['aggregate_falsity_score']

# Create training and testing splits
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print (X_train.shape, y_train.shape)
print (X_test.shape, y_test.shape)

# Initialize model
model = RandomForestModel()
# model = LinearRegressionModel()

# Fit model
model.fit(X_train, y_train)
# model.grid_search(X_train, y_train) # Try grid search for parameter selection

# Predict
y_pred = model.predict(X_test)

# Plot and save results
fig, ax = plt.subplots()

ax.scatter(y_test, y_pred)
ax.set_xlabel("True Values")
ax.set_ylabel('Predictions')
ax.set_title('Random Forest Model')

fig.savefig(dir.REPO_PATH / f'falsity_prediction/plots/random_forest_grid_search_no_extremes.png', format='png')