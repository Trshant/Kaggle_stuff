### PMI  CALCULATION   #####

# N= total documents
# N1= documents containing word1 
# N2= documents containing word2

# N3= number of times word1 and word2 appear in a window

# Prob(word1) = (N1 + 1) / N 
# Prob(word2) = (N2 + 1) / N
# Prob(word1, word2) = (N3 + 1) / N.

# PMI(word1, word2) = Log(Prob(word1, word2) / (Prob(word1) * Prob(word2)))

###########################


'''import nltk
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

cur.execute("SELECT * FROM tweetswithoutstopwords" )
 
rows = cur.fetchall()

for row in rows:'''
