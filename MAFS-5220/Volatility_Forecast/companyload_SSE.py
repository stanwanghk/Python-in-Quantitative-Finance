# coding--utf-8
import sqlite3

conn = sqlite3.connect('VF_SHE_SSE.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE  IF NOT EXISTS Company (code TEXT,name TEXT, place INTEGER)
''')
# place: 1 means the company listed on SSE; 2 means listed on SHE;
fname = 'SSE.csv'
fh = open(fname, encoding='gb2312')
for line in fh:
    # line = line.decode('gb2312').encode('utf-8')
    pieces = line.split(',')
    cur.execute('SELECT name FROM Company WHERE code = ?', (pieces[0], ))
    row = cur.fetchone()
    if row is None:
        cur.execute(''' INSERT INTO Company (code, name, place )
                        VALUES (?, ?, 1)
                    ''', (pieces[0], pieces[1]))
conn.commit()

print('end')
