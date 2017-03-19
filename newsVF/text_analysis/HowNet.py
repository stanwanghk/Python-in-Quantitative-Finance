"""Calculate the sentimental value of given newsid."""
import sqlite3
import settings
import text_analysis.sentimental_calculation as sencal
import wordsbase_load as wbl


def get_value_list(newsid_list):
    wordsbase = wbl.get_wordsbase()
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()
    for newsid in newsid_list:
        cur.execute(''' SELECT content FROM News 
                        WHERE news_id = ?''', (newsid,))
        text = cur.fetchone()[0]
        if text is not None or text is not "NO CONTENT":
            value = sencal.get_sentimental_value(text, wordsbase)
            cur.execute(''' INSERT INTO News(sentiment) 
                            VALUES(?)''', (value,))
    conn.commit()
