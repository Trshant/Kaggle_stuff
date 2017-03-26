import nltk
import os
import sqlite3
from nltk.corpus import stopwords
import csv

def remove_non_ascii(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])

fo = open('removal_results', 'w')
fw = csv.writer(fo,delimiter='\t')

stop = set(stopwords.words('english'))

conn = sqlite3.connect('emo_int.db')

cur = conn.cursor()

cur.execute("SELECT * FROM tweets" )
 
rows = cur.fetchall()

for row in rows:
	print row[0]
	iden = row[0]
	sentence = row[1]
	sentence=remove_non_ascii(sentence)
	after_removal = [i for i in sentence.lower().split() if i not in stop]
	after_removal=" ".join(after_removal)
	towriterow=[row[0]]
	towriterow.append(after_removal)
	fw.writerow(towriterow)
