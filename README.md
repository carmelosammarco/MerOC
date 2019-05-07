![Imgur](https://i.imgur.com/iEWAtkS.gif?1)
# MerOC    
 
[![Build Status](https://travis-ci.com/carmelosammarco/MerOC.png)](https://travis-ci.com/carmelosammarco/MerOC) [![Build status](https://ci.appveyor.com/api/projects/status/qqy9y9iu1a473qk4?svg=true)](https://ci.appveyor.com/project/carmelosammarco/meroc) [![PyPi](https://img.shields.io/badge/PyPi-Project-yellow.svg)](https://pypi.org/project/MerOC/) [![Gitter](https://badges.gitter.im/MerOC/community.svg)](https://gitter.im/MerOC/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

I developed this software while working as [AKKA](https://www.akka-technologies.com) consultant engeneer for the [CMEMS's Service Desk (Copernicus Marine Environment Monitoring Service)](http://marine.copernicus.eu). I was and I am inspired by the Mercator-Ocean's community (users, co-workers, web-forum discussions and many more) which gave me ideas and the motivational power to build this tool. It is the first python application of its kind created inside the CMEMS environment and I hope that with time it will became an ufficial CMEMS tool. The main goals that I wanted to adress were solving the most common user problems as the data-download requests and the netCDF file manipulations.

**This project gave me also ideas to develop other tools** as [tool4nc](https://github.com/carmelosammarco/tool4nc), [MerOCenv](https://github.com/carmelosammarco/MerOCenv) and [ads4mo](https://github.com/carmelosammarco/ads4mo). To know more about them just visit the projects web pages which are hyperlinked above.

I created also a **chat-community** powered by "Gitter" where is possible have an exchange of ideas,functionalities,bugs and many more. Just click ![Gitter](https://badges.gitter.im/MerOC/community.svg) to acces the chat room.

Many thanks to visit this page and try this software.

**Carmelo Sammarco**

## Introduction:

Python software containing functions for simplifying the netCDF files download and manipulations. The registration to the [CMEMS web portal](http://marine.copernicus.eu) (by Copernicus) is required to be able to use the download services (TAB1:netCDF-Download). The other tools (TAB2:netCDF-Manipulations) can be used without any registration.

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
- [x]  Shapely>=1.6.4.post1
- [x]  Fiona>=1.8.4
- [x]  cdo>=1.4.0


## Installation for Unix users (Linux distros and Mac-OSX systems):

If interested to have a fully use of the "TAB2:netCDF-Manipulations" please install the [cdo - climate data operator](https://code.mpimet.mpg.de/projects/cdo). In fact it is required to run few functions in the above mentioned tab. To do that you can use the following command:

```
sudo apt-get install cdo
```

Also please consider to install [Anaconda](https://www.anaconda.com) 3.* version (Be aware that to use this software is suggested python ~=3.6). Once the bash file (.sh) is downloaded, you can execute it in the terminal using the following command:

```
bash file_installation_Anaconda_downloaded.sh
```

Furthermore, an update of pip, setuptools and wheels is suggested. You can do it executing the following command:

```
python -m pip install --upgrade pip setuptools wheel
```

After that run the software installation with:

```
pip install MerOC
```

When the installation is concluded, just type in the terminal "MerOC",press the enter key and the application will pop up.


## Installation for Windows users:

As first things please install [cdo - climate data operator](https://code.mpimet.mpg.de/projects/cdo). It is required to run few functions inside the "TAB2:netCDF-Manipulations". From the product web page you can download the version which satisfy your system characteristics. Once de-compressed the folder downloaded just run the .exe file to install cdo in your Windows OS system.

Also please consider to install [Anaconda](https://www.anaconda.com) 3.* version (Be aware that to use this software is suggested python ~=3.6). The file from you downloaded will be a stardard executable (.exe). Before run the installation please be sure to tick the option for add in the Windows PATH environment variable the path of the anaconda package. 

Furthermore, an update of pip, setuptools and wheels is suggested. You can do it executing the following command:

```
python -m pip install --upgrade pip setuptools wheel
```

Before start with the software installation it is mandatory to manually configure and install few python dependencies that are not correctly managed by the stardard 'pip' Windows command installation. The dependencies that I am speaking of are “shapely” and “fiona”. They are essential Python modules for geospatial operations which are contained in this python software (exporting a netCDF variable as shapefile just to cite an example). In this particular scenario, and especially in a Windows OS, be able to install the required modules using the Python wheels can be very handy. In fact they are already pre-compiled and then easily digested from the Windows OS. Christoph Gohlke, at the Laboratory for Fluorescence Dynamics at UC Irvine, maintains a large [Python wheels library](https://www.lfd.uci.edu/~gohlke/pythonlibs/). Be aware that for each module you need to choose the one maching your Python version and the pc processor characteristics (32 or 64-bit). If we consider as example "Shapely-1.6.4.post1-cp37-cp37m-win32.whl" the "cp37" indicate the python version which is 3.7.* while "win32" the processor type which is 32-bit. The python version can be indicated also as "py3" or "py2" or "py2.py3". the latter when both the 2.* and 3.* python version can be used. To install a wheel file you just need to run "pip install [wheel_file]"  in the same location where the wheel is located. To succeed within the installation of "shapely" and "fiona" you must execute the following steps, in the same order as they are listed below:

1. Install [Visual studio C++](https://www.microsoft.com/en-us/download/details.aspx?id=48145).
 
2. Download [gdal](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal), [click](https://www.lfd.uci.edu/~gohlke/pythonlibs/#click), [cligj](https://www.lfd.uci.edu/~gohlke/pythonlibs/#cligj), [click_plugin](https://www.lfd.uci.edu/~gohlke/pythonlibs/#click), [attrs](https://www.lfd.uci.edu/~gohlke/pythonlibs/#attrs), [munch](https://www.lfd.uci.edu/~gohlke/pythonlibs/#munch), [fiona](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona), [pyproj](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj), [rtree](https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtree) and [shapely](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) from the [Python wheels library](https://www.lfd.uci.edu/~gohlke/pythonlibs/). Now you have what you need for the following steps.

3. Install the gdal wheel. I suggest you to don't use gdal module alongside OSGeo4W or other similar distributions because they could go in conflict and then generate errors and malfuctions. Also add the gdal library path to the Windows PATH environment variable (which will be something like "C:\pyhon_version\Lib\site-packages\osgeo").To know in which way add the gdal path variable  you can check [here](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/). Finally we can now test the gdal module. Before do that please to close and then re-open the command prompt and from whatever path location execute this command:

```
gdalinfo --help-general
```
 
If gdal is correctly configured it will display its usage instructions.
 
4. Install the others Python wheels modules, previously downloaded (gdal excluded), and following the list order (from the top to the bottom):

- click
- cligj
- click_plugin
- attrs
- munch
- fiona
- pyproj
- rtree
- shapely

Now that the all the most nasty dependencies are installed (at least for Windows OS), you can execute:

```
pip install MerOC
```

When the installation is concluded, just type in the terminal "MerOC",press the enter key and the application will pop up.

## Functionalities:

The program is divided into two tabs. The first tab is exslusively used by the download mechanisms while the second tab contains tools for the manipulation of netCDF files (See figure above). More details following below:

### TAB 1: netCDF-Download

This Tab allows to subset the CMEMS products by bounding box, variables, depths and time coverage and then download by days, months,depths or just as a single file the data requested. The way to download is strictly related to the data time coverage. In fact for a very large time window (ex. years or anyway for more than 2 months of data) it is wiser use the “Download-monthly” method (which generates one file for month) while for few days the simple “Download” and “Download daily” method can be used (the former generates just one output file while the latter a file for each day).

Below I am going to display a more detailed image of the "TAB 1: netCDF-Download". With different coulours are highlighted  the different "TAB" sections.

![Imgur](https://i.imgur.com/hV6QBiW.png?2)

![Imgur](https://i.imgur.com/Tqdnwmw.png?1)

I can summarise the workflow of the "TAB 1: netCDF-Download" as the following:

**1) Filling the form with all the parameters required**
- **CMEMS Usename**
- **CMEMS Password**
- **Product :** name of the product 
- **Dataset :** name of the dataset 
- **Long min/max :** Longitude min and max
- **Lat  min/max :** Latidude min and max
- **Depth min/max :** Depth min and max (if it is avaiable)
- **Date start/end :** Defined by dates and time  (**From** [date_start] at [hh:mm:ss] **To** [date end] **at** [hh:mm:ss])
- **Variable-1,2,3 :** Max three variables are allowed. If you want use less just leave the cell empty.
- **File name :** It needs to be typed also if just used by the single file download method)
- **Out-Dir :** output directory where we want to save the data

**2) Generation of the motuclient script**

**3) Download the data**

To satisfy both the first and second workflow's points we can proceed in two way listed below:

- **Fill the empty boxes** which are the CMEMS login credentials (highlighted in red) and motuclient parameters (highlighted in blue). Be aware that you can request a maximum of tree variables (if less just leave the others variable fields empty). For the output directory you need to select the folder from the window that pop up once you click on “Out-DIR”. Finally you chan generate the motuclient script using “Link-NRT” or “Link-MY” for a near-real-time or multi-year product respectively. 

- **Copy and paste in the empty text-box (1) the script generated by the web portal** and more specifically under the CMEMS subsetter download service related to the product of interest. However be aware that you should modify manually the login credential, file name and output folder. 
**Be aware that this method is going to work only if your data is downloaded as a single file. For the other cases it is mandatory "Fill" the empy boxes.**
  
**Once the first and second point is satisfied we are ready to download the data.** To do that just a click to the more appropriate methods (based on your needs) is required. As i said previously the download mechanisms will allow you to download data by depths, days, months, months&depths, Yearly or just as single file (In the figure above they are highlighted in yellow). 

### TAB 2: netCDF-Manipulation 

This tab is able to convert the netCDF files in different formats (CSV, GRID and shape files), concatenate segments of data coming from the same dataset but at different time steps and split the data in function of the time. It is possible split the data by day(DD), months(YYYYMM) and years(YYYY) with the additional option of addiing a suffix to the data generated. More details about the functions included in  this tab are displayed in a separate published python module named [tool4nc](https://github.com/carmelosammarco/tool4nc) which bring in a easy coding form all the manipulation functionalities.