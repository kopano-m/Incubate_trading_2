import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import h5py

def load_financial_data(start_date, end_date, output_file):
    try:
        df = pd.read_pickle(output_file)
        print('File data found...reading EUR/USD data')
    except FileNotFoundError:
        print('File not found...downloading the EUR/USD data')
        symbol = 'EURUSD=X'
        df = data.DataReader(symbol, 'yahoo', start_date, end_date)
        df.to_pickle(output_file)
    return df

EURUSD_data = load_financial_data(start_date='2003-01-01',
                        end_date='2020-01-01',
                        output_file='EURUSD_data.pkl')

# store the data frame EURUSD into the file EURUSD_data.h5
EURUSD_data.to_hdf('EURUSD_data.h5', 'EURUSD_data', mode='w', format='table', data_columns=True)

# load this file from the EURUSD.h5 and create a data frame EURUSD_data_from_h5_file
EURUSD_data_from_h5_file = h5py.File('EURUSD_data.h5')

print(EURUSD_data_from_h5_file['EURUSD_data']['table'])
print(EURUSD_data_from_h5_file['EURUSD_data']['table'][:])
for attributes in EURUSD_data_from_h5_file['EURUSD_data']['table'].attrs.items():
    print(attributes)
