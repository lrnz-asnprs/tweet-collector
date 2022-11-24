import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector')
import pickle
from models.regression_models import RandomForestRegressionModel, LinearRegressionModel
from models.classification_models import RandomForestClassificationModel
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from fake_collector.configs.directory_config import Directories
from fake_collector.utils.load_fake_true_users import load_all_fake_users_df
from falsity_prediction.model_config.features_config import DRIVER_CONTINUOUS_USER_FEATURES, GENERAL_CONTINUOUS_USER_FEATURES, DRIVER_BINARY_USER_FEATURES
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from preprocessing.user_preprocessor import UserPreprocessor
import pandas as pd
import math
from model_helpers import load_user_driver_data, save_feature_importance_plot_forest, split_in_chunks

"""
Script for model training and evaluation
"""

def run_regression_random_forest_model(model_type: str, continuous_features: list, target: str, save: bool):
    """
    Model type: simple or grid_search
    Continuous features: DRIVER_CONTINUOUS_USER_FEATURES
    target: aggregate_falsity_score or average_falsity_score
    save: true or false
    """

    dir = Directories()

    # Load user features
    user_df = load_user_driver_data()

    # Test on different groups
    # user_df = [user_df['fake_group'] != 'very_high']

    # Preprocess user features
    user_preprocessor = UserPreprocessor(continuous_columns = continuous_features)
    user_df_prepocessed = user_preprocessor.fit_transform(user_df)

    # Select X and y features
    X, y = user_df_prepocessed[continuous_features], user_df_prepocessed[target]

    # Create training and testing splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    print (X_train.shape, y_train.shape)
    print (X_test.shape, y_test.shape)

    # Initialize model
    model = RandomForestRegressionModel(type=model_type)
    # model = LinearRegressionModel()

    # Fit model
    model.fit(X_train, y_train)
    # model.grid_search(X_train, y_train) # Try grid search for parameter selection

    # Predict
    y_pred = model.predict(X_test)

    # Save feature importances
    # save_feature_importance_plot_forest(model=model, model_type='grid_search')

    # Plot and save results
    fig, ax = plt.subplots()

    ax.scatter(y_test, y_pred)
    ax.set_xlabel("True Values")
    ax.set_ylabel('Predictions')
    ax.set_title(f'Model Results Random Forest {model_type}')

    plt.axis('scaled')

    if save:
        save_feature_importance_plot_forest(model=model, model_type=model_type)
        fig.savefig(dir.REPO_PATH / f'falsity_prediction/plots/random_forest_{model_type}.png', format='png')

        # save
        with open(f'trained_models/{model_type}_random_forest.pkl','wb') as f:
            pickle.dump(model,f)

# Run regression
run_regression_random_forest_model(model_type='grid_search', continuous_features=DRIVER_CONTINUOUS_USER_FEATURES, target='aggregate_falsity_score', save=True)



def run_classification_random_forest_model(model_type: str, continuous_features: list, target: str, save: bool):
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
    user_df = split_in_chunks(user_df, 'aggregate_falsity_score', 2)

    # Preprocess user features
    user_preprocessor = UserPreprocessor(continuous_columns = continuous_features)
    user_df_prepocessed = user_preprocessor.fit_transform(user_df)

    # Select X and y features
    X, y = user_df_prepocessed[continuous_features], user_df_prepocessed[target]

    # Create training and testing splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    print (X_train.shape, y_train.shape)
    print (X_test.shape, y_test.shape)

    # Initialize model
    model = RandomForestClassificationModel(model_type=model_type)

    # Fit model
    model.fit(X_train, y_train)
    # model.grid_search(X_train, y_train) # Try grid search for parameter selection

    # Predict
    y_pred = model.predict(X_test)

    # Save feature importances
    # save_feature_importance_plot_forest(model=model, model_type='grid_search')

    # if save:
    #     save_feature_importance_plot_forest(model=model, model_type=model_type)
    #     fig.savefig(dir.REPO_PATH / f'falsity_prediction/plots/random_forest_{model_type}.png', format='png')


# dir = Directories()

# # Load user features
# user_df = load_user_driver_data()

# # Split in 3 different groups
# user_df = split_in_chunks(user_df, 'aggregate_falsity_score', 2)
# user_df.columns
# user_df[user_df['worldview_alignment'] == 0]


run_classification_random_forest_model(model_type='simple', continuous_features = DRIVER_CONTINUOUS_USER_FEATURES + GENERAL_CONTINUOUS_USER_FEATURES, target = 'group_aggregate_falsity_score', save = False)
