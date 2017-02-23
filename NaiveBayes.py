import pandas as pd
from sklearn.naive_bayes import GaussianNB
import csv
import numpy as np

def data_munging( test_df ):
    test_df['Age'].fillna(30.0, inplace=True)
    test_df['Fare'].fillna(35.6, inplace=True)
    test_df['Sex'] = test_df['Sex'].map({'female': 1, 'male': 0})
    
    test_df['Pclass'].apply(int)
    test_df['Fare'].apply(int)
    test_df['Parch'].apply(int)
    test_df['Age'].apply(float)
    test_df['SibSp'].apply(int)
    test_df['Sex'].apply(int)

    return test_df


class NaiveBayes_BasicFns:
    
    def preprocess(self , mode ):
        if mode == "training":
            self.train_df = data_munging( self.train_df )

        if mode == "testing":
            self.test_df = data_munging( self.test_df )    
        return self
    
    def test_naive(self , indexx , features_list ): 
        main=self.test_df[indexx].values.tolist()
        featurespace=self.test_df[features_list].values.tolist()  
        self.results=self.classifier.predict(featurespace)
        self.result = [list(elem) for elem in zip(main,self.results)]
        return self

    def train_naive(self , indexx , features_list ):
        survival=self.train_df[indexx].values.tolist()
        featurespace=self.train_df[ features_list ].values.tolist()
        gnb = GaussianNB()
        self.classifier= gnb.fit(featurespace, survival)
        return self

    def readCSV_train(self, filename):
        self.train_df = pd.read_csv(filename)
        return self

    def readCSV_test(self, filename):
        self.test_df = pd.read_csv(filename)
        return self
    
    def write_csv(self , filename):
        ofile  = open(filename , "wb")
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
 
        for row in self.result:
            writer.writerow(row)

        ofile.close()
        return self

simplebayes = NaiveBayes_BasicFns()
tr = simplebayes.readCSV_train('./files/train.csv').preprocess('training').train_naive('Survived' ,  ['Pclass','Sex','SibSp','Age','SibSp','Parch','Fare'] )
tr = tr.readCSV_test('./files/test.csv').preprocess('testing').test_naive( 'PassengerId' , ['Pclass','Sex','SibSp','Age','SibSp','Parch','Fare'] ).write_csv('./files/gen_op.csv')
print tr.results