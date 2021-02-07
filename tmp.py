import subprocess

subprocess.call('history | grep jupyter', shell=True)

subprocess.call('echo $PATH', shell=True)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number", type=int)
args = parser.parse_args()

print(args.square**2)
