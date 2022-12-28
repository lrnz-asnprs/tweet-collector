import pickle
import pandas as pd
import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector')

from fake_collector.configs.directory_config import Directories
from fake_collector.utils.load_fake_true_users import load_all_fake_users_df

dir = Directories()

# Load user features
user_features_dir = dir.USERS_PATH / 'fake_users'
with open(user_features_dir / 'fake_users_ALL_driver_features_v2.pickle', 'rb') as f:
    user_features = pickle.load(f)

user_features = user_features.reset_index().rename(columns={'index':'user_id'})
user_features['user_id'] = user_features['user_id'].astype(str)

user_features.to_csv('../data/falsebelief_users.csv')

# Save feature importances of RF
def save_feature_importance_plot_forest(model, model_type: str):

    dir = Directories()
    feature_names = model.model.feature_names_in_

    mdi_importances = pd.Series(
        model.model.feature_importances_, index=feature_names
    ).sort_values(ascending=True)

    ax = mdi_importances.plot.barh()
    ax.set_title("Random Forest Feature Importances (MDI)")
    ax.figure.tight_layout()

    ax.figure.savefig(dir.REPO_PATH / f'falsity_prediction/plots/random_forest_{model_type}_feature_importance_drivers_only.png', format='png')


# Load user data
def load_user_driver_data():

    dir = Directories()

    # Load user features
    user_features_dir = dir.USERS_PATH / 'fake_users'
    with open(user_features_dir / 'fake_users_ALL_driver_features_v2.pickle', 'rb') as f:
        user_features = pickle.load(f)

    user_features = user_features.reset_index().rename(columns={'index':'user_id'})
    user_features['user_id'] = user_features['user_id'].astype(str)

    user_features.columns

    # Load ideology features of users
    ideology_features = pd.read_csv(dir.DATA_PATH / 'driver_scores/worldview_driver_v2.csv')
    ideology_features.rename(columns={'index':'user_id'}, inplace=True)
    ideology_features['user_id'] = ideology_features['user_id'].astype(str)

    # Remove the ones without any political stance
    ideology_features.dropna(inplace=True)
    # Select relevant features
    ideology_features = ideology_features[['user_id', 'ideology_score', 'worldview_alignment', 'news_count']]

    # Load initial user df
    fake_users = load_all_fake_users_df()
    fake_users['user_id'] = fake_users['user_id'].astype(str)

    # Merge features into initial user df
    user_df = fake_users.merge(user_features, on='user_id', how='inner').merge(ideology_features, on='user_id', how='inner')

    return user_df


# Function that splits dataframe in 3 or 5 equal chunks (quintiles) based on column

def split_in_quantile_chunks(df: pd.DataFrame, column: str, quantiles: int):

    df = df.copy()

    if quantiles == 5:
        labels = ["0_very_low", "1_low", '2_medium', "3_high", '4_very_high']
    elif quantiles == 3:
        labels = ["0_low", '1_medium', "2_high"]
    elif quantiles == 2:
        labels = ["0_low", "1_high"]

    df["quantile_"+column] = pd.qcut(df[column], q=quantiles, labels=labels)
    
    return df

def split_in_ranges(df: pd.DataFrame, column: str, below: int, above: int):

    df = df.copy()

    def _apply_split(x):
        if x < below: return '0_low'
        elif x >= below and x <= above: return '1_medium'
        else: return '2_high'

    df['range_'+column] = df[column].apply(_apply_split)

    return df