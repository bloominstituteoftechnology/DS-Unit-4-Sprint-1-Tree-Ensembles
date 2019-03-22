#!/usr/bin/env python

from clean import clean, TRAIN_LABELS, TRAINPATH, TESTPATH
import pandas as pd
import category_encoders as ce
import xgboost as xgb

def encode(encoder, trainpath = TRAINPATH, testpath = TESTPATH):
    ''' pass a fresh encoder instance from ce library. '''

    df_test = clean(pd.read_csv(testpath))

    X_train = encoder.fit_transform(clean(pd.read_csv(trainpath))[0])
    X_test = encoder.fit_transform(df_test[0])

    return {'train': X_train, 'test': X_test, 'TEST_IDs': df_test[1]}

dfs = encode(ce.OneHotEncoder())

y_train = pd.read_csv(TRAIN_LABELS[0])[TRAIN_LABELS[1]]

dtrain = xgb.DMatrix(dfs['train'].values, y_train.values)
dtest = xgb.DMatrix(dfs['test'].drop(['purpose_13'], axis=1).values) # don't ask

