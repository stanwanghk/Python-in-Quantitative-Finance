import pandas as pd
import datetime

home_path = "~/Documents/data/"


def process_data():
    start_date = datetime.datetime(2010, 1, 4)
    end_date = datetime.datetime(2016, 6, 30)

    AP_5F_data = pd.read_csv(home_path+"Asia_Pacific_ex_Japan_5_Factors_Daily.csv",parse_dates=True,skiprows=6,index_col=0)
    AP_MF_data = pd.read_csv(home_path+"Asia_Pacific_ex_Japan_MOM_Factor_Daily.csv",parse_dates=True,skiprows=6,index_col=0)
    daily_price = pd.read_excel(home_path+"daily price.xls",index_col=0)
    exchange = pd.read_excel(home_path+"HKDUSD.xls",index_col=0)
    # combine the factor data
    FF_data = AP_5F_data.join(AP_MF_data)
    risk_free = FF_data.RF
    risk_free = daily_price.join(risk_free).RF
    # covert price in HKD to price in USD
    col_names = daily_price.columns
    for col in col_names:
        daily_price[col] *= exchange.HKDUSD
        daily_price[col] = daily_price[col].pct_change()*100 - risk_free
        daily_price[col] = daily_price[col].round(2)
    # cut the data that is out of the sample period
    FF_data = FF_data[(FF_data.index>=start_date)&(FF_data.index<=end_date)]
    daily_price = daily_price[(daily_price.index>=start_date)&(daily_price.index<=end_date)]
    # save the processed data
    FF_data.to_csv(home_path+"Asia_Pacific_ex_Japan_6_Factors_Daily.csv")
    daily_price.to_csv(home_path+"daily price in USD.csv")
    print("finished")


def process_data2():
    sector = pd.read_excel(home_path+"Hang Seng China 100 Index.xlsx",index_col=0)
    sec_names=["Financial","Information technology","Industrial","Real estate"]
    for name in sec_names:
        sector.ix[sector.Sector==name,name]="1"
        sector.ix[sector.Sector!=name,name]="0"
    sector[sec_names].to_csv(home_path+"sector_HSI100.csv",index=False)

    stocks = pd.read_excel(home_path+"Hang Seng China 100 Index_weekly data.xlsx",index_col=0)
    stocks = stocks.pct_change()[1:]
    stocks.to_csv(home_path+"stocks_HSI100.csv")
    # return sector
