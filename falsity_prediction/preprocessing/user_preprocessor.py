from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
import pandas as pd
from typing import List
from sklearn.impute import SimpleImputer
import numpy as np

class UserPreprocessor:
    """
    Preprocessor for tabular user features.
    """
    def __init__(
        self,
        continuous_columns: List[str],
        onehot_columns: List[str] = None,
        binary_columns: List[str] = None,
    ):
        self.onehot_columns = onehot_columns
        self.continuous_columns = continuous_columns
        self.binary_columns = binary_columns
        self.enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
        self.binarizer = LabelEncoder()
        self.standardize = StandardScaler()
        self.imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

    def clean(self, df):
        clean = df.copy()
        # Change if needed
        return clean

    def fit(self, df):
        self.imputer.fit(df[self.continuous_columns])
        self.standardize.fit(df[self.continuous_columns])
        if self.onehot_columns != None:
            self.enc.fit(df[self.onehot_columns])
        if self.binary_columns != None:
            self.binarizer.fit(df[self.binary_columns])

    def get_onehot_colnames(self):
        col_names = []
        for i, col in enumerate(self.onehot_columns):
            col_names = col_names + [
                col + "_" + str(a) for a in self.enc.categories_[i]
            ]
        return col_names

    def process_enc(self, df):
        df_out = df.copy()
        # impute missing values in continuous features
        df_out[self.continuous_columns] = self.imputer.transform(df_out[self.continuous_columns])
        # conduct standard scaling
        standardize = self.standardize.transform(df_out[self.continuous_columns])
        df_out[self.continuous_columns] = standardize
        # conduct one hot encoding
        if self.onehot_columns != None:
            onehot = self.enc.transform(df_out[self.onehot_columns])
            df_out[self.get_onehot_colnames()] = onehot
            df_out = df_out.drop(self.onehot_columns, axis=1)
        if self.binary_columns != None:
            df_out[self.binary_columns[0]] = self.binarizer.transform(df_out[self.binary_columns[0]])
        return df_out

    def fit_transform(self, df):
        df = self.clean(df)
        self.fit(df)
        df = self.process_enc(df)
        return df

    def transform(self, df):
        df = self.clean(df)
        df = self.process_enc(df)
        return df

    def inverse_trans(self, df):
        # inverse transform the standardize scaling
        standardize_inverse = self.standardize.inverse_transform(df[self.continuous_columns])
        df[self.continuous_columns] = standardize_inverse
        # inverse transform the one hot encoding
        if self.onehot_columns != None:
            onehot_inverse = self.enc.inverse_transform(df[self.get_onehot_colnames()])
            df[self.onehot_columns] = onehot_inverse
            df = df.drop(self.get_onehot_colnames(), axis=1)
        if self.binary_columns != None:
            binary_inverse = self.binarizer.inverse_transform(df[self.binary_columns])
            df[self.binary_columns] = binary_inverse
        return df

    def get_xdata(self, df, other_features):
        return df[other_features + self.get_onehot_colnames()].values
