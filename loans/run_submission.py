#!/usr/bin/env python

from model import preds_df
from subprocess import call
bsh = lambda s: call(s, shell=True)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("message", help="I need a message")
args = parser.parse_args()

def write_submit(submit_df,
                 filename='submission.csv',
                 message=args.message):
    ''''''
    submit_df.to_csv(filename, index=False)
    s0 = "kaggle competitions submit -c ds1-tree-ensembles -f "
    s1 = f"""{filename} -m "{message}" """

    try:
        bsh(s0+s1)
    except Exception as e:
        print(e)

if __name__=='__main__':
    #print(preds_df)
    write_submit(preds_df)
