from nltk.corpus import stopwords
import csv
from textblob import TextBlob
import re
from nltk.corpus import sentiwordnet as swn
import subprocess
import sqlite3
import pandas as pd

conn = sqlite3.connect('emo_int.db')

cur = conn.cursor()
'''
cur.execute("ALTER TABLE tweetswithoutstopwords ADD polarity_whole FLOAT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD subjectivity_whole FLOAT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD polarity_remstop FLOAT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD subjectivity_remstop FLOAT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD num_tok_whole INT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD num_tok_remstop INT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD vulgar_words TEXT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD average_vulgarity INT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD anger_words TEXT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD num_anger_words INT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD negative_words TEXT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD num_negative_words INT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD hashtags TEXT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD num_hashtags INT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD emo_words TEXT NULL" )
cur.execute("ALTER TABLE tweetswithoutstopwords ADD num_emo_words INT NULL" )
	


conn.commit()
'''
sql_update_tweet = """ UPDATE tweetswithoutstopwords SET polarity_whole = ?, subjectivity_whole=?, polarity_remstop=?, subjectivity_remstop=?, num_tok_whole=?, num_tok_remstop=?, vulgar_words=?, average_vulgarity=?, anger_words=?, num_anger_words=?, negative_words=?, num_negative_words=?, hashtags=?, num_hashtags=?, emo_words=?, num_emo_words=?    WHERE ID = ? """

def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

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
	ftemp.write(remove_non_ascii(tweet))
	ftemp.close()
	
	output_of_tagger=subprocess.check_output("bash /home/rupsa/Desktop/Collaborate/Kaggle_stuff/emotion_intensity/ark-tweet-nlp-0.3.2/runTagger.sh temp.txt", shell=True)
	
	output_tagger=output_of_tagger.split('\t')
	tags=output_tagger[1].split(' ')
	tokens=output_tagger[0].split(' ')
	tok_tag= zip(tokens,tags)
	
	return tok_tag
def remove_non_ascii(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])

lex_df=pd.read_csv("./lexicons/lexicons_compiled.csv")
lex_df=lex_df.fillna('')
word_list_lexicon=list(lex_df['word'])

vul_df=pd.read_csv("./lexicons/insults_scored.csv")
vul_df=vul_df.fillna('')



cur.execute("SELECT * FROM tweetswithoutstopwords" )
rows = cur.fetchall()


#Processing each row
for row in rows:
	feature_list=[]
	ID=row[0]

	try:
		tweet = row[1].decode('utf-8')
		tweet_remstop=row[4].decode('utf-8')
	except:
		tweet = row[1]
		tweet_remstop=row[4]

	print "\n\n",tweet,' :: Score= ',row[2]
	
	analysis = TextBlob(tweet)
	'''feature :polarity_whole, feature :subjectivity_whole'''	
	print "Sentiment of whole tweet: ",analysis.sentiment.polarity, analysis.sentiment.subjectivity    
	feature_list.append(analysis.sentiment.polarity)
	feature_list.append(analysis.sentiment.subjectivity)
	
		
	
	##stopwords removed
	analysis = TextBlob(tweet_remstop)
	'''feature :polarity_remstop, feature :subjectivity_remstop'''
	print "Sentiment of tweet without stopwords: ",analysis.sentiment.polarity, analysis.sentiment.subjectivity  
	feature_list.append(analysis.sentiment.polarity)
	feature_list.append(analysis.sentiment.subjectivity)
	
	#remove hastags
	tweet_remhash=tweet.replace('#','')
	tok_tag=tag_tokens(tweet_remhash)
	'''feature :num_tok_whole'''
	print "Num Tokens of Whole",len(tok_tag)                                        
	feature_list.append(len(tok_tag))
	
	tok_tag_text=tag_tokens(row[4].decode('utf-8'))
	'''feature : num_tok_remstop'''
	print "Num Tokens without stopwords ",len(tok_tag_text)                           
	feature_list.append(len(tok_tag_text))	
	
	vul_words=''
	vul_score=0
	for ind,vr in vul_df.iterrows():
		vul_phr=vr[1]
		if " "+vul_phr+" " in tweet_remhash:
			print vul_phr,vr[2]
			if vul_words!='':
				vul_words+='/'
			vul_words+=vul_phr 
			vul_score+=vr[2]
	'''feature : vulgar_words, feature: average_vulgarity'''
	if len(vul_words.split('/'))>0:
		print "Vulgarity :", vul_words, vul_score/len(vul_words.split('/'))
		feature_list.append(vul_words)
		feature_list.append(vul_score/len(vul_words.split('/')))
	else:
		avg_vulgarity=0
		feature_list.append(vul_words)
		feature_list.append(0)
	

	anger_words=''
	negative_words=''
	hashtags=''
	for tok,tag in tok_tag:
		if tok in word_list_lexicon:
			emotion_row=lex_df.loc[lex_df['word']==tok].values[0]
			#print emotion_row
			if emotion_row[1]=='anger':
				if anger_words!='':
					anger_words+='/'
				anger_words+=tok
			if emotion_row[4]=='negative':
				if negative_words!='':
					negative_words+='/'
				negative_words+=tok
	for tok,tag in tok_tag_text:
		if tag=='#':
			ht=tok.replace('#','')
			if len(ht)>0:
				if hashtags!='':
					hashtags+='/'
				hashtags+=ht	

	'''feature : num_anger_words feature : anger_words'''
	print "Anger :", len(anger_words.split('/')),anger_words
	feature_list.append(anger_words)
	feature_list.append(len(anger_words.split('/')))
	
	'''feature : num_negative_words , feature : negative_words'''
	print "Negative :", len(negative_words.split('/')),negative_words
	feature_list.append(negative_words)
	feature_list.append(len(negative_words.split('/')))
	

	'''feature : num_hastags, feature : hashtags'''
	print "Hashtags :", len(hashtags.split('/')),hashtags
	feature_list.append(hashtags)
	feature_list.append(len(hashtags.split('/')))
	

	### EMOTIONAL - words with punctuations eg. heck!, f*ck, @^%#@h#!, #hashtag, @mentions
	emo_words=''
	re_emotional=r"([a-zA-Z]*[\&\%\@\?\*\#\!]+[a-zA-Z]*)"
	matches = re.finditer(re_emotional, tweet)
	print "\nEmotional words are:"  
	em_cnt=0
	for match in matches:
		#print match.group()    
		if len(match.group())>1:                      
			em_cnt+=1
			if emo_words!='':
				emo_words+='/'
			emo_words+=match.group()

	'''feature : num_emo_words, feature: emo_words'''
	print "Emotional count",em_cnt, emo_words
	feature_list.append(emo_words)
	feature_list.append(len(emo_words.split('/')))

	
	conn.execute(sql_update_tweet , (feature_list[0],feature_list[1],feature_list[2],feature_list[3],feature_list[4],feature_list[5],feature_list[6],feature_list[7],feature_list[8],feature_list[9], feature_list[10],feature_list[11],feature_list[12],feature_list[13],feature_list[14],feature_list[15],ID, ) );
	print "-------------------------------"

conn.commit()
