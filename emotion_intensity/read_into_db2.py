
import sqlite3
import csv
from itertools import repeat
import pandas as pd

conn = sqlite3.connect('emo_int.db')
print "Opened database successfully";

filename = "/home/rupsa/Downloads/anger-ratings-0to1.train.txt"
filename2="removal_results"

df=pd.read_csv(filename2,sep='\t')



sql_basic_tweet = """INSERT INTO tweetswithoutstopwords (ID,tweet,rating,emotion,removed_stopwords) VALUES ( ?,?,?,?,?)"""


with open( filename ,'rb') as tsvin :
    tsvin = csv.reader(tsvin, delimiter='\t')
    
    for row in tsvin:
        print row ;

        ID = int(row[0])
        tweet = row[1].decode('utf-8')
        emo = row[2]
        rating = float(row[3])
	removed=df.loc[df['id']==ID]['removed_stopwords'].values[0]
        conn.execute( sql_basic_tweet , ( ID , tweet , rating , emo , removed,) );


conn.commit()
print "Records created successfully";
conn.close()


