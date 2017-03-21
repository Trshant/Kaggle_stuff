from sklearn import svm
from sklearn import datasets
from sklearn import preprocessing
from sklearn.externals import joblib

import pandas as pd

training_model_pickle_filename = "bank_model_save.mdl"
training_featureset_pickle_filename = "bank_featureset_pickle_save.fts"
training_filename = "filename.csv"

from paths import * 
######################## input #####################################################
df=pd.read_csv(training_filename)
loc_train=4   #location of the labels

############## labels ###################################
training_labels=df.ix[:,4].copy().values #[r for r in df['Risk Type']]


########### feature matrix ##############################
feature_mat= df.ix[:,5:-1].copy().values
norm_feature_mat=preprocessing.normalize(feature_mat, norm='max')
print "normalized",feature_mat.shape
################### features used #####################
feature_set=df.ix[:,5:-1].columns.values 
joblib.dump(feature_set, training_featureset_pickle_filename)
print "feature set written"


del(feature_mat)

############################# classifier ###################################
clf_svm = svm.SVC(gamma=0.001, C=100., kernel='linear',probability=True)
X, y = norm_feature_mat, training_labels
clf_svm.fit(X, y)  

################################ pickle #####################################
joblib.dump(clf_svm, training_model_pickle_filename) 
print "model written"
