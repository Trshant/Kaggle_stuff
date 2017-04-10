from sklearn import svm
from sklearn import datasets
from sklearn import preprocessing
from sklearn.externals import joblib

import pandas as pd

#from paths import * 
training_filename="train_indessa_svm.csv"
training_model_pickle_filename="indessa_svm_model.pkl"
training_featureset_pickle_filename="indessa_featureset.pkl"

######################## input #####################################################
df=pd.read_csv(training_filename)
loc_train=-1   #location of the labels
loc_features=2  #location of features
############## labels ###################################
training_labels=df.ix[:,loc_train].copy().values #location of labels


########### feature matrix ##############################
feature_mat= df.ix[:,loc_features:-2].copy().values  #last column is values, so till before that
norm_feature_mat=preprocessing.normalize(feature_mat, norm='max')
print "normalized",feature_mat.shape
################### features used #####################
feature_set=df.ix[:,2:29].columns.values 
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
