#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 23:45:37 2021

@author: Pranav Bhardwaj, Philippe Schicker, Sebastian Dodt
"""


## Importing all necessary libaries

import pandas as pd
import numpy as np
import requests
import urllib


## Loading data

land = pd.read_csv("County_FuelHazard.csv")
his_fires = pd.read_csv("County_Wildfires.csv")
rain = pd.read_csv("pcp_values(1900-2020).csv")
temp = pd.read_csv("temp_values(1900-2020).csv")


# Data Cleaning

### LAND
print(land.columns)  # We see that some empty columns are created
for i in ["4", "5", "6", "7", "8"]:
    land.drop("Unnamed: " + i, axis = 1, inplace = True) # removing those columns
land.isna().sum()   # returns 78 NaNs for counties in Puerto Rico. Can be removed.
land.dropna(inplace = True) # drop rows with NAs


### HISTORICAL FIRES
his_fires.isna().sum() # every county that did not have a forest fire has a NaN instead of a 0
his_fires.fillna(0, inplace=True) # fill the cells where no forest fires are reported with the value 0



### PRECIPITATION
rain.isna().sum().sum() # no NaNs
#### splitting the data into bins -- one for each decade
rain_bin = pd.concat([rain["County"],   
                      rain["Avg Precipitation (1901 - 2000)"]], axis = 1)
for i in list(range(1900, 2020, 10)):
    years = []
    for j in range(0,10,1):
        years.append("Value " + str(i+j))
    column_title = "Prec_" + str(i) + "_" + str(i+9) # creates the column title
    rain_bin[column_title] = rain[years].mean(axis = 1)
rain = rain_bin


### TEMPERATURE
temp.isna().sum().sum() # no NaNs
#### splitting the data into bins -- one for each decade
temp_bin = pd.concat([temp["County"], 
                      temp["Avg Temp (1901 - 2000)"]], axis = 1)
for i in list(range(1900, 2020, 10)):
    years = []
    for j in range(0,10,1):
        years.append("Value " + str(i+j))
    column_title = "Temp_" + str(i) + "_" + str(i + 9) # creates the column title
    temp_bin[column_title] = temp[years].mean(axis = 1)
temp = temp_bin


## Checks before merging

print("Number of rows of the Land cover data:       ", len(land))
print("Number of rows of the Forest Fire data:      ", len(his_fires))
print("Number of rows of the Rain data:             ", len(rain))
print("Number of rows of the Temperature cover data:", len(temp)) 

### we notice that the datasets are of very different lengths. 
### This is due to some datasets including Puerto Rico, D.C. and Alaska while others don't

### We need to merge the data based on a mutual value.
### Because county names differ in their spelling and are not unique, we instead use FIPS codes.
### To get the FIPS codes for the non-labelled, we call the census API.


## API

### Calling the API
headers = {"Content-Type": "application/json"}
url = "https://api.census.gov/data/2010/dec/sf1?get=NAME&for=county:*&key=4b3204291c47ca181335316af3f7370993cdb5ba"
returned_data = urllib.request.urlopen(url) # This code for the API call was recommend by the Census
FIPS_list = returned_data.read()
print ('Retrieved',len(FIPS_list),'characters')

### Extracting the data from a large string
FIPS_list = str(FIPS_list)
FIPS_list = FIPS_list.split(",\\n")
FIPS_list = FIPS_list[1:]
FIPS = []
county = []
state = []

### There are various spaces and unnecessary symbols in the data return by the API
### The following code removes these.
for i in range(0,len(FIPS_list)):
    FIPS_list[i] = FIPS_list[i].split(",")
    FIPS_list[i][0] = FIPS_list[i][0][2:]
    county.append(FIPS_list[i][0])
    FIPS_list[i][1] = FIPS_list[i][1][1:-1]
    state.append(FIPS_list[i][1])
    FIPS.append( FIPS_list[i][2][1:-1] + FIPS_list[i][3][1:-2] )
    if i == 3220:
        FIPS[i] = FIPS[i][:-2]

### The final dataset contains the FIPS, County name, and State name per county.
FIPS_final = pd.DataFrame([FIPS, county, state])
FIPS_final = FIPS_final.transpose()
FIPS_final.columns = ["FIPS", "County", "State"]
### We can use this information to merge the temperature and precipitation data that doesn't have FIPS codes

## Merging data

### Merging RAIN, TEMP and FIPS

### Loading datasets that show parts of the FIPS code per state or county respectively.
state_fips = pd.read_csv("state_fips_prefix.csv") 
state_fips2 = pd.read_csv("state_fips_suffix.csv")
for i in range(0, len(state_fips)):
    state_fips[" stusps"][i] = state_fips[" stusps"][i][1:] # removing unnecessary spaces


#### These for loops associates the right FIPS code with each county in our rain and temperature datasets
state = []
prefix = []
for i in range(0,len(rain)):
    state.append(rain["County"][i][-2:])
    prefix.append(state_fips[" st"][ state_fips[" stusps"] == state[i]])
fips = []
prefix = np.array(prefix)
for i in range(0,len(rain)):
    fips.append( str(prefix[i])[1:-1] + state_fips2["Location ID"][i][-3:])
    fips[i] = int(fips[i])
rain["FIPS"] = fips
temp["FIPS"] = fips



### Merging HIS_FIRES and RAIN, TEMP

df = pd.merge(his_fires, land, how = 'inner', on = 'FIPS') # We are using inner join to remove counties that lack data.
df = pd.merge(df, rain, how = 'inner', on = 'FIPS')
df = pd.merge(df, temp, how = 'inner', on = 'FIPS')

### Deleting duplicate and other unnecessary rows
df.drop("OBJECTID", axis = 1, inplace = True)
df.drop("FID_1", axis = 1, inplace = True)
df.drop("County_y", axis = 1, inplace = True)
df.drop("County_x", axis = 1, inplace = True)

### Exporting the dataframe as our final data to be used by the ML algorithm.
try:
    df.to_csv("df.csv")
    print("\n\nData successfully merged and exported as 'df.csv'. \nProceed with 'ML.py'.")
except:
    print("\n\nData not merged/exported successfully.")



    





