# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 12:22:30 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""

def showpng(outtiff,dim0,dim1):
    import rasterio
    import pylab as pl
    from matplotlib.colors import LinearSegmentedColormap
    #################################
    tifImage = rasterio.open(outtiff)
    dx = tifImage.transform[0]
    dy = tifImage.transform[4]
    ulx = tifImage.transform[2]
    uly = tifImage.transform[5]
    BIOMASS=tifImage.read(1)
    mask=tifImage.read(2)
    # pl.plot()
    fig = pl.figure()    
    # fig = pl.figure(figsize=(10,5))
    # pl.rcParams["figure.figsize"]=30,30
    # pl.rcParams.update({'font.size': 30})
    fig, ax = pl.subplots()    
    # customCmap = LinearSegmentedColormap.from_list('biomass', ['#F5F5DC', 'g', '#004500'])
    cax = ax.imshow(BIOMASS*mask,  extent=(ulx,ulx+dx*dim1, uly,uly-dy*dim0))  # cmap=customCmap,  
    #Set figure Layout:
    ax.set_xlabel('Longitude (m)')
    ax.set_ylabel('Latitude (m)')
    cbar=fig.colorbar(cax)
    cbar.set_label('Biomass (ton/ha)')   
    pl.grid()
    # Saving png preview
    name_var_output=outtiff.split('.tif');               #divide where it is .tiff file
    name_var=name_var_output[0]                                #I only take the filename because with split it keeps the two parts it cuts
    pl.savefig(name_var+'.png')                               #Save the file .png
    pl.show()