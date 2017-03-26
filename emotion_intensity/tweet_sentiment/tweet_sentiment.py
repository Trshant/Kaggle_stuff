import nltk
import os
import sqlite3
from nltk.corpus import stopwords
import csv
from textblob import TextBlob
import re
from nltk.corpus import sentiwordnet as swn
import subprocess


def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

conn = sqlite3.connect('emo_int.db')

cur = conn.cursor()

cur.execute("SELECT * FROM tweetswithoutstopwords limit 3" )
 
rows = cur.fetchall()

#Returns positive, negative, objectivity of a token
def getWordScores(token):
	synset=swn.senti_synsets(token)
	if len(list(synset))>0:
		sentiment_set= synset[0]
		return [sentiment_set.pos_score(),sentiment_set.neg_score(),sentiment_set.obj_score()]

#Returns sentiment scores of a token with a tag. Doesn't work well.
def getWordScores(token,tag):
	synset=swn.senti_synsets(token,tag.lower())
	if len(list(synset))>0:
		sentiment_set= synset[0]
		return [sentiment_set.pos_score(),sentiment_set.neg_score(),sentiment_set.obj_score()]

#returns list of (token,tag) for word-wise sentiment
def tag_tokens(tweet):   
	ftemp=open('temp.txt','w')
	ftemp.write(tweet)
	ftemp.close()
	
	output_of_tagger=subprocess.check_output("bash /home/rupsa/Desktop/titanic_k/emotion_intensity/ark-tweet-nlp-0.3.2/runTagger.sh temp.txt", shell=True)
	
	output_tagger=output_of_tagger.split('\t')
	tags=output_tagger[1].split(' ')
	tokens=output_tagger[0].split(' ')
	tok_tag= zip(tokens,tags)
	
	return tok_tag

for row in rows:
	tweet = row[1].decode('utf-8')
	print "\n\n",tweet,' :: Score= ',row[2]
	
	analysis = TextBlob(tweet)
	print "Sentiment of whole tweet: ",analysis.sentiment

		
	
	##stopwords removed
	analysis = TextBlob(row[4].decode('utf-8'))
	print "Sentiment of tweet without stopwords: ",analysis.sentiment

	#remove hastags and tokenize for wordwise sentiment
	tweet_remhash=tweet.replace('#','')
	tok_tag=tag_tokens(tweet_remhash)
	#print tok_tag
	for tok,tag in tok_tag:
		if tag=='N'or tag=='V' or tag=='R' or tag=='A':   #wordnet only knows these
			print tok, getWordScores(tok, tag)    #positive, negative, objectivity

	
	### EMOTIONAL - words with punctuations eg. heck!, f*ck, @^%#@h#!, #hashtag, @mentions
	#to be added - insults from list
	re_emotional=r"([a-zA-Z]*[\&\%\@\?\*\#\!]+[a-zA-Z]*)"
	matches = re.finditer(re_emotional, tweet)
	print "\nEmotional words are:"  
	for match in matches:
		print match.group()
	
	### HASHTAGS
	re_hashtags=r"\#[a-zA-z]+"
	matches = re.finditer(re_hashtags, tweet)
	print "\nHashtags are:"
	for match in matches:
		print match.group()

	#### MENTIONS
	re_mentions=r"\@[a-zA-z]+"
	matches = re.finditer(re_mentions, tweet)
	print "\nMentions are:"
	for match in matches:
		print match.group()

	print "-------------------------------"
