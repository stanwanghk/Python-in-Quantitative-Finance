"""The script to use crawler."""
import sqlite3
import settings
import time
import crawler.tencent_news_crawler as tnc
import crawler.tushare_crawler as tc


def company_list_load():
    """"Company list load."""
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()

    fname1, fname2 = settings.get_exchange_path()

    fh1 = open(fname1)
    for line in fh1:
        pieces = line.split(',')
        cur.execute('SELECT name FROM Companies WHERE code = ?', ('sz' + pieces[0], ))
        row = cur.fetchone()
        if row is None:
            cur.execute(''' INSERT INTO Companies (code, name)
                            VALUES (?, ?)
                        ''', ('sz' + pieces[0], pieces[1]))
    conn.commit()

    fh2 = open(fname2)
    for line in fh2:
        pieces = line.split(',')
        cur.execute('SELECT name FROM Companies WHERE code = ?', ('sh' + pieces[0], ))
        row = cur.fetchone()
        if row is None:
            cur.execute(''' INSERT INTO Companies (code, name)
                            VALUES (?, ?)
                        ''', ('sh' + pieces[0], pieces[1]))
    conn.commit()
    print('company list loading end')


def reset_sqlite():
    """Set the tables for storing news."""
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()
    cur.executescript('''
        DROP TABLE IF EXISTS Companies;
        DROP TABLE IF EXISTS News;
        DROP TABLE IF EXISTS Source;
        DROP TABLE IF EXISTS Company_News;
        ''')
    cur.executescript('''
                CREATE TABLE  Companies (
                code CHAR(8) PRIMARY KEY UNIQUE,
                name TEXT UNIQUE);

                CREATE TABLE  News (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                news_id TEXT UNIQUE,
                source_id INTEGER,
                pubdate TEXT,
                time_window INTEGER,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                sentiment REAL);

                CREATE TABLE  Source (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                source TEXT NOT NULL UNIQUE NOT NULL);

                CREATE TABLE  Company_News(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                news_table_id INTEGER,
                company_id CHAR(8))
                ''')
    conn.commit()
    print("sqlite reset")


def news_load(companies=['sh600000']):
    """Execute the tencent_news_crawler for company in the Companies list."""
    (start_date, end_date) = settings.get_date()
    number_of_news = {}

    for company in companies:
        number_of_news[company] = tnc.get_company_news(company, start_date, end_date)
        time.sleep(5)

    file = settings.get_number_path()
    if file is not '':
        f = open(file, 'a')
        for company in number_of_news:
            f.write('{}:{}'.format(company, number_of_news[company]))
            f.write('\r\n')
        f.close()
    print('news loading end')


def stock_load(companies=['sh600000']):
    """Execute the tushare_crawler for every company in the Companies list."""
    (start_date, end_date) = settings.get_date()

    for company in companies:
        tc.get_company_stock(company, start_date, end_date)
        time.sleep(5)
    print('stocks loading end')
