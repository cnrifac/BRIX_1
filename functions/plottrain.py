# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 13:33:48 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import numpy as np
from scipy.stats.stats import pearsonr
import pylab as pl
#
def plottrain(VV,VH,HV,HH,LIA,HL,BIOMASS,BIOMASSmax,BIOMASSlow,BIOMASShigh,net,err):    
    size=len(VV)
    inp = np.column_stack((VV,VH,HV,HH,LIA,HL))
    tar = (BIOMASS*BIOMASSmax).reshape(size,1) 
    out = (((net.sim(inp))*BIOMASSmax).reshape(size,1))  #
    # Filtering not valid values
    pos=np.argwhere((tar>BIOMASSlow) & (tar<BIOMASShigh) & (out>BIOMASSlow) & (out<BIOMASShigh))
    tar=tar[pos]
    out=out[pos]
    out=out.flatten()
    tar=tar.flatten()
    np.shape(tar)
    # Computing STATS
    R,pval=pearsonr(tar,out)
    RMSE=round(np.sqrt(((out - tar) ** 2).mean()),1)
    # np.save(outdir+outfile,(tar,out))
    # Plotting results
    #pl.subplot(211)
    pl.plot()
    pl.plot(err)
    pl.xlabel('Epoch number')
    pl.ylabel('error (default SSE)')
    pl.grid()
    pl.show()##
    #pl.subplot(212)
    pl.plot()
    pl.plot(tar,out,'*')
    pl.xlabel('target BIOMASS (t/ha)')
    pl.ylabel('ANN estimated BIOMASS (t/ha)')
    pl.grid()
    pl.plot(tar,tar)
    string = "R=%.3f\np-val=%.2f\nRMSE=%.2f t/ha\nN=%.0f" % (R, pval,RMSE,round(len(BIOMASS),0))
    pl.xlim(0, BIOMASShigh)
    pl.ylim(0, BIOMASShigh)
    pl.text(1,BIOMASShigh-125,string)