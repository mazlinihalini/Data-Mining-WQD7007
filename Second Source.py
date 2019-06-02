# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 09:21:55 2019

@author: User
"""
import requests
import pandas as pd

df = pd.read_excel("KLSECode.xlsx",
                     sheet_name = 0,
                     header = 0,
                     index_col = False,
                     keep_default_na = True)

#Convert Code to string by adding leading zero
df['Code']=df['Code'].apply(lambda x: '{0:0>4}'.format(x))

#Convert Column Code into list
companylist = df["Code"].tolist()

#Generate lists for quarterly report
QCode=[]
Eps=[]
Dps=[]
Nta=[]
Revenue=[]
P=[]
Q=[]
QDate=[]
FDate=[]
Announced=[]
Net=[]

ACode=[]
AEps=[]
Year=[]
ARev=[]
ANet=[]


for symbol in companylist:
    url = 'https://www.klsescreener.com/v2/stocks/view/' + symbol
    page = requests.get(url)
    code = str(symbol)

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    quarter_table=soup.find('table', class_='financial_reports table table-hover')
    quarter_table

    annual_table=soup.find('table', class_='table table-hover')
    annual_table
    
    for row in quarter_table.findAll("tr"):
        cells = row.findAll('td')
        if len(cells)==11: #Only extract table body not heading
            Eps.append(cells[0].find(text=True))
            Dps.append(cells[1].find(text=True))
            Nta.append(cells[2].find(text=True))
            Revenue.append(cells[3].find(text=True))
            P.append(cells[4].find(text=True))
            Q.append(cells[5].find(text=True))
            QDate.append(cells[6].find(text=True))
            FDate.append(cells[7].find(text=True))
            Announced.append(cells[8].find(text=True))
            Net.append(cells[9].find(text=True))
            QCode.append(code)
            

    for row in annual_table.findAll("tr"):
        cells = row.findAll('td')
        if len(cells)==5: #Only extract table body not heading
            Year.append(cells[0].find(text=True))
            ARev.append(cells[1].find(text=True))
            ANet.append(cells[2].find(text=True))
            AEps.append(cells[3].find(text=True))
            ACode.append(code)
            
#import pandas to convert list to data frame
quarter=pd.DataFrame(QCode,columns=['Code'], dtype=str)
quarter['EPS']=Eps
quarter['DPS']=Dps
quarter['NTA']=Nta
quarter['Revenue']=Revenue
quarter['Profit/Loss']=P
quarter['NQuarter']=Q
quarter['Quarter Date']=QDate
quarter['Financial Date']=FDate
quarter['Announced']=Announced
quarter['Net']=Net
quarter

quarter.to_excel('Quarter Report.xlsx')

#import pandas to convert list to data frame
annual=pd.DataFrame(ACode,columns=['Code'], dtype=str)
annual['Financial Year']=Year
annual['Annual Revenue']=ARev
annual['Annual Net']=ANet
annual['Annual EPS']=AEps
annual

annual.to_excel('Annual Report.xlsx')
