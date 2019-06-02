# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:25:47 2019

@author: User
"""

import pandas as pd
import numpy as np
import glob

##########################################################################################
# Data Processing for Stock Market--------------------------------------------------------
# Create list of file paths from a directory
paths = []

for filepath in glob.iglob('D:/Web Crawler/Klse Data/*'):
    paths.append(filepath)

#create list of dataframes using file paths
df_list = []
for file in paths:
   df_list.append(pd.read_excel(file))
   
#Merge a list of dataframe into one dataframe 
stock_data = pd.concat(df_list)

#Check data types
print (stock_data.dtypes)

#Change code into string
stock_data['Code']=stock_data['Code'].apply(lambda x: '{0:0>4}'.format(x))

#Strip Unwanted Character in Column Date
stock_data['Date'] = stock_data['Date'].map(lambda x: x.lstrip('Updated : ').rstrip(' |'))

#Convert String to Date format
stock_data['Date'] = pd.to_datetime(stock_data['Date'], format = '%d %b %Y')

#Convert Certain String Column to Numeric
stock_data['Open Price'] = pd.to_numeric(stock_data['Open Price'],errors='coerce')
stock_data['High Price'] = pd.to_numeric(stock_data['High Price'],errors='coerce')
stock_data['Low Price'] = pd.to_numeric(stock_data['Low Price'],errors='coerce')
stock_data['Last Price'] = pd.to_numeric(stock_data['Last Price'],errors='coerce')
stock_data['Change (%)'] = pd.to_numeric(stock_data['Change (%)'],errors='coerce')
stock_data['Volume'] = pd.to_numeric(stock_data['Volume'],errors='coerce')

#replace missing value with 0
stock_data = stock_data.replace(np.nan, 0, regex=True)

#Delete column 'Time' 
del stock_data['Time']

#Drop duplicate observation in a dataframe
stock_data = stock_data.drop_duplicates(keep = False)

#Add a 'Class' Column 
stock_data['Class'] = 'Constant'
stock_data.loc[stock_data['Change (%)'] > 0, 'Class'] = 'Up' 
stock_data.loc[stock_data['Change (%)'] < 0, 'Class'] = 'Down' 

#Save as excel file
stock_data.to_excel('Clean Stock Market Data.xlsx')

########################################################################################
#Data Processing for Quarter Report------------------------------------------------------
quarter = pd.read_excel("Quarter Report.xlsx",
                     sheet_name = 0,
                     header = 0,
                     index_col = False,
                     keep_default_na = True)

#Convert Code to string by adding leading zero
quarter['Code']=quarter['Code'].apply(lambda x: '{0:0>4}'.format(x))

#Convert String to Date format
quarter['Financial Year'] = pd.to_datetime(quarter['Financial Year'], format = '%d %b %Y')

#Delete column 'No' and 'Financial Date'
del quarter['No']
del quarter['Financial Date']
del quarter['Announced']

#Check data types
print(quarter.dtypes)

#Strip Unwanted Character in Column Revenue and Profit/Loss
quarter['Revenue'] = quarter['Revenue'].str.replace('k','')
quarter['Revenue'] = quarter['Revenue'].str.replace(',','')
quarter['Revenue'] = quarter['Revenue'] + "000"
quarter['Profit/Loss'] = quarter['Profit/Loss'].str.replace('k','')
quarter['Profit/Loss'] = quarter['Profit/Loss'].str.replace(',','')
quarter['Profit/Loss'] = quarter['Profit/Loss'] + "000"

# Change Profit/loss and Revenue to numeric
quarter['Revenue'] = pd.to_numeric(quarter['Revenue'], errors ='coerce')
quarter['Profit/Loss'] = pd.to_numeric(quarter['Profit/Loss'], errors ='coerce')

#Drop duplicate observation in a dataframe
quarter = quarter.drop_duplicates(keep = False)

quarter.to_excel("Quarter Report.xlsx")

########################################################################################
# Data Processing for Annual Report-----------------------------------------------------
annual = pd.read_excel("Annual Report.xlsx",
                     sheet_name = 0,
                     header = 0,
                     index_col = False,
                     keep_default_na = True)

#Convert Code to string by adding leading zero
annual['Code']=annual['Code'].apply(lambda x: '{0:0>4}'.format(x))

#Convert String to Date format
annual['Financial Year'] = pd.to_datetime(annual['Financial Year'], format = '%d %b %Y')

#Delete column 'No' and 'Financial Date'
del annual['No']
del annual['Financial Date']

#Drop duplicate observation in a dataframe
annual = annual.drop_duplicates(keep = False)

annual.to_excel("Annual Report.xlsx")