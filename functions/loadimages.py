# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 15:03:50 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
from functions.readband import readband
import numpy as np
#
def loadimages(VVfile,HVfile,VHfile,HHfile,HLfile,LIAfile,ANNdir,normfile):    
    #Loading min/max for normalization
    maxarray=np.load(ANNdir+normfile)
    # VVmin=maxarray[0]
    # VHmin=maxarray[1]
    # HVmin=maxarray[2]
    # HHmin=maxarray[3]
    # LIAmax=maxarray[4]
    # HLmax=maxarray[5]    
    BIOMASSmax=maxarray[6]
    ############################ VV ###########################################
    print('Processing image \n', VVfile)
    ds,VV,dim0,dim1,proj,geoinformation,driver=readband(VVfile)
    
    ############################ VH ###########################################
    print('Processing image \n', VHfile)
    _,VH,_,_,_,_,_=readband(VHfile)
    ############################ HV ###########################################
    print('Processing image \n', HVfile)
    _,HV,_,_,_,_,_=readband(HVfile)
    ############################ HH ###########################################
    print('Processing image \n', HHfile)
    _,HH,_,_,_,_,_=readband(HHfile)
    ############################ LIA ##########################################
    print('Processing image \n', LIAfile)
    _,LIA,_,_,_,_,_=readband(LIAfile)
    ########################### HLidar ########################################
    print('Processing image \n', HLfile)
    _,HL,_,_,_,_,_=readband(HLfile)
    # print("**** normalizing data ****")
    # VVnorm=VV/VVmin
    # VHnorm=VH/VHmin
    # HVnorm=HV/HVmin
    # HHnorm=HH/HHmin
    # LIAnorm=LIA/LIAmax
    # HLnorm=HL/HLmax
    # print('VVmin value: \n',VVmin)
    # print('VHmin value: \n',VHmin)
    # print('HVmin value: \n',HVmin)
    # print('HHmin value: \n',HHmin)
    # print('LIAmax value: \n',LIAmax)
    # print('HLmax value: \n',HLmax)  
    inp = np.column_stack((HH,HV,VH,VV,HL)) #LIA,
    mask=np.ones((dim0,dim1))
    mask[np.isnan(np.reshape(VV,(dim0,dim1)))] = "nan"
    mask[np.reshape(VV,(dim0,dim1))==0]="nan"
    return inp,ds,dim0,dim1,proj,geoinformation,driver,BIOMASSmax,mask