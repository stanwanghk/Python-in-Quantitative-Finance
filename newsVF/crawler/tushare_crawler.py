import tushare as ts
import pandas
import datetime
import settings
import sqlite3
import crawler.store_news as sn


def get_company_stock(code='sh600000',
                      date1=datetime.date(2017, 1, 1),  # for backward;
                      date2=datetime.date(2016, 1, 1)):
    """Crawling the stock price and other information by tushare."""
    """Storing the data in a sqlite database."""
    try:
        code_tushare = code[2:]
        # print('changing')
        time_format = settings.get_time_format()
        startdate = date1.strftime(time_format)
        enddate = date2.strftime(time_format)
        data = ts.get_hist_data(code_tushare, enddate, startdate)
        if data is not None:
            data.insert(0, 'code', code)
            conn = sqlite3.connect(settings.get_sqlite_path())
            cur = conn.cursor()
            cur.execute(''' SELECT name FROM sqlite_master WHERE name='Stock'
                 ''')
            exists = cur.fetchone()
            # print(exists)
            if exists is not None:
                cur.execute(''' SELECT code FROM Stock WHERE code = ?''',(code,))
                exists = cur.fetchone()
            # print(exists)
            if exists is None:
                data.to_sql('Stock', conn, if_exists='append')
            conn.commit()
            print('company(code: {}) stock crawling finished'.format(code))
        else:
            print('Not get stock information for {}'.format(code))
            sn.store_error_text('no stock information:  ' + code)
    except Exception as e:
        print(e,code)
        sn.store_error_text('stock loading error:  ' + code)
