# coding--utf-8
import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings


def company_list_load():
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()

    cur.execute('''
                CREATE TABLE  IF NOT EXISTS Company (code TEXT,name TEXT, place INTEGER)
            ''')
    fname = 'SHE.csv'
    fh = open(fname)
    for line in fh:
        pieces = line.split(',')
        cur.execute('SELECT name FROM Company WHERE code = ?', (pieces[0], ))
        row = cur.fetchone()
        if row is None:
            cur.execute(''' INSERT INTO Company (code, name, place )
                            VALUES (?, ?, 2)
                        ''', (pieces[0], pieces[1]))
    conn.commit()

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
    print('company list loading end')
