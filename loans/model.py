#!/usr/bin/env python

from add_encoder import dtrain, dtest, dfs

import xgboost as xgb
import pandas as pd

'''# specify parameters via map
param = {'booster': 'dart',
         'max_depth': 5, 'learning_rate': 0.1,
         'objective': 'binary:logistic',
         'silent': True,
         'sample_type': 'uniform',
         'normalize_type': 'tree',
         'rate_drop': 0.1,
         'skip_drop': 0.5}
num_round = 50
'''
param = {'max_depth':7, 'eta':1, 'silent':1, 'objective':'binary:logistic' }
num_round = 5


bst = xgb.train(param, dtrain, num_round)
# make prediction
# ntree_limit must not be 0
preds = bst.predict(dtest, ntree_limit=num_round)

preds_df = pd.DataFrame({'id': dfs['TEST_IDs'], 'charged_off': preds})
