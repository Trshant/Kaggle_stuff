from sklearn.naive_bayes import GaussianNB
import csv
import numpy as np

input_trainfilename='./files/train.csv'
input_testfilename='./files/test.csv'



def train():
	with open(input_trainfilename,"rb") as csvfile_sentiment:
		spamreader_sentiment = csv.reader(csvfile_sentiment)
		headers=spamreader_sentiment.next()
		featurespace=[]
		survival=[]
		for row in spamreader_sentiment:
			fr=[]
			fr.append(int(row[2]))
			if row[4]=='male':
				fr.append(0)
			else:
				fr.append(1)
			if row[5]!='':
				fr.append(float(row[5]))
			else:
				fr.append(30.0)
			fr.append(int(row[6]))
			fr.append(int(row[7]))
			fr.append(float(row[9]))
			featurespace.append(fr)
			survival.append(row[1])
			
		gnb = GaussianNB()

		nb_classifier= gnb.fit(featurespace, survival)
		
		return nb_classifier


def test(classifier):
	with open(input_testfilename,"rb") as csvfile_sentiment:
		spamreader_sentiment = csv.reader(csvfile_sentiment)
		headers=spamreader_sentiment.next()
		featurespace=[]
		index=[]
		for row in spamreader_sentiment:
			fr=[]
			index.append(int(row[0]))
			fr.append(int(row[1]))
			if row[3]=='male':
				fr.append(0)
			else:
				fr.append(1)
			if row[4]!='':
				fr.append(float(row[5]))
			else:
				fr.append(30.0)
			fr.append(int(row[5]))
			fr.append(int(row[6]))
			if row[8]!='':
				fr.append(float(row[8]))
			else:
				fr.append(35.6)
			featurespace.append(fr)
			
		results=classifier.predict(featurespace)
		
		res=zip(index,results)
		return res
			
classifier= train()
pred=test(classifier)

print pred
