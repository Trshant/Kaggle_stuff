import sqlite3

conn = sqlite3.connect('emo_int.db')
print "Opened database successfully";

conn.execute('''CREATE TABLE tweetswithoutstopwords
       (ID INT PRIMARY KEY     NOT NULL,
       tweet           TEXT    NOT NULL,
       rating            INT     NOT NULL,
       emotion        CHAR(50),
       removed_stopwords       CHAR(50) );''')
print "Table created successfully";

conn.close()
