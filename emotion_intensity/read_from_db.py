
import sqlite3

conn = sqlite3.connect('emo_int.db')

cur = conn.cursor()
cur.execute("SELECT * FROM tweets WHERE rating > 0.7 AND rating < 0.8 limit 5" )
 
rows = cur.fetchall()
 
for row in rows:
    print(row)



print("\n\n")

cur.execute("SELECT * FROM tweets WHERE rating > 0.6 AND rating < 0.7 limit 5" )
 
rows = cur.fetchall()
 
for row in rows:
    print(row)
