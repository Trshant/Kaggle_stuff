import pandas as pd
from sklearn.naive_bayes import GaussianNB
import csv
import numpy as np



tdf = pd.read_csv("../datasets/bank/train_indessa.csv")
print tdf.head(1)
