from sklearn import svm
from sklearn import datasets
from sklearn import preprocessing
from sklearn.externals import joblib

import pandas as pd
import numpy as np
import csv

from paths import *

def testing(df, loc_features):
	test_feature_mat= df.ix[:,loc_features:-1].copy().values
	################### features used #####################
	feature_set=joblib.load(testing_featureset_pickle_filename)
	
	test_feature_set=df.ix[:,loc_features:-1].columns.values 
	test_data_features=np.zeros((test_feature_mat.shape[0],len(feature_set)))
	
	for i in range(0,len(feature_set)):
		n=feature_set[i]
		if n in test_feature_set:
			matchind=np.where(test_feature_set==n)
			col=test_feature_mat[:,matchind].flatten()
			test_data_features[:,i]=col
	norm_test_feature_mat=preprocessing.normalize(test_data_features, norm='max')
	del(test_data_features)
	del(test_feature_mat)
	print "normalized"
	############################# classifier ###################################
	clf_svm = joblib.load(testing_model_pickle_filename)
	prediction =clf_svm.predict(norm_test_feature_mat)

	colnames=df.ix[:,0:loc_features].columns.values 
	#colnames=['Num','Desc']
	#colnames.append("Prediction")
	colnames=np.append(colnames,"Prediction")
	print colnames
	
	#print "colnames",colnames,len(prediction)
	return prediction,colnames
	

