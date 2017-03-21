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

print df

for index,r in  df.iterrows():
	text=r[0].replace(' ','-')
	url="http://onlineslangdictionary.com/meaning-definition-of/"+text
	print url
	response=urllib2.urlopen(url)
	soup = BeautifulSoup(response, 'html.parser')
	score= soup.find('span', {'id':'vulgarity-vote-average'}).string
	print r[0],score

