# Google-Maps-Places-Plugin-for-QGIS
A QGIS plugin to retrieve and attribute Google Maps Places. This plugin aims to fill a significant gap in the geospatial open-source software community. It performs the basic functionalities of retrieving and attributing Google Maps Places (such as bars, cafes, parks, hospitals etc.) for a given area. This particular task is very often used in fields such as competition research, choosing the best location to open a store or a brunch, or for urban planning activities.   

# Plugin overview
Given a dataset of Input points, a specified radius and selected types of places to download, the plugin will search and download for Google Maps Places in those areas, with the "Download Google Maps Places" algoirthm.

![image](https://github.com/kowalski93/Google-Maps-Places-Plugin-for-QGIS/assets/39091833/210b5075-448a-4a76-81a0-0573e5fdd3fe)

It is then possible to further attribute those places with their ratings, the number of user reviews and their price range (if applicable), with the "Attribute Places" algorithm.
![image](https://github.com/kowalski93/Google-Maps-Places-Plugin-for-QGIS/assets/39091833/2b2b5475-0a87-449d-a7df-f17d98a4be4a)

# Requirements
The only dependency is the library googlemaps, which can easily be installed through OSGeo4W and pip:
```
pip install googlemaps
```
# Documentation
The detailed documentation of the plugin can be found in the .pdf file of the repository. Make sure to read it carefully. 
