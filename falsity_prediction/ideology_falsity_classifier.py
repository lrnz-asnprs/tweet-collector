import sys
import os
sys.path.append('/Users/laurenzaisenpreis/Uni/Thesis/tweet-collector')

from models.regression_models import RandomForestRegressionModel, LinearRegressionModel
from models.classification_models import RandomForestClassificationModel, LogRegClassificationModel
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

# user_df['range_aggregate_falsity_score'].value_counts()

"""
Select only users with actual driver scores
"""
user_df = user_df[
    (user_df['weighted_average_falsity_mutual_friends'].notna()) &
    (user_df['elite_exposure_score'] >= 0) &
    (user_df['news_count'] >= 5)
]

user_df.plot(kind='scatter', x='average_falsity_score', y='ideology_score')

# user_df = user_with_scores

# Create training and testing splits
X_train, X_test, y_train, y_test = train_test_split(user_df[['ideology_score']], user_df['quantile_average_falsity_score'], test_size=0.2, random_state=35)
print (X_train.shape, y_train.shape)
print (X_test.shape, y_test.shape)

"""
Model configs:
"""
model_type = 'simple'

X_train

# Initialize model
model = LogRegClassificationModel(model_type=model_type)

# Fit model
model.fit(X_train, y_train)
# model.grid_search(X_train, y_train) # Try grid search for parameter selection

# model.predict_eval(X_test, y_test, target_names=target_names)

'''
Classification report
'''
y_pred = model.predict(X_test)

cl_report = classification_report(y_test, y_pred, output_dict=True)

report = pd.DataFrame(cl_report).transpose().round(3)

precision_score(y_test, y_pred, labels=['0_low', '1_high'], average='macro')
recall_score(y_test, y_pred, labels=['0_low', '1_high'], average='macro')
f1_score(y_test, y_pred, average='macro')

print(report)
# report.to_latex('classification_results_ideology_log_regression.tex')

"""
Plot feature importances
"""

feature_names = model.model.feature_names_in_

feature_names = [FEATURES_TO_DRIVER_NAME.get(feature_name) for feature_name in feature_names]

mdi_importances = pd.Series(
    model.model.feature_importances_, index=feature_names
).sort_values(ascending=True)


import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import pandas as pd
import numpy as np

# create a normalizer
norm = Normalize(vmin=0, vmax=0.4)
# choose a colormap
cmap = cm.inferno
# map values to a colorbar
mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
mappable.set_array(mdi_importances.values)


fig, ax = plt.subplots()
bars = ax.barh(mdi_importances.index, mdi_importances.values)

ax = bars[0].axes
lim = ax.get_xlim()+ax.get_ylim()
for bar, val in zip(bars, mdi_importances.values):
    grad = np.atleast_2d(np.linspace(0,val,256)).T
    bar.set_zorder(1)
    bar.set_facecolor('none')
    x, y = bar.get_xy()
    w, h = bar.get_width(), bar.get_height()
    ax.imshow(np.flip(grad), extent=[x,x+w,y,y+h], aspect='auto', zorder=1,interpolation='nearest', cmap=cmap, norm=norm)
ax.axis(lim)
ax.set_title("Random Forest Feature Importances (MDI)")
plt.show()

# fig.savefig('feature_importance_analysis.png', bbox_inches='tight')

# ax.figure.tight_layout()


# from sklearn.inspection import permutation_importance

# # start_time = time.time()
# result = permutation_importance(
#     model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2
# )

# forest_importances = pd.Series(result.importances_mean, index=feature_names)

# fig, ax = plt.subplots()
# forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
# ax.set_title("Feature importances using permutation on full model")
# ax.set_ylabel("Mean accuracy decrease")
# fig.tight_layout()
# plt.show()