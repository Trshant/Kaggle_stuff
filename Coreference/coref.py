from stanford_corenlp_pywrapper import CoreNLP
import os
from nltk.parse.stanford import StanfordParser
import StanfordDependencies
import numpy as np
import csv
from nltk.tokenize import sent_tokenize
import nltk
from nltk.parse.stanford import StanfordDependencyParser
from nltk.chunk import conlltags2tree
from nltk.tokenize import sent_tokenize,word_tokenize

os.environ['STANFORDTOOLSDIR']='/media/rupsa/New Volume/nltk_data/'
nltk.data.path.append('/media/rupsa/New Volume/nltk_data/')
os.environ['CLASSPATH']='/media/rupsa/New Volume/nltk_data/stanford-postagger-full-2015-04-20/stanford-postagger.jar:/media/rupsa/New Volume/nltk_data/stanford-ner-2015-04-20/stanford-ner.jar:/media/rupsa/New Volume/nltk_data/stanford-parser-full-2015-04-20/stanford-parser.jar:/media/rupsa/New Volume/nltk_data/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar'
os.environ['STANFORD_MODELS']='/media/rupsa/New Volume/nltk_data/stanford-postagger-full-2015-04-20/models:/media/rupsa/New Volume/nltk_data/stanford-ner-2015-04-20/classifiers'


parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")


dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz") #dependency-tagger
proc = CoreNLP("coref", corenlp_jars=["/media/rupsa/New Volume/nltk_data/stanford-corenlp-full-2015-04-20/*"])

def checkrep(st):
	ls=st.split(' ')
	sl=set(ls)
	if len(list(sl))<len(ls):
		return sl
	return None
	
def remove_non_ascii(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])
	
def chunks(l,n):
	for i in range(0,len(l),n):
		yield l[i:i+n]

def changecondition(replacing_word, to_be_replaced):
	return len(replacing_word)>1 and (',' not in replacing_word) and checkrep(replacing_word)==None and len(to_be_replaced)>1 and (',' not in to_be_replaced) and replacing_word!=to_be_replaced 

def getphrase(start_ind,end_ind,toklist):
	replacing_word=''
	for token in toklist:
		if int(token[0])>start_ind and int(token[0])<=end_ind :
			replacing_word+=token[1]+' '
	
	return replacing_word

def replacephrase(tokenlist,sent_num,indices,wordlist,replacing_word):
	start=-99
	stop=-99
	ind=0
	replacing_word=replacing_word.strip()
	for tk in tokenlist[sent_num]:
		ind+=1
		if int(tk[0])==indices[0]:
			start=ind
		if int(tk[0])==indices[1]:
			stop=ind
	
	print "\nchanging: ",wordlist[sent_num][start:stop][0],replacing_word
	wordlist[sent_num][start:stop]=[replacing_word]
	#print wordlist[sent_num]

	return wordlist
	
def changeref(res,wordlist,tokenlist):	
	for i in res['entities']:
		if len(i['mentions'])>1: #there are replacements to be done
			replacing_word=''
			for j in i['mentions']:
				#print j
				toklist=tokenlist[j['sentence']]
				if 'representative' in j and j['representative']==True: #this word is a representative for others
					replacing_word=getphrase(j['tokspan_in_sentence'][0],j['tokspan_in_sentence'][1],toklist)
				
				original_sentence=' '.join(wordlist[j['sentence']])
				
				to_be_replaced=getphrase(j['tokspan_in_sentence'][0],j['tokspan_in_sentence'][1],toklist)
				
				if replacing_word!='':
					if changecondition(replacing_word, to_be_replaced):
						#print "changed",to_be_replaced
						revisedwordlist=replacephrase(tokenlist,j['sentence'],j['tokspan_in_sentence'],wordlist,replacing_word)
						
						#print 'now',' '.join(wordlist[j['sentence']])
				
				#print "CHANGED: ", t[j['sentence']]
				
				if original_sentence!=' '.join(wordlist[j['sentence']]):
					#print "ret"
					tex=''
					for te in wordlist:
						tex+=' '.join(te)+" "
					tex=tex.strip()
					return str(tex)

def gettokenlist(list_of_sentences):
	tokenlist=[]
	wordlist=[]
	for ts in list_of_sentences:
		parsed_sentence=dep_parser.raw_parse(ts)
		for pr in parsed_sentence:
			conlled=pr.to_conll(10)
		con=conlled.split()
		toklist=(list(chunks(con,10)))
		tokenlist.append(toklist)
		wl=[]
		for tok in toklist:
			wl.append(tok[1])
		wl.append(ts[-1])
		wordlist.append(wl)
	return wordlist,tokenlist

def resolute(initext):
	text_sent=sent_tokenize(initext)
	#print "leng",len(text_sent)
	wordlist,tokenlist=gettokenlist(text_sent)
	
	suml=0
	for te in wordlist:
		suml+=len(te)
		
	res=proc.parse_doc(initext)
	prevtext=initext
	
	for s in range(suml):
		#print s
		#print res
		text_new=changeref(res,wordlist,tokenlist)
		oldlist=wordlist
		if text_new!=None:
			text_new_sent=sent_tokenize(text_new)
			#print "got",text_new,"leng",len(text_new)
			
			wordlist,tokenlist=gettokenlist(text_new_sent)
			for i in range(0,len(wordlist)):
				if list(set(oldlist[i])-set(wordlist[i]))!=[]:
					#print wordlist[i]
					#print oldlist[i]
					#print "changed ",list(set(oldlist[i])-set(wordlist[i])), ": from: ",list(set(wordlist[i])-set(oldlist[i]))
					print "\nNew:: ",text_new
			res=proc.parse_doc(text_new)
			s+=1
			prevtext=text_new
			oldlist=wordlist
		else:
			return prevtext

text="Promontory Financial Group vowed Monday to take the New York Department of Financial Services to court after the department effectively banned the consulting firm from working on regulatory issues with the banks the department supervises. Promontory, founded by former Comptroller of the Currency Eugene Ludwig, helped London-based Standard Chartered whitewash reports on money laundering it submitted to the regulator in 2010 and 2011, the department said in a report issued Monday. The regulator in 2012 fined Standard Chartered $640 million for allowing about $250 billion of transactions for countries under sanction by the government. The department had been investigating whether Promontory had helped the bank conceal or minimize the scale of its wrongdoing, as reported last month in The New York Times and elsewhere."


#text="Brahmin was pious. He had 2 followers."	
text=remove_non_ascii(text)


print "Input:: ",text	
result=resolute(text)
print "\nFinal Result Obtained:: ",result
