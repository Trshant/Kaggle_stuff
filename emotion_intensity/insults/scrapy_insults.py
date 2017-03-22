import codecs
from bs4 import BeautifulSoup
import requests
import nltk
import re
import datetime
import pandas as pd
import unidecode
import urllib2

html_escape_table = {
	
       "&": "&amp;",
       '"': "&quot;",
       "'": "&apos;",
       ">": "&gt;",
       "<": "&lt;",
       }
def html_escape(text):
	return "".join(html_escape_table.get(c,c) for c in text)
	
def inputhandler_csv(inputfilename):
	df=pd.read_csv(inputfilename,header=None,sep='\t')
	return df

df=inputhandler_csv("/home/rupsa/Desktop/titanic_k/emotion_intensity/basic_insults.csv")
df.columns = ['Insult']
df['Vulgarity']=pd.Series("", index=df.index)
for index,r in  df.iterrows():
	try:
		text=r[0].replace(' ','-')
		url="http://onlineslangdictionary.com/meaning-definition-of/"+text.lower()
		print index,url
		response=urllib2.urlopen(url)
		soup = BeautifulSoup(response, 'html.parser')
		score= soup.find('span', {'id':'vulgarity-vote-average'}).string
		score=score.replace('%','')
		print score=='None'
		if score=='None':
				score=0
	except:
		score=0
	df.loc[index]['Vulgarity']=int(score)
	
	
df.to_csv("/home/rupsa/Desktop/titanic_k/emotion_intensity/insults_scored.csv")
