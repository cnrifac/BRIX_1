# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 11:35:32 2025


@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
from osgeo import gdal
#
def savetiff(outtiff, dim1, dim0, BIOMASS, mask, driver, proj, geoinformation):

    rasterOut = driver.Create(outtiff, dim1, dim0, 2, gdal.GDT_Float32)
    rasterOut.SetProjection(proj)
    rasterOut.SetGeoTransform(geoinformation)
    rasterOut.GetRasterBand(1).WriteArray(BIOMASS)   
    rasterOut.GetRasterBand(2).WriteArray(mask)    
    rasterOut = None;    