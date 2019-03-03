# MerOC

Python software (in Development) containing functions for simplifing the download, manipulations and visualization of netCDF files. The registration to the CMEMS web portal (by Copernicus) is required to be able to use the download functions. The other fuction doesn’t require any registration to be used. 

## Dependencies:

In the setup.py it is possible have a look to all the dependencies required which are listed below:

[x]  'netCDF4>=1.4.2'
[x]  'ftputil>=3.4'
[x]  'motuclient>=1.8.1'
[x]  'csv342>=1.0.0'
[x]  'pandas>=0.23.4'
[x]  'xarray>=0.11.0' 
[x]  'csv342>=1.0.0'
[x]  'shapely>=1.6.4.post2'
[x]  'fiona>=1.8.4' 
[x]  'cdo>=1.4.0'
[x]  'moviepy>=0.2.3.5'
[x]  'matplotlib>=3.0.2'
[x]  'numpy>=1.15.4'


## Be aware that:

This software is in development so it can be possible find bugs, errors and imprecisions. Please to report them if you can. In the speciphic the major improvment need to be done with:

#### - The plotintime fuction: 

It works just in particular conditions in which "lat" and "lon" are the metadata name attributes for both latitude and longitude and the input file has just one depth record. In the next future i will try to let it works for other latitude/longitude metadata record names. As long term project the aim is to use both data at single depth and with multi-depths. For the latter I would like let the user decide in which  level focus on and also be able to display variation in fuction of depth. It requires the installation of basemap which you can find [here](https://github.com/matplotlib/basemap) 

#### - The downwload by depth function:

In some occasion and with some dataset, the fuction is not able to retrieve the data. Probably related to the metadata depth information stored. 

  
## Installation:

To use this software is suggested the creation of a python environment (python ~=3.6). It becames mandatory if your python version is part of the 2.* family. Following few basic instructions if interesed to install the module in a new ad-hoc environment.

### Procedure for the Anaconda python distribution:

- conda update conda (To update the Anaconda distribution)

- conda create -n {your_env_name} python=3.6 (For the creation of a python environment)

- conda list (List all the environments installed)

- conda activate {your_env_name} (Activate the chosen environment)

- conda activate (to come back to the initial environment)

### Procedure for the standard python distribution:

- pip install pipenv (installation of the package needed)

- create project folder 

- pipenv pipenv --python 3.6 (Install the python environment inside the project folder)


### MerOC installation using:

- pip install MerOC: 

For Anaconda users and the command can be executed from every path locations. 
 
- pipenv install MerOC:

For python standard distribution users. The command needs to be run inside the project folder.


## Functions included:

The program is divided into two tabs. The first tab is exslusively used by the download mechanisms while the second tab contains tools for the manipulation/visualization of netCDF files. More details following below:

### TAB 1: Download mechanisms

They allow to subset the CMEMS products by bounding box, variables, depths and time coverage. They allow to retrieve the data by day, month, depth or just as a single file. The way to download is strictly related to the data time coverage. In fact for a very large time window (ex. years or anyway for more than 2 months of data) it is wiser use the “Download-monthly” method (which generates one file for month) while for few days the simple “Download” and “Download daily” method can be used (the former generates just one output file while the latter a file for each day). In the “Download daily” can be specified the HH:MM:SS for both the starting and ending foreach daily file (This fuction can be used when for example interested to a same time-window)


### TAB 2: Manipulation and visualization of netCDF files

This tab at the moment is able to convert the netCDF files in different formats (CSV, GRD and shape files), concatenate segments of data coming from the same dataset but at different time steps and split in function of the time. It is possible split the data by day(DD), months(YYYYMM) and years(YYYY)with the additional option to add a suffix to the data generated. More details about the functions included with a brief description are displayed in a separate python module named [tool4nc](https://pypi.org/project/tool4nc/).

## Others useful information:

I am working to realise a guide/tutorial so to help you to understand its use in different contexts and needs. 
 













