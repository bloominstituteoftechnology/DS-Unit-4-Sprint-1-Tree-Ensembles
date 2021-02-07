#!/usr/bin/env python

from ipywidgets import interact
import pandas as pd
import numpy as np
import logging
#import matplotlib.pyplot as plt
#plt.style.use('dark_background')
#from sklearn.preprocessing import FunctionTransformer, StandardScaler
#from sklearn.ensemble import RandomForestRegressor
#from sklearn.model_selection import train_test_split, cross_val_score
#from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
#from sklearn.decomposition import PCA
#from sklearn.linear_model import LogisticRegression
#from sklearn.pipeline import Pipeline
#from sklearn.compose import ColumnTransformer
import xgboost as xgb
import category_encoders as ce

TRAIN_LABELS = ('train_labels.csv', 'charged_off')
TRAINPATH = 'train_features.csv'
TESTPATH = 'test_features.csv'


def clean(dat: pd.DataFrame) -> pd.DataFrame:
    ''' refactored Ryan H's wrangle function from lecture today into method chaining'''
    greater_than_10k_ = [k for k,v in dat.mean().iteritems() if v > 10**4]

    todrop_ = ['id', # id is random
              'member_id', # all null
              'url', # all null
              'desc', # all null
              'title', # duplicate of purpose
              'grade', # duplicate of sub_grade
              'emp_title', # getting re-engineered, cardinality too high
              'zip_code' # cardinality too high
               # list `greater_than_10k` will be engineered into units of k
             ]

    many_nulls = ['sec_app_mths_since_last_major_derog',
                  'sec_app_revol_util',
                  'sec_app_earliest_cr_line',
                  'sec_app_mort_acc',
                  'dti_joint',
                  'sec_app_collections_12_mths_ex_med',
                  'sec_app_chargeoff_within_12_mths',
                  'sec_app_num_rev_accts',
                  'sec_app_open_act_il',
                  'sec_app_open_acc',
                  'revol_bal_joint',
                  'annual_inc_joint',
                  'sec_app_inq_last_6mths',
                  'mths_since_last_record',
                  'mths_since_recent_bc_dlq',
                  'mths_since_last_major_derog',
                  'mths_since_recent_revol_delinq',
                  'mths_since_last_delinq',
                  'il_util',
                  'emp_length',
                  'mths_since_recent_inq',
                  'mo_sin_old_il_acct',
                  'mths_since_rcnt_il',
                  'num_tl_120dpd_2m',
                  'bc_util',
                  'percent_bc_gt_75',
                  'bc_open_to_buy',
                  'mths_since_recent_bc']

    greater_than_10k = [i for i in greater_than_10k_ if i not in many_nulls]

    todrop = [i for i in todrop_ if i not in many_nulls] + greater_than_10k

    def wrangle_sub_grade(x):
        '''Transform sub_grade from "A1" - "G5" to 1.1 - 7.5'''
        first_digit = ord(x[0]) - 64
        second_digit = int(x[1])
        return first_digit + second_digit/10

    assigns = {# sub_grade to ordinal
        **{'sub_grade': dat.sub_grade.apply(wrangle_sub_grade)}, # sub_grade to ordinal
        # Convert percentages from strings to floats
        **{name: dat[name].str.strip('%').astype(float)
                 for name in ['int_rate', 'revol_util']}, # Convert percentages from strings to floats
        # Transform earliest_cr_line to an integer: how many days it's been open
        **{'earliest_cr_line': (pd.Timestamp.today() - \
                                  pd.to_datetime(dat.earliest_cr_line, infer_datetime_format=True)
                               ).dt.days},
        # Create features for three employee titles: teacher, manager, owner
        **{'emp_title_'+name: dat.emp_title.str.contains(name, na=False)
                              for name in ['teacher', 'manager', 'owner']},
        # Transform features with many nulls to binary flags
        **{name: dat[name].isnull() for name in many_nulls},
        # For features with few nulls, do mean imputation
        **{name: dat[name].fillna(dat[name].mean()) for name in dat.select_dtypes(include=['int', 'float', 'float64']).columns}
              }

    return (dat.assign(emp_title = dat.emp_title.str.lower())
               .assign(**assigns)
               .drop(todrop, axis=1)), dat.id.values
