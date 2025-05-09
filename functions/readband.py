# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:25:12 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import os
#os.environ['PROJ_LIB'] = 'C:\\Users\\Emanuele\\anaconda3\\Library\\share\\proj' # to solve path issue
#os.environ['GDAL_DATA'] = 'C:\\Users\\Emanuele\\anaconda3\\Library\\share'      # to solve path issue
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly
import numpy as np 
    ###########################################################################
def readband(infile):
    ds = gdal.Open(infile, GA_ReadOnly)
    #fix the driver
    driver = gdal.GetDriverByName("GTiff")
    #find rows and columns 
    dim1 = ds.RasterXSize
    dim0 = ds.RasterYSize
    #fix projection (same raster in input) 
    proj = ds.GetProjection()
    geoinformation = ds.GetGeoTransform()
    # ds = gdal.Open(infile, GA_ReadOnly)
    # dim1 = ds.RasterXSize
    # dim0 = ds.RasterYSize
    rb = ds.GetRasterBand(1)   
    band = rb.ReadAsArray()  
    
    # dim0=band.shape[0]
    # dim1=band.shape[1]
    band=np.nan_to_num(band) 
    ##############################################
    # band=band[0:dim0:10,0:dim1:10]
    # dim0=band.shape[0]
    # dim1=band.shape[1]
    ##############################################
    band=np.reshape(band,dim0*dim1)
    #To save memory
    # ds=None;
    # rb=None;
    return ds,band,dim0,dim1,proj,geoinformation,driver