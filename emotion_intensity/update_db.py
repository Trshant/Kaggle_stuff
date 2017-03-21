
import sqlite3
import csv
from itertools import repeat

conn = sqlite3.connect('emo_int.db')
cur = conn.cursor()
print "Opened database successfully";


#cur.execute("ALTER TABLE tweets ADD removestop TEXT NULL" )
#conn.commit()


filename = "removal_results"

sql_update_tweet = """ UPDATE tweets SET removestop = ? WHERE ID = ? """

with open( filename ,'rb') as tsvin :
    tsvin = csv.reader(tsvin, delimiter='\t')
    
    for row in tsvin:
        print row ;

        ID = int(row[0])
        tweet = row[1].decode('utf-8')

        conn.execute( sql_update_tweet , ( tweet , ID , ) );

conn.commit()
print "Records updated successfully";
conn.close()


