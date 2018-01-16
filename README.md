# Exploration of OpenStreetMap data for Philadelphia, Pennsylvania.
**Kasey Cox, May 2017**

***

View project report here: https://kacox.github.io/philadelphia_osm/

## Overview

This project aims to take [OpenStreetMap](https://www.openstreetmap.org) data
for Philadelphia, Pennsylvania and do the following:

+ Audit data's structure and constituents with Python
+ Clean, Export, then Import data to a local instance of MongoDB as a JSON
file using Python
+ Query (investigate) the data using MongoDB

The OSM file used in this project was obtained from
[MapZen](https://mapzen.com/data/metro-extracts/metro/philadelphia_pennsylvania/101718083/Philadelphia/)

**I neither included the original OSM file nor the resulting JSON file in **
**this repository due to their large sizes (690.6 MB and 622.2 MB **
**respectively)**

This map is of Philadelphia and the surrounding "Philadelphia suburbs". This
means that there are nodes in towns and cities other than Philadelphia in the
data set.

I chose this area not only for its size, but also because I grew up in
this area.

## Files
**index.html** - Project report of processes and findings (HTML)  
**audit.py** -  Python code used to audit data  
**audit2.py** - Additional Python code used to audit data  
**clean.py** - Python code to clean OSM XML data, load into a Python
dictionary, and write as a JSON file.  
**query.py** - Python code to query a local instance of MongoDB that contains
the cleaned OSM XML data.  
**references.txt** - Outside references used in making this project.  
**Project3.ipynb** - iPython notebook used to create `kcox_project3.html`  
**clean_small_one.py** - Code to clean a _sample_ of the OSM XML data, load
into a Python dictionary, and write as a JSON file. This code is for testing
purposes, not for the final product.
