# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 20:09:12 2021

@author: Pranav Bhardwaj

PROCESS FOR EXTRACTING MAJORITY LAND COVER BY COUNTY
"""
import pandas as pd

# Full names of states, in a list so that it can run in a for loop. 
states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

# Create an empty dataframe
LandCover = pd.DataFrame()

for i in states: 
    
    # Use the "Select Layer by Attribute" in the Management Toolbox to select just the counties in a specific state
    arcpy.management.SelectLayerByAttribute("USA_Counties", i, "USA_Counties.STATE_NAME =" i, None)

    # Create a new table based on the states
    arcpy.management.CreateTable(r"C:\Users\prana\OneDrive\Documents\ArcGIS\Projects\PythonProject\PythonProject.gdb\"" i, i,)

    # Use the "Zonal Statistics As Table" function in the Spatial Analyst (SA) toolbox
    # Extract the MAJORITY fuel type based on the LANDCOVER RASTER ("LC20_FCCS_200.tif")
    # Use the MAJORITY FUNCTION (as the average function takes too long to process for each state)
    # NOTATION IS AS FOLLOWED (state table name, zone feature (FIPS), raster data, path, "DATA", "MAJORITY", "CURRENT_SLICE", 90 (DEFAULT), "AUTO_DETECT")
    arcpy.sa.ZonalStatisticsAsTable(i, "USA_Counties.FIPS", "LC20_FCCS_200.tif", r"C:\Users\prana\OneDrive\Documents\ArcGIS\Projects\PythonProject\PythonProject.gdb\"" i, "DATA", "MAJORITY", "CURRENT_SLICE", 90, "AUTO_DETECT")
    
    # Append each of the tables to get all states and all counties
    # i is the statename and since we are using this as the newly created table name in each step
    LandCover = pd.LandCover.append(i)
    
# Covert DataFrame into Excel
# Should be 3220 x 2 (two columns are FIPS and Majority Land Cover)
LandCover.to_excel(r"C:\Users\prana\OneDrive\Documents\90819 Intermediate Python\Project\Counties_FuelHazard", sheet_name = 'FuelType')

# This excel is then used alongisde another excel, with the Majority Land Type CODES (0-1281) to get the name of the landcover
# This is then manually converted into a hazard score (out of 10) based on the USDA Forest Service Classification
# https://www.fs.fed.us/rm/pubs/rmrs_gtr153.pdf
# Starting on PAGE 16. 