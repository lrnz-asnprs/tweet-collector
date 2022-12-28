from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
from fake_collector.configs.directory_config import Directories

dir = Directories()


class RandomForestClassificationModel:
    def __init__(self, model_type: str):
        if model_type == 'simple':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=8,
            )
        elif model_type == 'grid_search':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=16,
                max_features=9,
                min_samples_split=5,
            )

    def fit(self, X, y):
        print("Training RF classifier.")
        self.model.fit(X, y)
        # target_names = y.unique()
        # self.predict_eval(X, y, target_names)

    def grid_search(self, X, y):
        parameters = {
            'max_features': np.arange(5,10),
            'n_estimators':[100, 200, 400, 800],
            'max_depth':[4, 8, 16],
            'min_samples_split':[1, 5, 10]
        }
        clf = GridSearchCV(self.model, parameters, cv=4, n_jobs=4, verbose=3, scoring='f1_macro')
        clf.fit(X,y)

        print(clf.best_score_)
        print(clf.best_params_)
        self.model = clf


    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def predict_eval(self, X, y, target_names):
        target_names = y.unique()
        predictions = self.model.predict(X)
        print(classification_report(y,predictions))
         # Plot confusion matrix
        fig, ax = plt.subplots(figsize=(12, 8))
        cm = confusion_matrix(y, predictions, labels=target_names)
        sns.heatmap(cm, annot = True, cbar = False, fmt = "d", linewidths = .5, cmap = "Blues", ax = ax)
        ax.set_title("Confusion Matrix")
        ax.set_xlabel("Predicted class")
        ax.set_ylabel("Actual class")
        ax.set_xticklabels(target_names)
        ax.set_yticklabels(target_names)
        fig.tight_layout()


class LogRegClassificationModel:
    def __init__(self, model_type: str):
        if model_type == 'simple':
            self.model = LogisticRegression(
    
            )

    def fit(self, X, y):
        print("Training LogReg classifier.")
        self.model.fit(X, y)
        # target_names = y.unique()
        # self.predict_eval(X, y, target_names)

    # def grid_search(self, X, y):
    #     parameters = {
    #         'max_features': np.arange(5,10),
    #         'n_estimators':[100, 200, 400, 800],
    #         'max_depth':[4, 8, 16],
    #         'min_samples_split':[1, 5, 10]
    #     }
    #     clf = GridSearchCV(self.model, parameters, cv=4, n_jobs=4, verbose=3, scoring='f1_macro')
    #     clf.fit(X,y)

    #     print(clf.best_score_)
    #     print(clf.best_params_)
    #     self.model = clf


    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def predict_eval(self, X, y, target_names):
        target_names = y.unique()
        predictions = self.model.predict(X)
        print(classification_report(y,predictions))
         # Plot confusion matrix
        fig, ax = plt.subplots(figsize=(12, 8))
        cm = confusion_matrix(y, predictions, labels=target_names)
        sns.heatmap(cm, annot = True, cbar = False, fmt = "d", linewidths = .5, cmap = "Blues", ax = ax)
        ax.set_title("Confusion Matrix")
        ax.set_xlabel("Predicted class")
        ax.set_ylabel("Actual class")
        ax.set_xticklabels(target_names)
        ax.set_yticklabels(target_names)
        fig.tight_layout()
