import pandas as pd
from sklearn.naive_bayes import GaussianNB
import csv
import numpy as np

class NaiveBayes_Basic:
    def readCSV_train(self, filename):
        self.train_df = pd.read_csv(filename)
        return self
    def preprocess_training(self):
        self.train_df['Age'].fillna(30.0, inplace=True)
        self.train_df['Sex'] = self.train_df['Sex'].map({'female': 1, 'male': 0})

        self.train_df['Pclass'].apply(int)
        self.train_df['Fare'].apply(int)
        self.train_df['Parch'].apply(int)
        self.train_df['Age'].apply(float)
        self.train_df['SibSp'].apply(int)
        self.train_df['Sex'].apply(int)
        return self
    
    def train(self , indexx , features_list ):
        survival=self.train_df[indexx].values.tolist()
        featurespace=self.train_df[ features_list ].values.tolist()
        gnb = GaussianNB()
        self.classifier= gnb.fit(featurespace, survival)
        return self

    def readCSV_test(self, filename):
        self.test_df = pd.read_csv(filename)
        return self

    def preprocess_testing(self):
        self.test_df['Age'].fillna(30.0, inplace=True)
        self.test_df['Fare'].fillna(35.6, inplace=True)
        self.test_df['Sex'] = self.test_df['Sex'].map({'female': 1, 'male': 0})
        
        self.test_df['Pclass'].apply(int)
        self.test_df['Fare'].apply(int)
        self.test_df['Parch'].apply(int)
        self.test_df['Age'].apply(float)
        self.test_df['SibSp'].apply(int)
        self.test_df['Sex'].apply(int)
        return self

    def test(self , indexx , features_list ): 
        main=self.test_df[indexx].values.tolist()
        featurespace=self.test_df[features_list].values.tolist()  
        self.results=self.classifier.predict(featurespace)
        self.res=zip(main,self.results)
        return self
    def write_csv(self , filename):
        self.result = [list(elem) for elem in self.res]
        ofile  = open(filename , "wb")
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
 
        for row in self.result:
            writer.writerow(row)

        ofile.close()
        return self

simplebayes = NaiveBayes_Basic()
tr = simplebayes.readCSV_train('./files/train.csv').preprocess_training().train('Survived' ,  ['Pclass','Sex','SibSp','Age','SibSp','Parch','Fare'] )
tr = tr.readCSV_test('./files/test.csv').preprocess_testing().test( 'PassengerId' , ['Pclass','Sex','SibSp','Age','SibSp','Parch','Fare'] ).write_csv('./files/gen_op.csv')
print tr.results