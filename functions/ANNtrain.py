# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 13:18:37 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import numpy as np
# from scipy.stats.stats import pearsonr
from scipy import stats
import pylab as pl
import neurolab as nl 
#
def ANNtrain(nepochs,nshow,valgoal,nneu,step,indir,trainfile,BIOMASSlow,BIOMASShigh):
    ######################### loading training data ###########################
    HH,HV,VH,VV,LIA,HL,BIOMASS = np.loadtxt (indir+trainfile,unpack = True,usecols = (0,1,2,3,4,5,6),delimiter = ',')
    
    ################ computing minmax (for ANN training) ######################
    size = len(VV) 
    sizetrain=len(VV[0:size:step])
    VVmin=min(VV)
    VHmin=min(VH)
    HVmin=min(HV)
    HHmin=min(HH)
    LIAmax=max(LIA)
    HLmax=max(HL)
    BIOMASSmax=max(BIOMASS)  
    
    ########################## Training ANN ###################################
    # Create network with 5 inputs, nneu neurons in input layer nneu in second and 1 in output layer
    net = nl.net.newff([[min(VV), max(VV)],[min(VH), max(VH)],[min(HV), max(HV)],[min(HH), max(HH)],[min(HL), max(HL)]], [nneu, nneu, 1],) #,[min(LIA), max(LIA)]
    # net.trans = nl.trans.LogSig                                            # changing transfer function to LogSig (default Tansig)
    print("**** ANN architecture defined ...")     
     
    ############# Creating Input/Target data for ANN ##########################
    inp = np.column_stack((HH[0:size:step],HV[0:size:step],VH[0:size:step],VV[0:size:step],
                           HL[0:size:step])) #,LIAnorm LIA[0:size:step],
    tar = (BIOMASS[0:size:step]/BIOMASSmax).reshape(sizetrain,1) 
    #sys.exit() 
    print("**** input/output vectors defined ****")
    # Train process
    err = net.train(inp, tar, epochs=nepochs, show=nshow, goal=valgoal)   
    
    ######################## testing the ANN ##################################
    
    inp = np.column_stack((HH,HV,VH,VV,HL)) #LIA,
    out = (((net.sim(inp))*BIOMASSmax).reshape(size,1))  #  
    tar = BIOMASS.reshape(size,1) 
    # out = (((net.sim(inp))*BIOMASSmax).reshape(size,1))  #
    # Filtering not valid values
    pos=np.argwhere((tar>BIOMASSlow) & (tar<BIOMASShigh) & (out>BIOMASSlow) & (out<BIOMASShigh))
    tar=tar[pos]
    out=out[pos]
    out=out.flatten()
    tar=tar.flatten()
    np.shape(tar)
    # Computing STATS
    # R,pval=pearsonr(tar,out)
    slope, intercept, R, pval, std_err = stats.linregress(tar,out)
    RMSE=round(np.sqrt(((out - tar) ** 2).mean()),1)
    RMSE=round(np.sqrt(((out - tar) ** 2).mean()),1)
    print('r_value :' + str(R))
    print('p_value :' + str(pval))
    print('RMSE :' + str(RMSE))
    
    # Plotting results
    print("**** plotting results ****")
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
    
    return net,err,VVmin,VHmin,HVmin,HHmin,LIAmax,HLmax,BIOMASSmax     


