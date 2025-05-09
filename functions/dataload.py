# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 07:19:22 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import numpy as np
#
def dataload(ROIlistfile):
    data1,data2=np.load(ROIlistfile)
    rois=data1
    measuredBiomasses=data2.astype(float) 
    return rois, measuredBiomasses