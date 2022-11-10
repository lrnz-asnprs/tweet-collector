from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()

    def fit(self, X, y):
        self.model.fit(X, y)
        print("MAE:", mean_absolute_error(y, self.model.predict(X)))

    def predict(self, X):
        return self.model.predict(X)


class RandomForestModel:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=400,
            max_features=5,
            min_samples_split=10,
            criterion='absolute_error',
            max_depth=16,
        )
        # self.model = RandomForestRegressor(
        #     n_estimators=100,
        #     max_depth=8,
        # )

    def fit(self, X, y):
        print("Training RF regressor.")
        self.model.fit(X, y)
        # Evaluate predictions
        self.predict_eval(X, y)

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
        print("Mean squared error")
        print(mean_squared_error(y, self.model.predict(X)))
        print()
        print('Mean absolute error')
        print(mean_absolute_error(y, self.model.predict(X)))
        print()
        print('R2 Score')
        print(r2_score(y, self.model.predict(X)))

