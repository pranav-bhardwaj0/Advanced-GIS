# Advanced-GIS
Repository/Portfolio for 90753: Advanced GIS at Carnegie Mellon University

https://pranav-bhardwaj0.github.io/Bhardwaj-AdvancedGIS-Portfolio/

## About me
I'm a first-year MSPPM - Data Analytics student from Singapore, with an Earth Science and Environmental Studies background from my undergraduate degree. As such, GIS was a big part of my coursework and research. I used open-source data to analyze the multivariate factors that contribute to landslide risk and hazard in distinct geographies around the world, with the hope of understanding how governments can better utilize their resources for disaster management. As someone who has been raised all over the world, I love using maps and statistics to understand earth systems globally, and how climate change will affect our society in the near future.

Outside of my academic interests, mapping is still a large of my hobbies/interests. My favourite show is The Amazing Race, and I love seeing the different countries that the teams visit, and the transportation routes that they take on the race. I'm also a huge basketball fan, so March Madness is another way that I engage with maps. I love seeing how the "bracket" turns out through the geographical relationship between school location and arena location nationally. 

## What I hope to learn
My GIS skills are pretty focused on physical geography using a variety of data sources. One of the things I want to learn better through the course is how to integrate other data skills (Python, SQL, or R) to better tell stories about data through maps. Integrating a variety of different/disparate sources, and resources is one of the things that I want to continue to build upon. This is always a tricky task, and the content of this class will definitely put this to practice. 

## Portfolio

### Assignment #1: Creating a custom map for the Environmental Defense Fund (EDF)
Link to JSON code - https://github.com/pranav-bhardwaj0/Bhardwaj-AdvancedGIS-Portfolio/blob/main/edf-basemap.json

The non-profit organization I selected for this assignment is the Environmental Defense Fund (EDF). This is a United States-based non-profit that advocates for climate change solutions, including market-based solutions and ecosystem restoration. As such, I expect a lot of “green” to be a part of the map design. 

Document with Design choices (summarized below) - https://github.com/pranav-bhardwaj0/Bhardwaj-AdvancedGIS-Portfolio/blob/main/EDF%20Map%20Design.docx

I used the following two pictures to get a wide variety of colours, since the initial logo only gave me a limited number of options. Since I wanted the “purpose” of this map to show all the EDF offices nationally, I thought it would be best to have a variety of colour options to style this map appropriately. Since the blues in these two palettes are quite deep, and intense, I had adjusted one of the blues for a lighter blue that could be used as water on the basemap. This adjustment is shown below and was done using the Adobe Colour tool. 
![Colour Palette #1](https://user-images.githubusercontent.com/101579103/159188489-6275544b-ef40-4bec-9b69-b52fb1dcbc76.PNG)
![Colour Palette #2](https://user-images.githubusercontent.com/101579103/159188492-8083a5e0-3910-4293-9174-b85bceeecaab.PNG)
![Adjustment 1](https://user-images.githubusercontent.com/101579103/159188495-3b84cb43-6a86-415d-bd17-6d7a3cf127bd.PNG)

Using Google’s Map Styling Wizard, I selected the “Retro” theme as my base. I thought that this option gave me the distinct colour choices that I was looking for this base map. As mentioned earlier, a light blue was used for the water, otherwise a darker blue was too dominant and harsh on the eyes. Some of the elements were kept at the default colour because they didn’t have a large impact on the extents that I was looking while developing this map. Initially, I converted all roads to Matisse (#126C99), but after zooming in, seeing all roads in these colour crowded the map and made it very difficult to read. The “Road” geometry was then changed to Porcelain (#E8EEEE). The Nevada gray (#6D6F72) was a great colour to generally use for text fill.I tried to keep the overall land, and parks as a type of green, as indicated by the “Natural” geometry which was given the Caper colour (#DCE8AC). The “Park” geometry was given a more intense Turmeric colour (#BAD252). These two colour truly showed the greens of the EDF organization, and with the blues represented by the highways, and ocean, all the colour profiles are represented quite well. 

National Map
![National](https://user-images.githubusercontent.com/101579103/159188210-55357091-7ee6-4c3e-9f4c-47625963e641.PNG)

Example of the map at a local scale (New York City, New York)
![NYC](https://user-images.githubusercontent.com/101579103/159188447-c5191c31-f04a-4287-ac1d-9fd6debb3168.PNG)

## Assignment 2
<iframe src="https://insights.arcgis.com/#/embed/59fe3e2c1471401a812316f612bbb27d" width="100%" height="1360" frameborder="0"></iframe>
