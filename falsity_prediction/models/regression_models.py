from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pandas as pd
from fake_collector.configs.directory_config import Directories

dir = Directories()

class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()

    def fit(self, X, y):
        self.model.fit(X, y)
        print("MAE:", mean_absolute_error(y, self.model.predict(X)))

    def predict(self, X):
        return self.model.predict(X)

    def predict_eval(self, X, y):
        print("Mean squared error")
        print(mean_squared_error(y, self.model.predict(X)))
        print()
        print('Mean absolute error')
        print(mean_absolute_error(y, self.model.predict(X)))
        print()
        print('R2 Score')
        print(r2_score(y, self.model.predict(X)))
        print('Adjusted R2 Score')
        r2 = r2_score(y, self.model.predict(X))
        no_observations = len(X)
        no_variables = len(X.columns)
        adjusted_r2 = 1 - ((1-r2)*(no_observations-1)/(no_observations-no_variables-1))
        print(adjusted_r2)


class RandomForestRegressionModel:
    def __init__(self, type: str):
        """
        Type: simple or grid_search
        """
        if type == 'grid_search':
            self.model = RandomForestRegressor(
                n_estimators=400,
                max_features=5,
                min_samples_split=10,
                criterion='absolute_error',
                max_depth=16,
            )
        elif type == 'simple':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=8,
            )

    def fit(self, X, y):
        print("Training RF regressor.")
        self.model.fit(X, y)
        # Evaluate predictions
        self.feature_importance()

    def grid_search(self, X, y):
        parameters = {
            'max_features': np.arange(5,10),
            'n_estimators':[100, 200, 400],
            'max_depth':[4, 8, 16],
            'min_samples_split':[1, 5, 10]
        }
        clf = GridSearchCV(self.model, parameters, cv=4, n_jobs=4, verbose=3, scoring='neg_mean_absolute_error')
        clf.fit(X,y)

        print(clf.best_score_)
        print(clf.best_params_)
        self.model = clf


    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def predict_eval(self, X, y):
        """
        Plug in X_test, y_test here
        """
        print("Mean squared error")
        print(mean_squared_error(y, self.model.predict(X)))
        print()
        print('Mean absolute error')
        print(mean_absolute_error(y, self.model.predict(X)))
        print()
        print('R2 Score')
        print(r2_score(y, self.model.predict(X)))
        print('Adjusted R2 Score')
        r2 = r2_score(y, self.model.predict(X))
        no_observations = len(X)
        no_variables = len(X.columns)
        adjusted_r2 = 1 - ((1-r2)*(no_observations-1)/(no_observations-no_variables-1))
        print(adjusted_r2)

    def feature_importance(self):

        feature_names = self.model.feature_names_in_

        mdi_importances = pd.Series(
            self.model.feature_importances_, index=feature_names
        ).sort_values(ascending=True)

        ax = mdi_importances.plot.barh()
        ax.set_title("Random Forest Feature Importances (MDI)")
        ax.figure.tight_layout()
        
