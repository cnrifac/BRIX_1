# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 13:18:37 2025


@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import numpy as np
from scipy import stats
# from scipy.stats.stats import pearsonr
import pylab as pl
from sklearn.ensemble import RandomForestRegressor#
#
def RFtrain(n_est,rnd_state,step,indir,trainfile,BIOMASSlow,BIOMASShigh):

    ######################### loading training data ###########################
    HH,HV,VH,VV,LIA,HL,BIOMASS = np.loadtxt (indir+trainfile,unpack = True,usecols = (0,1,2,3,4,5,6),delimiter = ',')
    
    ################ computing minmax (for ANN training) ######################
    size = len(VV) 
    # sizetrain=len(VV[0:size:step])
    
    ########################## Defining RF ###################################
    rf = RandomForestRegressor(n_estimators = n_est, random_state = 0)# Train the model on training data
    print("**** RF architecture defined ****")
         
    ############# Creating Input/Target data for RF ###########################
    inp = np.column_stack((HH[0:size:step],HV[0:size:step],VH[0:size:step],VV[0:size:step],
                           HL[0:size:step])) #,LIAnorm LIA[0:size:step],
    tar = BIOMASS[0:size:step]
    #sys.exit() 
    print("**** input/output vectors defined, start training ****")
    # Train process
    
    rf.fit(inp, tar) # 
    print("**** training completed ****")
    ######################### testing the RF ##################################    
    inp = np.column_stack((HH,HV,VH,VV,HL)) #LIA,
    out = rf.predict(inp)   #  
    tar = BIOMASS
    
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
        
    print('r_value :' + str(R))
    print('p_value :' + str(pval))
    print('RMSE :' + str(RMSE))
    # Plotting results
    print("**** plotting results ****")
    pl.plot()
    pl.plot(tar,out,'*')
    pl.xlabel('target BIOMASS (t/ha)')
    pl.ylabel('ANN estimated BIOMASS (t/ha)')
    pl.grid()
    pl.plot(tar,tar)
    pl.plot(tar,slope*tar+intercept,'r')
    string = "R=%.3f\np-val=%.2f\nRMSE=%.2f t/ha\nN=%.0f" % (R, pval,RMSE,round(len(BIOMASS),0))
    pl.xlim(0, BIOMASShigh)
    pl.ylim(0, BIOMASShigh)
    pl.text(1,BIOMASShigh-125,string)     
    
    return rf     


