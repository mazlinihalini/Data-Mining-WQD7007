# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 08:48:29 2019

@author: User
"""
import pandas as pd 
import numpy as np

df = pd.read_excel("KLSECode.xlsx",
                     sheet_name = 0,
                     header = 0,
                     index_col = False,
                     keep_default_na = True)

#Convert Code to string by adding leading zero
df['Code']=df['Code'].apply(lambda x: '{0:0>4}'.format(x))

companylist = df["Name"].tolist()

Name = []
Code =[]
Open = []
High = []
Lowest = []
Last = []
Change = []
Volume = []
Buy = []
Sell = []
Date = []
Time = []

from lxml import html
import requests

class AppCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

        name = tree.xpath('//h1[@id="slcontent_0_ileft_0_compnametxt"]/text()')[0]
        code = tree.xpath('//li[@class="f14"]/text()')[1]
        openprice = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        highprice = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        lowprice = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        lastprice = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        chg = tree.xpath('//td[@id="slcontent_0_ileft_0_chgpercenttrext"]/text()')[0]
        volume = tree.xpath('//td[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        buy = tree.xpath('//td[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]
        sell = tree.xpath('//td[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]
        date = tree.xpath('//span[@id="slcontent_0_ileft_0_datetxt"]/text()')[0]
        time = tree.xpath('//span[@id="slcontent_0_ileft_0_timetxt"]/text()')[0]
                  
        Name.append(name)
        Code.append(code[3:])
        Open.append(openprice)
        High.append(highprice)
        Lowest.append(lowprice)
        Last.append(lastprice)
        Change.append(chg)
        Volume.append(volume)
        Buy.append(buy)
        Sell.append(sell)
        Date.append(date)
        Time.append(time)

        print(name + code + " " + "information collected")

        return

class App:
    def __init__(self, name, code, openprice, highprice, lowprice, lastprice, chg, volume, buy, sell, date, time, links):
        self.name = name
        self.code = code
        self.openprice = openprice
        self.highprice = highprice
        self.lowprice = lowprice
        self.lastprice = lastprice
        self.chg = chg
        self.volume = volume
        self.buy = buy
        self.sell = sell
        self.date = date
        self.time = time
        self.links = links

    def __str__(self):
        return ("Name: " + self.name.encode('UTF-8') +
        "\r\nCode: " + self.developer.encode('UTF-8') +
        "\r\nOpenPrice: " + self.openprice.encode('UTF-8') + 
        "\r\nHighPrice: " + self.highprice.encode('UTF-8') + 
        "\r\nLowPrice: " + self.lowprice.encode('UTF-8') + 
        "\r\nLastPrice: " + self.lastprice.encode('UTF-8') +
        "\r\nChange: " + self.chg.encode('UTF-8') + 
        "\r\nVolume: " + self.volume.encode('UTF-8') + 
        "\r\nBuyVolume: " + self.buy.encode('UTF-8') + 
        "\r\nSellVolume: " + self.sell.encode('UTF-8') + 
        "\r\nDate: " + self.date.encode('UTF-8') +
        "\r\nTime: "  + self.time.encode('UTF-8') + "\r\n")   
#1
for symbol in companylist: 
    crawler = AppCrawler("https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=" + symbol, 0)
    crawler.crawl()
    
    for app in crawler.apps:
        print(app)

# Store in a dataframe        
stock=pd.DataFrame(Name,columns=['Name'])
stock['Code'] = Code
stock['Open Price'] = Open
stock['High Price'] = High
stock['Low Price'] = Lowest
stock['Last Price']=Last
stock['Change (%)'] = Change
stock['Volume']=Volume
stock['Buy Volume'] = Buy
stock['Sell Volume'] = Sell
stock['Date'] = Date
stock['Time'] = Time

#Check data types for Stock dataframe
print (stock.dtypes)

#Data Preprocessing 
#Strip Unwanted Character in Column Date
stock['Date'] = stock['Date'].map(lambda x: x.lstrip('Updated : ').rstrip(' |'))

#Convert Certain String Column to Numeric
stock['Open Price'] = pd.to_numeric(stock['Open Price'],errors='coerce')
stock['High Price'] = pd.to_numeric(stock['High Price'],errors='coerce')
stock['Low Price'] = pd.to_numeric(stock['Low Price'],errors='coerce')
stock['Last Price'] = pd.to_numeric(stock['Last Price'],errors='coerce')
stock['Change (%)'] = pd.to_numeric(stock['Change (%)'],errors='coerce')
stock['Volume'] = pd.to_numeric(stock['Volume'],errors='coerce')

#replace missing value with 0
stock = stock.replace(np.nan, 0, regex=True)

# Store in a csv file
stock.to_excel('KLSE_300419.xlsx', index = False)