import sys
from pathlib import Path

gen_dir = str(Path(__file__).resolve().parents[3])
if gen_dir not in sys.path:
    sys.path.append(gen_dir)

import pickle

import pandas as pd

from utils import unzip as uz

county = "HarrisCounty"

with open(gen_dir + '/data/created_data/' + county + '/segid_to_refspeed.pkl', "rb") as f:
    test = pickle.load(f)
print(test)

print(len(test))