#MerOC software - Download/manipulate netCDF files

##This tools simplify the CMEMS product's downloads/manipulations. Especially usefull is the download mechanisms which allow to subset CMEMS by region, variables, depths and time coverage (format:"yyyy-mm-dd 00:00:00").

###Please to be noted that:

###The download mechanism  is strictly related with the data time coverage. In fact for a very large time window (ex. years or for more than 2 months data) it is wiser use the "Download-monthly" method (it generates one file for month) while for few days the simple "Download" od "Download daily" method need to be used (the former generates just one output file while the latter a file for each day in a specific HH:MM:SS time window).

###The "netCDF-processing" tab is able to convert the netCDF files in different formats (as CSV, GRD and Shape files) and it is able to concatenate segments of data coming from the same dataset but at different time steps. For the conversions, however, there is the limitation about the maximum numbers of records that python can analyse in the same time. Probably slit the netCDF file can be a solution if the problem arises. In fact, It is possible split the data by day(DD), months(YYYYMM) and years(YYYY) with the option to add a suffix to the so generated data. 

