
import sqlite3
import csv
from itertools import repeat

conn = sqlite3.connect('emo_int.db')
print "Opened database successfully";

filename = "../datasets/emotionintensity/anger-ratings.train.txt"

sql_basic_tweet = """INSERT INTO tweets (ID,tweet,rating,emotion) VALUES ( ?,?,?,?)"""

with open( filename ,'rb') as tsvin :
    tsvin = csv.reader(tsvin, delimiter='\t')
    
    for row in tsvin:
        print row ;


        ID = int(row[0])
        tweet = row[1].decode('utf-8')
        emo = row[2]
        rating = float(row[3])

        conn.execute( sql_basic_tweet , ( ID , tweet , rating , emo , ) );


conn.commit()
print "Records created successfully";
conn.close()


