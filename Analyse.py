# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 13:20:21 2019

@author: user
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

df = pd.read_excel("Clean Stock Market Data.xlsx",
                     sheet_name = 0,
                     header = 0,
                     index_col = False,
                     keep_default_na = True)

#Convert Code to string by adding leading zero
df['Code']=df['Code'].apply(lambda x: '{0:0>4}'.format(x))

#Select six company stockout of 795 company
stock = (df[(df.Code == '1818') | (df.Code == '1023') | (df.Code == '5099') | (df.Code == '6012')]).reset_index()

#Add a 'Symbol' Column 
stock['Symbol'] = ''
stock.loc[stock['Code'] == '1023', 'Symbol'] = 'CIMB' 
stock.loc[stock['Code'] == '5099', 'Symbol'] = 'AIRASIA' 
stock.loc[stock['Code'] == '1818', 'Symbol'] = 'BURSA' 
stock.loc[stock['Code'] == '6012', 'Symbol'] = 'MAXIS' 


#############################################################################################
# Individual Company Visualisation
# split the stock dataframe according to each symbol
cimb = stock[stock['Symbol'] == 'CIMB'] 
airasia = stock[stock['Symbol'] == 'AIRASIA'] 
bursa = stock[stock['Symbol'] == 'BURSA'] 
maxis = stock[stock['Symbol'] == 'MAXIS'] 

# Plot the Last Price for each company in different graph and set the labels

############################################################################################
# CIMB Plot
plt.figure(figsize=(10,5))
top = plt.subplot2grid((4,4), (0, 0), rowspan=3, colspan=4)
bottom = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
top.plot(cimb.Date, cimb['Last Price'])
bottom.bar(cimb.Date, cimb['Volume']) 
 
top.axes.get_xaxis().set_visible(False)
top.set_title('CIMB Group Holdings Berhad')
top.set_ylabel('Last Price')
bottom.set_ylabel('Volume')
plt.savefig('CIMB.jpg')

plt.figure(figsize=(10,5))
sns.distplot(cimb['Last Price'].dropna(), bins=50, color='purple')
plt.savefig('CIMB Histogram.jpg')

############################################################################################
# Maybank Plot
plt.figure(figsize=(10,5))
top = plt.subplot2grid((4,4), (0, 0), rowspan=3, colspan=4)
bottom = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
top.plot(airasia.Date, airasia['Last Price'])
bottom.bar(airasia.Date, airasia['Volume']) 
 
top.axes.get_xaxis().set_visible(False)
top.set_title('AirAsia Group Berhad')
top.set_ylabel('Last Price')
bottom.set_ylabel('Volume')
plt.savefig('AIRASIA.jpg')

plt.figure(figsize=(10,5))
sns.distplot(airasia['Last Price'].dropna(), bins=50, color='purple')
plt.savefig('AIRASIA Histogram.jpg')

############################################################################################
# Bursa Plot
plt.figure(figsize=(10,5))
top = plt.subplot2grid((4,4), (0, 0), rowspan=3, colspan=4)
bottom = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
top.plot(bursa.Date, bursa['Last Price'])
bottom.bar(bursa.Date, bursa['Volume']) 
 
top.axes.get_xaxis().set_visible(False)
top.set_title('Bursa Malaysia Berhad')
top.set_ylabel('Last Price')
bottom.set_ylabel('Volume')
plt.savefig('BURSA.jpg')

plt.figure(figsize=(10,5))
sns.distplot(bursa['Last Price'].dropna(), bins=50, color='purple')
plt.savefig('BURSA Histogram.jpg')

############################################################################################
# Maxis Plot
plt.figure(figsize=(10,5))
top = plt.subplot2grid((4,4), (0, 0), rowspan=3, colspan=4)
bottom = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
top.plot(maxis.Date, maxis['Last Price'])
bottom.bar(maxis.Date, maxis['Volume']) 
 
top.axes.get_xaxis().set_visible(False)
top.set_title('Maxis Berhad')
top.set_ylabel('Last Price')
bottom.set_ylabel('Volume')
plt.savefig('MAXIS.jpg')

plt.figure(figsize=(10,5))
sns.distplot(maxis['Last Price'].dropna(), bins=50, color='purple')
plt.savefig('MAXIS Histogram.jpg')

#############################################################################################
# Company Price Comparison
# keep only three column from the Stock datarame and save it in a new dataframe
price = stock[['Date', 'Symbol','Last Price']]

# Pivot the price to Company Symbol
price = price.pivot_table('Last Price', ['Date'], 'Symbol')

# Plot the Last Price in Price dataframe
price.plot(secondary_y = ["CIMB", "MAYBANK", "MAXIS"], grid = True)
plt.savefig('Last Price.jpg')

# Plot the Last Price Return in Price dataframe
price_return = price.apply(lambda x: x / x[0])
price_return.head()
price_return.plot(grid = True).axhline(y = 1, color = "black", lw = 2)
plt.savefig('Last Price Return.jpg')

# Compare the Price Change
price_change=price.pct_change()

price_change.plot(figsize=(10,4))
plt.axhline(0, color='black', lw=1)
plt.ylabel('Daily Percentage Return')
plt.savefig('Compare Price Change.jpg')


# Correlation Plot 
sns.jointplot('AIRASIA', 'CIMB', price, kind='scatter', color='seagreen')
corr = price.corr()
plt.figure(figsize=(8,8))
sns.heatmap(corr.dropna())
plt.savefig('Correlation Plot.jpg')
 
fig = sns.PairGrid(price.dropna()) 
# define top, bottom and diagonal plots
fig.map_upper(plt.scatter, color='purple')
fig.map_lower(sns.kdeplot, cmap='cool_d')
fig.map_diag(sns.distplot, bins=30)
plt.savefig('Extended Correlation Plot.jpg')



