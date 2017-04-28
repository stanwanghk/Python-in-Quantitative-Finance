import pandas as pd
import read_data as rd

def response_fun(data,freq='250L'):
    # data = rd.read_data()
    data.resample()