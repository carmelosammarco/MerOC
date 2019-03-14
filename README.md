# MerOC

Python software containing functions for simplifying the netCDF files download and manipulations. The registration to the CMEMS web portal (by Copernicus) is required to be able to use the download services (TAB1:netCDF-Download). The other tools (TAB2:netCDF-Manipulations) can be used without any registration.

![Imgur](https://i.imgur.com/oDEhCIX.png?raw=true)


## Be aware that:

Because of the early project development stage, it is possible find bugs, errors and imprecisions. Please to report them if you can.
  

## Dependencies:

The dependencies  are listed below:

- [x]  netCDF4>=1.4.2
- [x]  ftputil>=3.4
- [x]  motuclient>=1.8.1
- [x]  pandas>=0.23.4
- [x]  xarray>=0.11.0 
- [x]  csv342>=1.0.0
- [x]  shapely*
- [x]  fiona*
- [x]  cdo>=1.4.0


## Installation:

To use this software is suggested python ~=3.6. Following the command to install the software:

```
pip install MerOC
```
### * For Windows users only:

If you work in a Windows environment you must read this guide which will guide you to the installation of “shapely” and “fiona”. They are essential Python tools for geospatial operations (exporting a netCDF variable as shapefile just to cite one). In this particular scenario I lively suggest you to install the modules using the Python wheels when possible, because they are pre-compiled and then easily digested from the Windows OS. Christoph Gohlke, at the Laboratory for Fluorescence Dynamics at UC Irvine, maintains a large [Python wheels library](https://www.lfd.uci.edu/~gohlke/pythonlibs/). Be aware that for each module you need to choose the one maching your Python version and the pc processor characteristics (32 or 64-bit). If we consider as example "Shapely-1.6.4.post1-cp37-cp37m-win32.whl" the "cp37" indicate the python version which is 3.7.* while "win32" the processor type which is 32-bit. The python version can be indicated also as "py3" or "py2" or "py2.py3". the latter when both the 2.* and 3.* python version can be used. To install a wheel file you just need to run "pip install [wheel_file]"  in the same location where the wheel is located. To succeed with the installation of "shapely" and "fiona" you must execute the following steps, in the same order as they are listed below:

1) Install [Visual studio C++](https://www.microsoft.com/en-us/download/details.aspx?id=48145).
 
2) Download [GDAL](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal), [Click](https://www.lfd.uci.edu/~gohlke/pythonlibs/#click), [cligj](https://www.lfd.uci.edu/~gohlke/pythonlibs/#cligj), [click_plugin](https://www.lfd.uci.edu/~gohlke/pythonlibs/#click), [attrs](https://www.lfd.uci.edu/~gohlke/pythonlibs/#attrs), [munch](https://www.lfd.uci.edu/~gohlke/pythonlibs/#munch), [fiona](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona), [pyproj](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj), [rtree](https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree) and [shapely](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) from the [Python wheels library](https://www.lfd.uci.edu/~gohlke/pythonlibs/), to have all ready for the next steps.

3) Install the GDAL wheel. I suggest you to don't use GDAL module alongside OSGeo4W or other similar distributions because they could go in conflict and then generate errors and malfuctions. Also add the GDAL library path to the Windows PATH environment variable (which will be something like "C:\pyhon_version\Lib\site-packages\osgeo").To know as add the GDAL path variable  you can check [here](https://www.howtogeek.com/118594how-to-edit-your-system-path-for-easy-command-line-access/). Finally we can now test the GDAL module. Before do that please close and then re-open the command prompt and from whatever path location execute  this command; “gdalinfo --help-general”. If GDAL is configured correctly it will display the usage instructions.
 
4) Install the others Python wheels modules downloaded previously (GDAL excluted) following the list order:

- click
- cligj
- click plugin
- attrs
- munch
- fiona
- pyproj
- rtree
- shapely

Now that the all the most nasty dependencies are installed (at least for Windows OS ), you can “pip install MerOC” as I already showed above.


## Functionalities:

The program is divided into two tabs. The first tab is exslusively used by the download mechanisms while the second tab contains tools for the manipulation of netCDF files (See figure above). More details following below:

### TAB 1: netCDF-Download

This Tab allows to subset the CMEMS products by bounding box, variables, depths and time coverage and then download it by day, month,depth or just as a single file. The way to download is strictly related to the data time coverage. In fact for a very large time window (ex. years or anyway for more than 2 months of data) it is wiser use the “Download-monthly” method (which generates one file for month) while for few days the simple “Download” and “Download daily” method can be used (the former generates just one output file while the latter a file for each day).


### TAB 2: netCDF-Manipulation 

This tab is able to convert the netCDF files in different formats (CSV, GRID and shape files), concatenate segments of data coming from the same dataset but at different time steps and split the data in function of the time. It is possible split the data by day(DD), months(YYYYMM) and years(YYYY) with the additional option of addiing a suffix to the data generated. More details about the functions included in  this tab are displayed in a separate published python module named [tool4nc](https://pypi.org/project/tool4nc/) which bring in a easy coding form all the manipulation functionalities.






 













