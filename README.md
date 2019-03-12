# MerOC

Python software (at the moment designed to work in a UNIX environment) containing functions for simplifying the netCDF files download and manipulations. The registration to the CMEMS web portal (by Copernicus) is required to be able to use the download services (TAB1:netCDF-Download). The other tools (TAB2:netCDF-Manipulations) can be used without any registration.

![Imgur](https://i.imgur.com/oDEhCIX.png?raw=true)

## Dependencies:

The dependencies  are listed below:

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

Because of the early project development stage, it is possible find bugs, errors and imprecisions. Please to report them if you can.
  

## Installation:

To use this module is suggested python ~=3.6. Following the command to install the software:

```
pip install MerOC
```

## Functionalities:

The program is divided into two tabs. The first tab is exslusively used by the download mechanisms while the second tab contains tools for the manipulation of netCDF files (See figure above). More details following below:

### TAB 1: netCDF-Download

This Tab allows to subset the CMEMS products by bounding box, variables, depths and time coverage and then download it by day, month,depth or just as a single file. The way to download is strictly related to the data time coverage. In fact for a very large time window (ex. years or anyway for more than 2 months of data) it is wiser use the “Download-monthly” method (which generates one file for month) while for few days the simple “Download” and “Download daily” method can be used (the former generates just one output file while the latter a file for each day).


### TAB 2: netCDF-Manipulation 

This tab is able to convert the netCDF files in different formats (CSV, GRID and shape files), concatenate segments of data coming from the same dataset but at different time steps and split the data in function of the time. It is possible split the data by day(DD), months(YYYYMM) and years(YYYY) with the additional option of addiing a suffix to the data generated. More details about the functions included in  this tab are displayed in a separate published python module named [tool4nc](https://pypi.org/project/tool4nc/) which bring in a easy coding form all the manipulation functionalities.






 













