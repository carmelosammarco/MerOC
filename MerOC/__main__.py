#####################################################################
#Programm for Mercator Ocean by Carmelo Sammarco
#####################################################################
#Import modules 

import xarray as xr
import pandas as pd
import os

import csv342 as csv
from shapely.geometry import Point, mapping
from fiona import collection


from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext


import datetime as dt
import time
import calendar

import motuclient as mt
from motuclient import motu_api
import ftputil
import netCDF4

import sys
import cdo

import pkg_resources

#######################################


def main(args=None):
    
    window = Tk()


    window.title("MerOC-by-CSammarco")
    


    tab_control = ttk.Notebook(window)

    
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)

    
    tab_control.add(tab1, text='netCDF-Download')
    tab_control.add(tab2, text='netCDF-Manipulation')

    #################
    #TAB 1 
    #Functions
    #################

    Voutmc1 = StringVar()

    def Outputmotuclient1():
        outMC1 = filedialog.askdirectory() 
        Voutmc1.set(outMC1)

    def downloadmotu1():
        inputValue = txt1.get("1.0","end")
        #print (inputValue)
        os.system(inputValue)


    #################################################
    #For download mechanisms

    a = []
    listnew=[]
    styyyymmdd=[]
    endyyyymmdd=[]
    lines = []
    x = "--variable"
    z = "--depth-max"
    hhstart = str()
    hhend = str()

    ########################
    #Download daily
    ########################

    def downloaddaily():

        def countX(lst, x):
            count = 0
            for ele in a:
                if (ele==x):
                    count = count+1
            return count


        def extract_from_link(lista):
            for element in lista:
                e = element.split(' ')[1]
                listnew.append(e)


        def extractstart(listast):
            for element in listast:
                e = element.split(' ')
                styyyymmdd.append(e)


        def extractend(listaend):
            for element in listaend:
                e = element.split(' ')
                endyyyymmdd.append(e)


        def load_options(default_values):
            class cmemsval(dict):
                pass
            values=cmemsval()
            for k,v in default_values.items():
                setattr(values, k, v)
            return values

        #################
        #generation days from interval  
        def perdelta(st,ed,delta):
            curr=st
            while curr <= ed:
                yield curr
                curr += delta
        
        
        #################

        inputValue = txt1.get("1.21",'end-1c')
        print (inputValue)
        a = inputValue.split()
        #print(a)
        nV = countX(a, x)
        dV = countX(a, z)
        #print(nV)
        #print(dV)


        if dV == 0 and nV == 1:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
        
            t1 = sd[0:10]
            t2 = ed[0:10]

            #print (t1)
            #print (t2)
            
            date_min = t1 +" 00:00:00"
            date_max = t2 +" 00:00:00"

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            
            hhstart = str(hhmmssentrystart.get())
            hhend = str(hhmmssentryend.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)

            #lines []
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items():

                with open (Voutmc1.get() + "/listdate.txt") as f:
                    
                    while True:

                        line = f.readline()
                        date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line: 
                            break 
             

        elif dV == 1 and nV == 1:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)

            #lines []
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items(): 
                with open (Voutmc1.get() + "/listdate.txt") as f:

                    while True:

                        line = f.readline()

                    #for line in f:
                        #line = line.strip()
                        #lines.append(line[0:10])  

                        date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line:
                            break
                



        elif dV == 0 and nV == 2:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)

            #lines []
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items(): 
                with open (Voutmc1.get() + "/listdate.txt") as f:

                    while True:

                        line = f.readline()

                    #for line in f:
                        #line = line.strip()
                        #lines.append(line[0:10])  

                        date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line:
                            break


        elif dV == 1 and nV == 2:

            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
        
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)

            #lines []
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items(): 
                with open (Voutmc1.get() + "/listdate.txt") as f:

                    while True:

                        line = f.readline()

                    #for line in f:
                        #line = line.strip()
                        #lines.append(line[0:10])  

                        date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line:
                            break


        elif dV == 0 and nV == 3:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
        
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)

            #lines []
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items(): 
                with open (Voutmc1.get() + "/listdate.txt") as f:

                    while True:

                        line = f.readline()

                    #for line in f:
                        #line = line.strip()
                        #lines.append(line[0:10])  

                        date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line:
                            break



        elif dV == 1 and nV == 3:

            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)

            #lines []
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            for key, value in default_values.items(): 
                with open (Voutmc1.get() + "/listdate.txt") as f:

                    while True:

                        line = f.readline()

                    #for line in f:
                        #line = line.strip()
                        #lines.append(line[0:10])  

                        date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                        default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

                        print(outputname)

                        _opts = load_options(default_values)
                        mt.motu_api.execute_request(_opts)

                        if not line:
                            break


    #######################
    #Download MONTHLY!! 
    #######################

    def downloadmotumontly1():

        def countX(lst, x):
            count = 0
            for ele in a:
                if (ele==x):
                    count = count+1
            return count


        def extract_from_link(lista):
            for element in lista:
                e = element.split(' ')[1]
                listnew.append(e)


        def extractstart(listast):
            for element in listast:
                e = element.split(' ')
                styyyymmdd.append(e)


        def extractend(listaend):
            for element in listaend:
                e = element.split(' ')
                endyyyymmdd.append(e)


        def load_options(default_values):
            class cmemsval(dict):
                pass
            values=cmemsval()
            for k,v in default_values.items():
                setattr(values, k, v)
            return values
    

        inputValue = txt1.get("1.21",'end-1c')
        print (inputValue)
        a = inputValue.split()
        #print(a)
        nV = countX(a, x)
        dV = countX(a, z)
        #print(nV)
        #print(dV)


        if dV == 0 and nV == 1:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
        
            t1 = sd[0:10]
            t2 = ed[0:10]

            #print (t1)
            #print (t2)
            
            date_min = t1 +" 00:00:00"
            date_max = t2 +" 00:00:00"

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            hhstar = str(hhmmssentrystart.get())
            hhend = str(hhmmssentryend.get())

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)

            date_bend = dt.datetime(year2,month2-1,d2,0,0)

            date_end = dt.datetime(year2,month2,d2,0,0)

            #print(date_start)
            #print(date_end)
            #print(date_bend)

            for key, value in default_values.items():
            
                while (date_start <= date_bend):
                
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))

                    date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart ,  date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend

                    print (date_end_cmd)
                    print (date_cmd)
                    
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)


            date_cmd2 =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end.strftime("%Y-%m-%d") +" "+ hhend

            #print (date_cmd2)

            date_min = date_cmd2[0]
            date_max = date_cmd2[1]

            outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            print(outputname)

            _opts = load_options(default_values)
            mt.motu_api.execute_request(_opts)


        elif dV == 1 and nV == 1:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstar = str(hhmmssentrystart.get())
            hhend = str(hhmmssentryend.get())

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)

            date_bend = dt.datetime(year2,month2-1,d2,0,0)

            date_end = dt.datetime(year2,month2,d2,0,0)

            #print(date_start)
            #print(date_end)

            for key, value in default_values.items():
            
                while (date_start <= date_bend):
                
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                    #print (date_cmd)
                    
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)


            date_cmd2 =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end.strftime("%Y-%m-%d") +" "+ hhend

            #print (date_cmd2)

            date_min = date_cmd2[0]
            date_max = date_cmd2[1]

            outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            print(outputname)

            _opts = load_options(default_values)
            mt.motu_api.execute_request(_opts)



        elif dV == 0 and nV == 2:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstar = str(hhmmssentrystart.get())
            hhend = str(hhmmssentryend.get())

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)

            date_bend = dt.datetime(year2,month2-1,d2,0,0)

            date_end = dt.datetime(year2,month2,d2,0,0)

            #print(date_start)
            #print(date_end)

            for key, value in default_values.items():
            
                while (date_start <= date_bend):
                
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                    #print (date_cmd)
                    
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)


            date_cmd2 =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end.strftime("%Y-%m-%d") +" "+ hhend

            #print (date_cmd2)

            date_min = date_cmd2[0]
            date_max = date_cmd2[1]

            outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            print(outputname)

            _opts = load_options(default_values)
            mt.motu_api.execute_request(_opts)



        elif dV == 1 and nV == 2:

            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
        
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstar = str(hhmmssentrystart.get())
            hhend = str(hhmmssentryend.get())

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)

            date_bend = dt.datetime(year2,month2-1,d2,0,0)

            date_end = dt.datetime(year2,month2,d2,0,0)

            #print(date_start)
            #print(date_end)

            for key, value in default_values.items():
            
                while (date_start <= date_bend):
                
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                    #print (date_cmd)
                    
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)


            date_cmd2 =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end.strftime("%Y-%m-%d") +" "+ hhend

            #print (date_cmd2)

            date_min = date_cmd2[0]
            date_max = date_cmd2[1]

            outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            print(outputname)

            _opts = load_options(default_values)
            mt.motu_api.execute_request(_opts)


        elif dV == 0 and nV == 3:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
        
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstar = str(hhmmssentrystart.get())
            hhend = str(hhmmssentryend.get())

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)

            date_bend = dt.datetime(year2,month2-1,d2,0,0)

            date_end = dt.datetime(year2,month2,d2,0,0)

            #print(date_start)
            #print(date_end)

            for key, value in default_values.items():
            
                while (date_start <= date_bend):
                
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                    #print (date_cmd)
                    
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)


            date_cmd2 =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end.strftime("%Y-%m-%d") +" "+ hhend

            #print (date_cmd2)

            date_min = date_cmd2[0]
            date_max = date_cmd2[1]

            outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': '', 'depth_max': '','longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            print(outputname)

            _opts = load_options(default_values)
            mt.motu_api.execute_request(_opts)



        elif dV == 1 and nV == 3:

            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            #print(date_start)
            #print(date_end)

            hhstar = str(hhmmssentrystart.get())
            hhend = str(hhmmssentryend.get())

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            #print (default_values)
            date_start = dt.datetime(year1,month1,d1,0,0)

            date_bend = dt.datetime(year2,month2-1,d2,0,0)

            date_end = dt.datetime(year2,month2,d2,0,0)

            #print(date_start)
            #print(date_end)

            for key, value in default_values.items():
            
                while (date_start <= date_bend):
                
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                    #print (date_cmd)
                    
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]
                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}
            
                    print(outputname)
                    
                    _opts = load_options(default_values)
                    mt.motu_api.execute_request(_opts)
                
                    date_start = date_end_cmd + dt.timedelta(days=1)


            date_cmd2 =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end.strftime("%Y-%m-%d") +" "+ hhend

            #print (date_cmd2)

            date_min = date_cmd2[0]
            date_max = date_cmd2[1]

            outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

            default_values = {'date_min': str(date_min),'date_max': str(date_max),'depth_min': depth_min, 'depth_max': depth_max,'longitude_max': lon_max,'longitude_min': lon_min,'latitude_min': lat_min,'latitude_max': lat_max,'describe': None, 'auth_mode': 'cas', 'motu': motu_server,'block_size': 65536, 'log_level': 30, 'out_dir': outputdir,'socket_timeout': None,'sync': None,  'proxy_server': proxy_server,'proxy_user': proxy_user,'proxy_pwd': proxy_pass, 'user': cmems_user, 'pwd': cmems_pass,'variable': [v1,v2,v3],'product_id': dataset_id,'service_id': product_id,'user_agent': None,'out_name': outputname, 'outputWritten': 'netcdf','size' : '','console_mode': ''}

            print(outputname)

            _opts = load_options(default_values)
            mt.motu_api.execute_request(_opts)
    
    #########################################
    # LOGIC TO GENERATE LINK for DOWNLOAD....

    dmi1 = StringVar()
    dma1 = StringVar()
    padd1 = StringVar()
    nrt = StringVar()
    my = StringVar()
    sd = StringVar()
    ed = StringVar()

    def gennrt():


        if len(dmin1.get()) == 0 : 
            
            if len(V11.get()) != 0 and len(V12.get()) == 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), Voutmc1.get(), fname1.get()))
            
            elif len(V11.get()) != 0 and len(V12.get()) != 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(),  ed.get(), V11.get(), V12.get(), Voutmc1.get(), fname1.get()))

            else :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), V12.get(), V13.get(), Voutmc1.get(), fname1.get()))

        
        elif len(dmin1.get()) != 0 :  
            
            if len(V11.get()) != 0 and len(V12.get()) == 0 and len(V13.get()) == 0 :


                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), Voutmc1.get(), fname1.get()))

            elif len(V11.get()) != 0 and len(V12.get()) != 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), V12.get(), Voutmc1.get(), fname1.get()))

            else  :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), V12.get(), V13.get(), Voutmc1.get(), fname1.get()))


    def genmuy():

        if len(dmin1.get()) == 0 : 
            
            if len(V11.get()) != 0 and len(V12.get()) == 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), Voutmc1.get(), fname1.get()))
            
            elif len(V11.get()) != 0 and len(V12.get()) != 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), V12.get(), Voutmc1.get(), fname1.get()))

            else :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), V12.get(), V13.get(), Voutmc1.get(), fname1.get()))

        
        elif len(dmin1.get()) != 0 :  
            
            if len(V11.get()) != 0 and len(V12.get()) == 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), Voutmc1.get(), fname1.get()))

            elif len(V11.get()) != 0 and len(V12.get()) != 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), V12.get(), Voutmc1.get(), fname1.get()))

            else  :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), V12.get(), V13.get(), Voutmc1.get(), fname1.get()))


    ############
    # To Clen the Link generated for download 

    def genclean1():
        txt1.delete(1.0,END)

    #END FUNCTIONS###
    ############################

    Username1 = Label(tab1, text="Username")
    Username1.grid(column=0, row=0)
    User1 = Entry(tab1, width=13)
    User1.grid(column=0, row=1)
    ##
    Password1 = Label(tab1, text="Password")
    Password1.grid(column=1, row=0)
    Pwd1 = Entry(tab1, width=13, show="*")
    Pwd1.grid(column=1, row=1)
    ##
    Product1 = Label(tab1, text="Product")
    Product1.grid(column=0, row=2)
    Pd1 = Entry(tab1, width=13)
    Pd1.grid(column=0, row=3)
    ##
    Dataset1 = Label(tab1, text="Dataset")
    Dataset1.grid(column=1, row=2)
    Ds1 = Entry(tab1, width=13)
    Ds1.grid(column=1, row=3)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=4)
    ##
    longmin1 = Label(tab1, text="Long min")
    longmin1.grid(column=0, row=5)
    lomin1 = Entry(tab1, width=13)
    lomin1.grid(column=0, row=6)
    ##
    longmax1 = Label(tab1, text="Long max")
    longmax1.grid(column=1, row=5)
    lomax1 = Entry(tab1, width=13)
    lomax1.grid(column=1, row=6)
    ##
    latmin1 = Label(tab1, text="Lat min")
    latmin1.grid(column=0, row=7)
    lamin1 = Entry(tab1, width=13)
    lamin1.grid(column=0, row=8)
    ##
    latmax1 = Label(tab1, text="Lat max")
    latmax1.grid(column=1, row=7)
    lamax1 = Entry(tab1, width=13)
    lamax1.grid(column=1, row=8)
    ##
    depthmin1 = Label(tab1, text="Depth min")
    depthmin1.grid(column=0, row=9)
    dmin1 = Entry(tab1, width=13)
    dmin1.grid(column=0, row=10)
    ##
    depthmax1 = Label(tab1, text="Depth max")
    depthmax1.grid(column=1, row=9)
    dmax1 = Entry(tab1, width=13)
    dmax1.grid(column=1, row=10)
    ##
    space1 = Label(tab1, text=" ")
    space1.grid(column=0, row=11)
    ##
    stardate1 = Label(tab1, text="From [YYYY-MM-DD]")
    stardate1.grid(column=0, row=12)
    sd1 = Entry(tab1, width=13)
    sd1.grid(column=0, row=13)
    ##
    hourdate1 = Label(tab1, text="At [HH:MM:SS]")
    hourdate1.grid(column=1, row=12)
    hhstartentry = Entry(tab1, width=13)
    hhstartentry.grid(column=1, row=13)
    ##
    #format_date1 = Label(tab1, text='["yyyy-mm-dd 00:00:00"]')
    #format_date1.grid(column=0, row=11)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=14)
    ##
    enddate1 = Label(tab1, text="To [YYYY-MM-DD]")
    enddate1.grid(column=0, row=15)
    ed1 = Entry(tab1, width=13)
    ed1.grid(column=0, row=16)
    ##
    houredate1 = Label(tab1, text="At [HH:MM:SS]")
    houredate1.grid(column=1, row=15)
    hhendentry = Entry(tab1, width=13)
    hhendentry.grid(column=1, row=16)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=17)
    ##
    Variable1 = Label(tab1, text="Variable-1")
    Variable1.grid(column=0, row=18)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=19)
    ##
    Variable2 = Label(tab1, text="Variable-2")
    Variable2.grid(column=0, row=20)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=21)
    ##
    Variable3 = Label(tab1, text="Variable-3")
    Variable3.grid(column=0, row=22)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=23)

    ##
    V11 = Entry(tab1, width=13)
    V11.grid(column=1, row=18)

    V12 = Entry(tab1, width=13)
    V12.grid(column=1, row=20)

    V13 = Entry(tab1, width=13)
    V13.grid(column=1, row=22)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=23)
    ##
    filename1 = Label(tab1, text="File name")
    filename1.grid(column=0, row=24)
    fname1 = Entry(tab1, width=13)
    fname1.grid(column=1, row=24)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=25)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=26)
    #
    btn1 = Button(tab1, text="Link-NRT", bg="green", command=gennrt)
    btn1.grid(column=1, row=27)
    ##
    btn1 = Button(tab1, text="Link-MY", bg="green", command=genmuy)
    btn1.grid(column=1, row=28)
    ##
    txt1 = scrolledtext.ScrolledText(tab1,width=45,height=10)
    txt1.grid(column=1,row=29)
    ##
    Out1 = Button(tab1, text="Out-DIR", bg="yellow", command=Outputmotuclient1)
    Out1.grid(column=0, row=29)
    ##
    btn1 = Button(tab1, text="Clean-link", bg="white", command=genclean1)
    btn1.grid(column=1, row=30)
    ##
    btn1 = Button(tab1, text="Download as single file", bg="red", command=downloadmotu1)
    btn1.grid(column=0, row=31)
    ##
    btn1 = Button(tab1, text="Download as monthly files", bg="red", command=downloadmotumontly1)
    btn1.grid(column=0, row=32)
    ###
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=33)
    ###

    btn1 = Button(tab1, text="Download as daily files", bg="red", command=downloaddaily)
    btn1.grid(column=0, row=34)

    hhmmssentrystart = Entry(tab1, width=13)
    hhmmssentrystart.grid(column=0, row=35)
    hhmmsstxts = Label(tab1, text="Daily [START]-time (HH:MM:SS)")
    hhmmsstxts.grid(column=1, row=35)
    hhmmssentryend = Entry(tab1, width=13)
    hhmmssentryend.grid(column=0, row=36)
    hhmmsstxte = Label(tab1, text="Daily [END]-time (HH:MM:SS)")
    hhmmsstxte.grid(column=1, row=36)

    ########################################
    #TAB 2
    #FUNCTIONS
    ###########

    def clicked1():
        clicked1.netCDF_file = filedialog.askopenfilename()


    def clicked2():
        clicked2.Home_dir = filedialog.askdirectory()


    def clicked3(): 
        ds = xr.open_dataset(clicked1.netCDF_file, decode_times=False)
        df = ds.to_dataframe()
        df.to_csv(clicked2.Home_dir + "/file.csv")
        data = pd.read_csv(clicked2.Home_dir +"/file.csv")
        data.dropna().to_csv(clicked2.Home_dir + "/file_cleaned.csv", index = False)
        

    def clicked4():
        ds = xr.open_dataset(clicked1.netCDF_file, decode_times=False)
        df = ds.to_dataframe()
        df.to_csv(clicked2.Home_dir + "/file.csv")
        data = pd.read_csv(clicked2.Home_dir +"/file.csv")
        data.dropna().to_csv(clicked2.Home_dir + "/file_cleaned.csv", index = False)

        filecsv = open(clicked2.Home_dir + "/file_cleaned.csv")
        listed=[]
        line = filecsv.readline()
        for u in line.split(','):
            listed.append(u)
        
        if 'lat' in listed:
            schema = { 'geometry': 'Point', 'properties': { Vr.get() : 'float' } }
            with collection(clicked2.Home_dir +"/file.shp", "w", "ESRI Shapefile", schema) as output:
                with open(clicked2.Home_dir + "/file_cleaned.csv", 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        point = Point(float(row['lon']), float(row['lat']))
                        output.write({
                            'properties': {
                                Vr.get(): row[ Vr.get() ]
                            },
                            'geometry': mapping(point)
                        })
                    
        elif 'Lat' in listed:
            schema = { 'geometry': 'Point', 'properties': { Vr.get() : 'float' } }
            with collection(clicked2.Home_dir +"/file.shp", "w", "ESRI Shapefile", schema) as output:
                with open(clicked2.Home_dir + "/file_cleaned.csv", 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        point = Point(float(row['Lon']), float(row['Lat']))
                        output.write({
                            'properties': {
                                Vr.get(): row[ Vr.get() ]
                            },
                            'geometry': mapping(point)
                        })
                    
        elif 'Latitude' in listed:
            schema = { 'geometry': 'Point', 'properties': { Vr.get() : 'float' } }
            with collection(clicked2.Home_dir +"/file.shp", "w", "ESRI Shapefile", schema) as output:
                with open(clicked2.Home_dir + "/file_cleaned.csv", 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        point = Point(float(row['Longitude']), float(row['Latitude']))
                        output.write({
                            'properties': {
                                Vr.get(): row[ Vr.get() ]
                            },
                            'geometry': mapping(point)
                        })
                    
        elif 'latitude' in listed:
            schema = { 'geometry': 'Point', 'properties': { Vr.get() : 'float' } }
            with collection(clicked2.Home_dir +"/file.shp", "w", "ESRI Shapefile", schema) as output:
                with open(clicked2.Home_dir + "/file_cleaned.csv", 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        point = Point(float(row['longitude']), float(row['latitude']))
                        output.write({
                            'properties': {
                                Vr.get(): row[ Vr.get() ]
                            },
                            'geometry': mapping(point)
                        })
                    
        else:
            messagebox.showinfo('Warning', 'Need to be added a new text format. Please contact Carmelo!')
            print("Need to be added a new text format. Please contact Carmelo!")
        
        os.remove(clicked2.Home_dir +"/file.csv")
        os.remove(clicked2.Home_dir +"/file_cleaned.csv")




    def clicked5():
        command = "cdo mergetime  " + clicked2.Home_dir +"/*.nc  " +  clicked2.Home_dir + "/Concatenated.nc"
        print(command)
        os.system(command)


    def clicked6():
        if typedmy.get() == "DAY":
            command = "cdo splitday" +"  " + clicked1.netCDF_file + "  " + clicked2.Home_dir +"/"+ Suffix.get()
            print(command)
            os.system(command)

        elif typedmy.get() == "MONTH":
            command = "cdo splityearmon" +"  " + clicked1.netCDF_file + "  " + clicked2.Home_dir +"/"+ Suffix.get()
            print(command)
            os.system(command)

        elif typedmy.get() == "YEAR":
            command = "cdo splityear" +"  " + clicked1.netCDF_file + "  " + clicked2.Home_dir +"/"+ Suffix.get()
            print(command)
            os.system(command)
        
        else:
            print("Please to insert DAY, MONTH or YEAR option")




    def clicked7():
        command = "cdo  -f grb copy  " + clicked1.netCDF_file  + "   " + clicked2.Home_dir + "/Convert.grb"
        print(command)
        os.system(command)

    #END FUNCTIONS
    ##########################


    space = Label(tab2, text="")
    space.grid(column=1, row=0)
    ###
    btn = Button(tab2, text="Select file", bg="yellow", command=clicked1)
    btn.grid(column=0, row=1)
    ###
    space = Label(tab2, text="")
    space.grid(column=0, row=2)
    ###
    btn = Button(tab2, text="Select folder", bg="yellow", command=clicked2)
    btn.grid(column=0, row=3)
    ###
    space = Label(tab2, text="")
    space.grid(column=0, row=4)
    ###
    ###
    space = Label(tab2, text="")
    space.grid(column=0, row=5)
    ####
    btn = Button(tab2, text="Convert to CSV", bg="red", command=clicked3)
    btn.grid(column=0, row=6)
    Conc = Label(tab2, text="Select file and folder")
    Conc.grid(column=1, row=6)
    ##
    space = Label(tab2, text="")
    space.grid(column=0, row=7)
    ###
    btn = Button(tab2, text="Convert to shapefile", bg="red", command=clicked4)
    btn.grid(column=0, row=8)
    Var = Label(tab2, text="Select file and Variable =")
    Var.grid(column=1, row=8)
    Vr = Entry(tab2, width=8)
    Vr.grid(column=2, row=8)
    ##
    space = Label(tab2, text="")
    space.grid(column=0, row=9)
    ###
    btn = Button(tab2, text="Concatenate netCDF files", bg="red", command=clicked5)
    btn.grid(column=0, row=10)
    Conc = Label(tab2, text="Select folder")
    Conc.grid(column=1, row=10)
    ###
    ##
    space = Label(tab2, text="")
    space.grid(column=0, row=11)
    ###
    btn = Button(tab2, text="Split NetCDF files", bg="red", command=clicked6)
    btn.grid(column=0, row=12)

    Suff1 = Label(tab2, text="Select file and folder")
    typediv = Label(tab2, text="Divide by DAY/MONTH/YEAR --> ")
    Suff2 = Label(tab2, text="Select SUFFIX = ")
    Suff1.grid(column=1, row=12)
    typediv.grid(column=1, row=13)
    Suff2.grid(column=1, row= 14)

    typedmy = Entry(tab2, width=8)
    typedmy.grid(column=2, row=13)

    Suffix = Entry(tab2, width=8) 
    Suffix.grid(column=2, row=14)

    space = Label(tab2, text="")
    space.grid(column=0, row=15)

    btn = Button(tab2, text="Convert to grib", bg="red", command=clicked7)
    btn.grid(column=0, row=16)
    grib = Label(tab2, text="Select file and folder")
    grib.grid(column=1, row=16)

    #################################################################

    tab_control.pack(expand=1, fill='both')
    
    window.mainloop()
