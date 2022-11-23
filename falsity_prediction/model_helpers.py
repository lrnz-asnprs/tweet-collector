import pickle
import pandas as pd
import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector')

from fake_collector.configs.directory_config import Directories
from fake_collector.utils.load_fake_true_users import load_all_fake_users_df


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
    with open(user_features_dir / 'fake_users_driver_features.pickle', 'rb') as f:
        user_features = pickle.load(f)

    user_features = user_features.reset_index().rename(columns={'index':'user_id'})
    user_features['user_id'] = user_features['user_id'].astype(str)

    # Load ideology features of users
    ideology_features = pd.read_csv(dir.DATA_PATH / 'driver_scores/worldview_driver.csv')
    ideology_features.rename(columns={'index':'user_id'}, inplace=True)
    ideology_features['user_id'] = ideology_features['user_id'].astype(str)
    # Remove the ones without any political stance
    ideology_features.dropna(inplace=True)
    # Select relevant features
    ideology_features = ideology_features[['user_id', 'ideology_score', 'worldview_alignment']]

    # Load initial user df
    fake_users = load_all_fake_users_df()
    fake_users['user_id'] = fake_users['user_id'].astype(str)

    # Merge features into initial user df
    user_df = fake_users.merge(user_features, on='user_id', how='inner').merge(ideology_features, on='user_id', how='inner')

    return user_df


# Function that splits dataframe in 3 or 5 equal chunks (quintiles) based on column

def split_in_chunks(df: pd.DataFrame, column: str, no_splits: int):

    df = df.copy()

    if no_splits == 5:
        labels = ["very_low", "low", 'medium', "high", 'very_high']
    elif no_splits == 3:
        labels = ["low", 'medium', "high"]
    elif no_splits == 2:
        labels = ["low", "high"]

    df["group_"+column] = pd.qcut(df[column], q=no_splits, labels=labels)
    
    return df