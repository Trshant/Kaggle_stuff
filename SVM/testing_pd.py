import pandas as pd
from sklearn.naive_bayes import GaussianNB
import csv
import numpy as np

def GEThomeVAL(value):
	home_ownership = ["","OWN","MORTGAGE","RENT"]
	##value = "RENT"
	idx = -1
	while True:
	    try:
	        idx = home_ownership.index(value, idx+1)
	    except ValueError:
	        break

	return idx


def GETinitial_list_status(value):
	home_ownership = ["","w","f"]
	##value = "RENT"
	idx = -1
	while True:
	    try:
	        idx = home_ownership.index(value, idx+1)
	    except ValueError:
	        break

	return idx


def pull_first_num(ss):
	return re.findall(r'\d+', ss )[0]



def measureSbgrade(value):
	grades = ["","a","b","c","d","e","f"]
	grades_num = grades.index(value[0])
	return int(grades_num) * int(value[1])

tdf = pd.read_csv("../datasets/bank/train_indessa.csv")

columns =  tdf.columns.tolist()
print columns 

print tdf.describe()


# TODO : DONE : home_ownership ["OWN","MORTGAGE","RENT"]
# TODO : DONE : initial_list_status ['w','f']
# TODO : DONE : last_week_pay , term
# TODO : DONE : sub_grade

#cols_to_keep = ['member_id', 'loan_amnt', 'funded_amnt', 'funded_amnt_inv', 'term', 'int_rate', 'sub_grade', 'home_ownership', 'annual_inc', 'dti', 'inq_last_6mths', 'mths_since_last_record', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc', 'initial_list_status', 'total_rec_int', 'total_rec_late_fee', 'recoveries', 'collection_recovery_fee', 'collections_12_mths_ex_med', 'mths_since_last_major_derog',  'last_week_pay', 'acc_now_delinq', 'tot_coll_amt', 'tot_cur_bal', 'total_rev_hi_lim', 'loan_status']
##tdf[cols_to_keep].to_csv("../datasets/bank/train_indessa_svm.csv")