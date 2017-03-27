"""Calculate the sentimental value for given text."""
import jieba
import sqlite3
import settings
import text_analysis.wordsbase_load as wbl


def get_sentimental_value(text, wordsbase):
    k = 20
    m = 10
    n = 10
    modifier_weights = [2.0, 1.8, 1.6, 1.4, 0.8]
    paragraphs = text.split('\n')
    text_value = 0.0
    for paragraph in paragraphs:
        paragraph_value = 0.0
        # alogrithm for sentiment value
        words_list = jieba.lcut(paragraph)
        # print(words_list)
        for index, words in enumerate(words_list):
            value = 0.0
            weight_adjust = False
            if words in wordsbase['positive']:
                # print('positive',words)
                value = 1
                weight_adjust = True
            elif words in wordsbase['negative']:
                # print('negative',words)
                value = -1
                weight_adjust = True
            if weight_adjust:
                # test if there is a privative
                for pword in words_list[max(index - k, 0):index]:
                    if words in wordsbase['privative']:
                        # print('privative',words)
                        value *= -1
                # test if there is a modifiers for forward M words or backward N words
                for mword in words_list[max(index - m, 0):min(index + n + 1, len(words_list) - 1)]:
                    if words in wordsbase['modifiers']['level1']:
                        # print('level1',words)
                        value *= modifier_weights[0]
                        break
                    elif words in wordsbase['modifiers']['level2']:
                        # print('level2',words)
                        value *= modifier_weights[1]
                        break
                    elif words in wordsbase['modifiers']['level3']:
                        # print('level3',words)
                        value *= modifier_weights[2]
                        break
                    elif words in wordsbase['modifiers']['level4']:
                        # print('level4',words)
                        value *= modifier_weights[3]
                        break
                    elif words in wordsbase['modifiers']['level5']:
                        # print('level5',words)
                        value *= modifier_weights[4]
                        break
            paragraph_value += value
        # print(paragraph_value)
        text_value += paragraph_value
    return text_value


# fname = "text_analysis/test.txt"
# f = open(fname).read()
# wordsbase = wbl.get_wordsbase()
# print(get_sentimental_value(f, wordsbase))


def get_value_list(start_table_id=1, end_table_id=100):
    """Return the list of sentimental value of news."""
    # loading the wordsbase to analysis
    wordsbase = wbl.get_wordsbase()
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()
    value = {}
    for id in range(start_table_id, end_table_id + 1):
        cur.execute(''' SELECT content FROM News
                        WHERE id = ?''', (id,))
        raw = cur.fetchone()
        # print(raw)
        # newsid = raw[0]
        text = str(raw[0])
        if text != "None" and text != "NO CONTENT":
            value[id] = round(get_sentimental_value(text, wordsbase),2)
    return value


def store_csv_value(value):
    """Store the value in txt file."""
    fname = settings.get_value_path()
    f = open(fname, 'a')
    for index in value:
        f.write('{},{}\n'.format(index,value[index]))
    f.close()


def store_sqlite_value():
    """Store the value in Data Base."""
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()
    fname = settings.get_value_path()
    f = open(fname)
    for line in f:
        raw = line.split(',')
        cur.execute(''' UPDATE News SET sentiment = ?
                        WHERE id = ?''',(raw[1], raw[0]))
    conn.commit()
    print("stored over")
