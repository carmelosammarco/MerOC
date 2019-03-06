# MerOC

Python software (in Development) containing functions for simplifying the netCDF files download/manipulations . The registration to the CMEMS web portal (by Copernicus) is required to be able to use the download services (TAB1:netCDF-Download in figure below). The other tools (TAB2:netCDF-Manipulations in figure below) can be used without any registration requirements.

![Imgur](https://i.imgur.com/oDEhCIX.png?raw=true)

## Dependencies:

In the setup.py it is possible have a look to all the dependencies required which are listed below:

- [x]  netCDF4>=1.4.2
- [x]  ftputil>=3.4
- [x]  motuclient>=1.8.1
- [x]  pandas>=0.23.4
- [x]  xarray>=0.11.0 
- [x]  csv342>=1.0.0
- [x]  shapely>=1.6.4.post2
- [x]  fiona>=1.8.4
- [x]  cdo>=1.4.0


## Be aware that:

Because of the early project development stage, it can be possible find bugs, errors and imprecisions. Please to report them if you can. In the speciphic the major improvment need to be done with:

#### - Downwload by depths:

In some occasion and with some dataset, the fuction is not able to retrieve the data. Probably related to the different way to store, in each product, the metadata depths information. 

  
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

The program is divided into two tabs. The first tab is exslusively used by the download mechanisms while the second tab contains tools for the manipulation of netCDF files (See figure above). More details following below:

### TAB 1: Download mechanisms

They allow to subset the CMEMS products by bounding box, variables, depths and time coverage and then download it by day, month,depth or just as a single file. The way to download is strictly related to the data time coverage. In fact for a very large time window (ex. years or anyway for more than 2 months of data) it is wiser use the “Download-monthly” method (which generates one file for month) while for few days the simple “Download” and “Download daily” method can be used (the former generates just one output file while the latter a file for each day). In the “Download daily” can be specified the HH:MM:SS for both the starting and ending of each daily file (This function can be used when for example interested recursively to a same time-window)


### TAB 2: Manipulations of netCDF files

This tab at the moment is able to convert the netCDF files in different formats (CSV, GRID and shape files), concatenate segments of data coming from the same dataset but at different time steps and split the data in function of the time. It is possible split the data by day(DD), months(YYYYMM) and years(YYYY) with the additional option of addiing a suffix to the data so generated. More details about the functions included togheter with a brief description are displayed in a separate python module named [tool4nc](https://pypi.org/project/tool4nc/) which bring in a easy coding form all the manipulation functionalities.

## Others useful information:

I am working to realise a guide/tutorial so to help you to understand its use in different contexts and needs. 
 













