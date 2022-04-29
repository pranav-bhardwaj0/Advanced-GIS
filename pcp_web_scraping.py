#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 19:44:01 2021

@author: sebastiandodt
"""

## Importing libraries

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np


# =============================================================================
# With major alterations, code inspired by: 
# https://towardsdatascience.com/how-to-use-selenium-to-web-scrape-with-example-80f9b23a843a
# =============================================================================


## Locating driver
driver = webdriver.Chrome('/Applications/chromedriver')


## Locating website (will open in Chrome)
driver.get('https://www.ncdc.noaa.gov/cag/county/mapping/110/pcp/190001/12/value')



## Identifying 'region' class & putting all counties into one dataframe
regions = driver.find_elements_by_xpath('//td[@class="region"]')
county_names = []
for p in range(len(regions)):
    county_names.append(regions[p].text)

'''Commented out parts were used for testing.'''
#for p in range(0,2):
#    county_names.append(regions[p].text)


## County names are moved into one dataframe and a column name is assigned.
df_county_names = pd.DataFrame(county_names)
df_county_names.columns = ['County']




## Identifying 'value' class
avg_value = driver.find_elements_by_xpath('//td[@class="value"]')
avg_pcp = []

## All values in table are classified as 'value'. Only the 4th value in every row is needed.
for p in range(3,len(regions)*4,4):
    avg_pcp.append(avg_value[p].text)

'''Commented out parts were used for testing.'''
#for p in range(3,8,4):  ######## second arg county# * 4
#    avg_pcp.append(avg_value[p].text)


## Avg pcp values are moved into one dataframe and a column name is assigned.
df_avg_pcp = pd.DataFrame(avg_pcp)
df_avg_pcp.columns = ['Avg Precipitation (1901 - 2000)']



## The following for loop loops through every year and pulls out only the pcp value for each county.
## First, for loop through the years is inserted into the URL.

df_values_ann = pd.DataFrame()
for i in range(1986, 2021, 1):
    i = str(i)
    driver.get('https://www.ncdc.noaa.gov/cag/county/mapping/110/pcp/' + i + '01/12/value')
    print(i)

## All values in table are classified as 'value'. Only every the first value in each row is needed.
    values = driver.find_elements_by_xpath('//td[@class="value"]')
    table_values = []
    for p in range(0, len(regions)*4, 4):
        table_values.append(values[p].text)
    

    '''Commented out parts were used for testing.'''
    #for p in range(0,8,4): ######## second arg is county# multiplied by 4
    #    table_values.append(values[p].text)


## Turning lists into numpy array.
    array_values = np.array(table_values)

## Appending the empty dataframe created before the for loop with the values from for loop.
## Assigning a name to each new column using the corresponding year.
    df_values_ann['Value ' + i] = array_values.tolist()



## Concatinating all three dataframes (county name, pcp values each year, &  avg pcp for the century)
## into one large dataframe
df_years = pd.concat([df_county_names, df_values_ann, df_avg_pcp], axis = 1)
print(df_years)


## Exporting that large dataframe into a CSV file, excluding the index.
df_years.to_csv('pcp_values(1986-2020).csv', encoding='utf-8', index=False)