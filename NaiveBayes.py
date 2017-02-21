import pandas as pd
from sklearn.naive_bayes import GaussianNB
import csv
import numpy as np


def train(df):
   #df['Age'].fillna('30.0', inplace=True )
    featurespace=[]
    survival=[]
    for index, row in df.iterrows():
        fr=[]
        fr.append(int(row["Pclass"]))
        if row["Sex"]=='male':
            fr.append(0)
        else:
            fr.append(1)
        ##print pd.isnull(df['Age'])
        fr.append(float(row["Age"]))
        fr.append(int(row["SibSp"]))
        fr.append(int(row["Parch"]))
        fr.append(float(row["Fare"]))
        featurespace.append(fr)
        survival.append(row["Survived"])
    gnb = GaussianNB()
    nb_classifier= gnb.fit(featurespace, survival)
    return nb_classifier

def test(classifier , df):
    #df['Age'].fillna('30.0',inplace=True) 
    #df['Fare'].fillna('35.6', inplace=True ) 
    featurespace=[]
    main=[]
    for index, row in df.iterrows():
        fr=[]
        main.append(int(row["PassengerId"]))
        fr.append(int(row["Pclass"]))
        if row["Sex"]=='male':
            fr.append(0)
        else:
            fr.append(1)
        fr.append(float(row["Age"])) 
        fr.append(int(row["SibSp"])) 
        fr.append(int(row["Parch"])) 
        fr.append(float(row["Fare"]))
        featurespace.append(fr)	
    results=classifier.predict(featurespace)
    res=zip(main,results)
    return res

def read_CSV(filename):
	df = pd.read_csv(filename)
	return df

def mung_na(df,colname,colval_new):
	df[colname].fillna(colval_new,, inplace=True)
	return df
	
train_df=read_CSV('./files/train.csv')

train_df=mung_na(train_df, 'Age','30.0')


test_df=read_CSV('./files/test.csv')

test_df=mung_na(test_df, 'Age','30.0')
test_df=mung_na(test_df, 'Fare','35.6')

classifier = train(train_df)
tr = test(classifier,test_df)
print tr
## TODO : make this into a nice class