import pandas as pd
from sklearn.naive_bayes import GaussianNB
import csv
import numpy as np



tdf = pd.read_csv("../datasets/bank/train_indessa.csv")

columns =  tdf.columns.tolist()
print columns 

print tdf.describe()


# TODO : home_ownership ["OWN","MORTGAGE","RENT"]
# TODO : initial_list_status ['w','f']
# TODO : last_week_pay , term
# TODO : sub_grade

#cols_to_keep = ['member_id', 'loan_amnt', 'funded_amnt', 'funded_amnt_inv', 'term', 'int_rate', 'sub_grade', 'home_ownership', 'annual_inc', 'dti', 'inq_last_6mths', 'mths_since_last_record', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 'initial_list_status', 'total_rec_int', 'total_rec_late_fee', 'recoveries', 'collection_recovery_fee', 'collections_12_mths_ex_med', 'mths_since_last_major_derog',  'last_week_pay', 'acc_now_delinq', 'tot_coll_amt', 'tot_cur_bal', 'total_rev_hi_lim', 'loan_status']
##tdf[cols_to_keep].to_csv("../datasets/bank/train_indessa_svm.csv")