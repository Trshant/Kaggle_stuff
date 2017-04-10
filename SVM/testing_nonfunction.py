from sklearn import svm
from sklearn import datasets
from sklearn import preprocessing
from sklearn.externals import joblib

import pandas as pd
import numpy as np
import csv

#from paths import *
testing_filename="text_indessa_svm.csv"
training_model_pickle_filename="indessa_svm_model.pkl"
training_featureset_pickle_filename="indessa_featureset.pkl"
outputfilename="result_indessa_svm.csv"


######################## input #####################################################
df=pd.read_csv(testing_filename)
loc_features=2   #location of the features start


test_feature_mat= df.ix[:,loc_features:-1].copy().values
print test_feature_mat.shape
################### features used #####################
	
feature_set=joblib.load(training_featureset_pickle_filename)
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
clf_svm = joblib.load(training_model_pickle_filename)
print norm_test_feature_mat.shape
prediction =clf_svm.predict(norm_test_feature_mat)
colnames=df.ix[:,0:loc_features].columns.values 


print "here", prediction
combined=zip(df.ix[:,0].values,prediction)
print combined
for c in combined:
	with open(outputfilename, 'a+') as csvfileout2:
		spamwriter2 = csv.writer(csvfileout2)
		spamwriter2.writerow([c[0],c[1]])
