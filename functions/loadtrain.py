# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 13:01:32 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import numpy as np
#
def loadtrain(indir,trainfile,step):    
    HH,HV,VH,VV,LIA,HL,BIOMASS = np.loadtxt (indir+trainfile,
                unpack = True,
                usecols = (0,1,2,3,4,5,6),
                delimiter = ',')
    print("**** data loaded ****")
    # pos=np.argwhere((BIOMASS>BIOMASSlow) & (BIOMASS<BIOMASShigh) & (VV<0) & (VH<0) 
    #                 & (HV<0) & (HH<0))
############### resampling data (for ANN training) ###########################
    size = len(VV) 
    VVmin=min(VV)
    VHmin=min(VH)
    HVmin=min(HV)
    HHmin=min(HH)
    LIAmax=max(LIA)
    HLmax=max(HL)
    BIOMASSmax=max(BIOMASS)  
    
    VVnorm=VV/VVmin
    VHnorm=VH/VHmin
    HVnorm=HV/HVmin
    HHnorm=HH/HHmin
    LIAnorm=LIA/LIAmax
    HLnorm=HL/HLmax
    BIOMASSnorm=BIOMASS/BIOMASSmax
    # print('VVmin value: \n',VVmin)
    # print('VHmin value: \n',VHmin)
    # print('HVmin value: \n',HVmin)
    # print('HHmin value: \n',HHmin)
    # print('LIAmax value: \n',LIAmax)
    # print('HLmax value: \n',HLmax)
    # print('BIOMASSmax value: \n',BIOMASSmax)
      
    # resamplig data for training
    VV=VVnorm[0:size:step]
    VH=VHnorm[0:size:step]
    HV=HVnorm[0:size:step]
    HH=HHnorm[0:size:step]
    LIA=LIAnorm[0:size:step]
    HL=HLnorm[0:size:step]
    BIOMASS=BIOMASSnorm[0:size:step]
    return VV,VH,HV,HH,LIA,HL,BIOMASS,VVmin,VHmin,HVmin,HHmin,LIAmax,HLmax,BIOMASSmax,size