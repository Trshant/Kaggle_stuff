
import sqlite3

conn = sqlite3.connect('emo_int.db')

cur = conn.cursor()
cur.execute("SELECT * FROM tweets WHERE rating > 0.6 AND rating < 0.7" )
 
rows = cur.fetchall()
 
for row in rows:
    print(row)
