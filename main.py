#SETUP BEFORE RUNNING - Tested on Ubuntu
# STEP 1: WITHIN YOUR HOME FOLDER CREATE A FOLDER CALLED ticker_data 
# STEP 2: RIGHT CLICK ON THE NEWLY CREATED ticker_data AND SELECT properties 
# STEP 3: LOCATED Parent Folder and COPY THE FILE PATHWAY
# STEP 4: NAVIGATE TO LINE 45 WITHIN THE CODE & PASTE THE NEWLY COPIED FILE PATHWAY
# STEP 5: ADD /ticker_data to the end
# This will enable the automation to create new cvs
# NEXT STEPS Integrate SQL Server connection to allow for both local and cloud based backups

import os
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import datetime
from pandas.plotting import register_matplotlib_converters

symbol = 'XYZ'    # ADD TICKER SYMBOL OF CURRENCY NEEDED TO BE SCRAPPEP
end = datetime.datetime.today()
start = datetime.date(end.year - 10, 1, 1)
Volume = ''
#google = pdr.DataReader(symbol, 'yahoo', end=end, start=start)
google = pdr.DataReader(symbol, 'stooq', end=end, start=start) # 5 year max
register_matplotlib_converters()
# fig, axs = plt.subplots()
google_close = pd.DataFrame(google.Close)
fig1 = plt.figure(figsize=(20, 10))

plt.plot(google.tail()['Close'], 'g-o', label="Close")
plt.legend()
plt.grid(True)
plt.xlabel("Date")
plt.ylabel("$ price")
plt.title(symbol + " 5 Day Close Price", color='blue', size=20)
fig2 = plt.figure(figsize=(20, 10))
plt.title(symbol + "   Close Price", color='purple', size=20)
# google['middle_band', 'MA_50'] = google_close.Close.rolling(50).mean()
google[symbol] = google_close.Close.rolling(50).mean()
google['upper band'] = google_close.Close.rolling(200).mean()
plt.plot(google[symbol], 'r--', label="Middle MA")
plt.plot(google['upper band'], 'y--', label="Upper MA")
plt.plot(google['Close'],  label="Close")
plt.legend()
plt.grid(True)
plt.xlabel("Date")
plt.ylabel("$ Price")
plt.title(symbol + " 5 Year Close Price", color='purple', size=20)

path_out = '/home/USER/ticker_data/{0}/'.format(symbol) 
try:
    os.makedirs(path_out)
    print("Directory ", path_out,  " Created ")
except FileExistsError:
    print("Directory ", path_out,  " Already Exists")
google.to_csv(path_out + symbol + "_10_Year.csv")
google.tail().to_csv(path_out + symbol + '_Weekly.CSV')
fig1.savefig(path_out + symbol + '_5_DAY.png')
fig2.savefig(path_out + symbol + '_10_YEAR.png')
