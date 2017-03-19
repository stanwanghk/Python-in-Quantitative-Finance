# coding=utf-8
import sqlite3
import settings
# import time


def store_article_txt(article):
    article_path = settings.get_article_path()
    content_file = open(article_path, 'a')
    content_file.write('\r\n' + '*' * 20)
    content_file.write('\r\n' + article.title + '  ' + article.pubdate + '\r\n')
    # content_file.write(article.source + '\r\n')
    content_file.write(article.newsid + '\r\n')
    content_file.write(article.url + '\r\n')
    content_file.write(article.source + '\r\n')
    if article.content is not None:
        content_file.write(article.content + '\r\n')
    content_file.write('\r\n')
    content_file.close()


def store_article_sqlite(article):
    # print('starting store')
    # print(article.content)
    if article.content is not "None":
        conn = sqlite3.connect(settings.get_sqlite_path(), timeout=5)
        cur = conn.cursor()
        # source table
        cur.execute(''' SELECT id FROM Source WHERE source = ?''', (article.source,))
        source_id = cur.fetchone()
        if source_id is None:
            cur.execute(''' INSERT OR IGNORE INTO Source (source) VALUES(?)''', (article.source,))  

        # News
        cur.execute(''' SELECT id FROM Source WHERE source = ?''', (article.source,))
        source_id = cur.fetchone()[0]
        cur.execute(''' SELECT id FROM News WHERE news_id = ?''', (article.newsid,))
        news_table_id = cur.fetchone()
        if news_table_id is None:
            cur.execute(''' INSERT INTO News (news_id, source_id, pubdate, url, title, content)
                VALUES(?, ?, ?, ?, ?, ?)''', (article.newsid, source_id, article.pubdate, article.url, article.title, article.content,))

        # Company_News
        cur.execute(''' SELECT id FROM News WHERE news_id = ?''', (article.newsid,))
        news_table_id = cur.fetchone()
        cur.execute(''' SELECT company_id FROM Company_News WHERE news_table_id = ?''', (news_table_id[0],))
        related_companies = cur.fetchall()
        related_company = []
        for com in related_companies:
            related_company.append(com[0])

        if (related_company is None) or (article.companyid not in related_company):
            cur.execute(''' INSERT INTO Company_News (news_table_id, company_id)
                    VALUES(?, ?)''', (news_table_id[0], article.companyid,))
        conn.commit()
    print('{} stored over'.format(article.title))
    # time.sleep(5)


def store_error_text(text):
    error_path = settings.get_error_path()
    error_file = open(error_path, 'a')
    error_file.write(text)
    error_file.write('\r\n')
    error_file.close()
