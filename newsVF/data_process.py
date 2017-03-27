"""To do some analysis for data."""
import sqlite3
import settings


def get_sample_company():
    """Set the list of chosen companies."""
    fSSE, fSHE = settings.get_sample_data()
    f1 = open(fSSE)
    f2 = open(fSHE)

    sample_path = settings.get_sample_path()
    sample = open(sample_path, 'w')
    number1 = 0
    number2 = 0
    for line in f1:
        raw = line.split(',')
        sample.write('sh' + raw[0] + ',' + raw[1])
        sample.write('\n')
        number1 += 1
    for line in f2:
        raw = line.split(',')
        sample.write('sz' + raw[0] + ',' + raw[1])
        sample.write('\n')
        number2 += 1
    sample.close()
    print('sh:', number1, 'sz:', number2)
    print('end of sampling')


def number_of_news():
    """Calculate the number of useful news for one company."""
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()
    fname = settings.get_number_path()
    f = open(fname, 'w')
    f.write('code,numberOfNews,numberOfNoContent,numberOfNone\n')

    companies = []
    # count the number of news of all companies
    cur.execute(''' SELECT code FROM Companies''')
    raws = cur.fetchall()
    for raw in raws:
        companies.append(raw[0])

    # count the number of news of given sample
    # fsample = settings.get_sample_path()
    # samples = open(fsample)
    # for line in samples:
    #     raw = line.split(',')
    #     companies.append(raw[0])

    total_number = 0
    total_nocontent = 0
    total_none = 0
    for company in companies:
        cur.execute(''' SELECT news_table_id FROM Company_News WHERE company_id = ?''', (company,))
        newsids = cur.fetchall()
        number = 0
        none = 0
        nocontent = 0
        for newsid in newsids:
            # print(newsid)
            cur.execute(''' SELECT content FROM News WHERE id = ?''', (newsid[0],))
            text = cur.fetchone()[0]
            if text == 'None':
                none += 1
            elif text == 'NO CONTENT':
                nocontent += 1
            else:
                number += 1
        f.write(company + ',{},{},{}'.format(number, nocontent, none))
        f.write('\n')
        total_number += number
        total_nocontent += nocontent
        total_none += none
    f.write('total,{},{},{}'.format(total_number, total_nocontent, total_none))
    f.close()
    print('end of counting')
