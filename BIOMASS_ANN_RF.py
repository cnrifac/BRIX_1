# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 14:18:10 2017

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
#for cleaning previously loaded  variables 
from IPython import get_ipython
get_ipython().magic('reset -sf')
#*************************************

import os as os
#os.environ['PROJ_LIB'] = 'C:\\Users\\Emanuele\\anaconda3\\Library\\share\\proj'
#os.environ['GDAL_DATA'] = 'C:\\Users\\Emanuele\\anaconda3\\Library\\share'

# import gdal
# from osgeo import gdal
#from osgeo.gdalconst import GA_ReadOnly
# import os as os
import numpy as np 
import joblib as joblib
import neurolab as nl 
import time as time
import glob as glob
from pathlib import Path
import sys
# import rasterio as rasterio
#from scipy.stats.stats import pearsonr
import pylab as pl
#import matplotlib.lines as mlines
# from matplotlib.colors import LinearSegmentedColormap
from functions.readband import readband
# from functions.loadtrain import loadtrain
from functions.ANNtrain import ANNtrain
from functions.RFtrain import RFtrain
# from functions.plottrain import plottrain
from functions.verifydir import verifydir
from functions.loadimages import loadimages
#import functions.roiStatistics as roiStatistics
from functions.savetiff import savetiff
from functions.showpng import showpng
from functions.plotscatterplot import plotscatterplot
from functions.dataload import dataload
# import functions.projectors as projectors
import functions.roiStatistics as roiStatistics

# from PIL import Image
# from osgeo.gdalconst import GA_ReadOnly

##################### defining paths and filenames ############################
trainflag="false"                                                               # "true" "false"
testflag="true"                                                               # "true" "false"
MLmethod="RF"                                                                  # "ANN" "RF"
indir="DataIN\\"                                                               # setting input data path 
traindir=indir + "TRAIN\\"                                                     # setting training data path (within indir)
outdir="DataOUT\\"                                                             # setting output data path
ANNdir="ML\\ANN\\"                                                             # setting path for saving the trained ANN
RFdir="ML\\RF\\"                                                               # setting path for saving the trained RF
trainfile="training.csv"                                                       # setting the training data file (to be replaced if other is available)
ANNfiguretrainfile="scatterplot_ANN_train.jpeg"                                # setting file name for the ANN training result plot
RFfiguretrainfile="scatterplot_RF_train.jpeg"                                  # setting file name for the RF training result plot
ANNfile="ANN.net"                                                              # setting file name for the trained ANN
RFfile="RF.rff"                                                                # setting file name for the trained RF
normfile="dataminmax.npy"                                                      # setting the file containing data normalization parameters (for training)
cwd = os.getcwd()
ROIfile="ROIlist.npy"                                                          # setting ROI data file
####################### other folder definitions ##############################
shapeFolderPrefix = cwd+ '\\' + indir + "ROI\\afrisar_dlr_roi_"                # setting ROI data path

##################### Defining general parameters #############################
BIOMASSlow=0                                                                   # lower limit of biomass value (t/ha) for data filtering and plots
BIOMASShigh=600                                                                # higher limit of biomass value (t/ha) for data filtering and plots
trainperc=20                                                                   # % of data in the training file to be used for training

###################### Defining ANN parameters ################################
nepochs=500                                                                    # number of training iterations
nshow=10                                                                       # display error every nshow iteration
valgoal=0.1                                                                    # target error to stop training
nneu=20                                                                        # Defining number of neurons in hidden layers  

###################### Defining RF parameters ################################
n_est = 500                                                                    #number of estimators
rnd_state = 0                                                                  # random state   
                                                          
############ checking and creating the destination directories ###############
verifydir(outdir)
verifydir(ANNdir)
verifydir(RFdir)

###################### summarizing configuration ##############################
print("**** summarizing configuration ****")
print("working dir is ", cwd)
print("training " + trainflag)
print("testing " + testflag)
print("ML method " + MLmethod)
##################### verifying for file existence ############################
existtrainfile=Path(traindir+trainfile)
if trainflag=="true" and not existtrainfile.is_file():
    print("training enabled but training file "+ traindir+trainfile + " missing: exiting ")
    sys.exit()  
    
if MLmethod=="ANN":
    existMLfile=Path(ANNdir+ANNfile)
elif MLmethod=="RF":
    existMLfile=Path(RFdir+RFfile)  
if trainflag=="false" and not existMLfile.is_file():
    print("training not enabled but trained "+ MLmethod + " missing: exiting ")
    sys.exit()  

##################### starting the main processing ############################
start = time.process_time()
startot =  time.process_time()
if trainflag=="true":  
    step=np.round(100/trainperc).astype(int)                                   # sampling for training 

    ################################## ANN ####################################
    if MLmethod=="ANN":
         ######################## Training ANN ################################
         net,err,VVmin,VHmin,HVmin,HHmin,LIAmax,HLmax,BIOMASSmax=ANNtrain(nepochs,nshow,valgoal,nneu,step,traindir,trainfile,BIOMASSlow,BIOMASShigh)
         # print("**** ANN training completed, plotting outputs ****")
         pl.savefig(ANNdir+ANNfiguretrainfile)
         pl.show()         
         ####################### Saving the ANN ###############################
         print("**** Saving ANN ****")
         net.save(ANNdir+ANNfile)
         maxarray=[VVmin,VHmin,HVmin,HHmin,LIAmax,HLmax,BIOMASSmax]
         np.save(ANNdir+normfile,maxarray)         

    ################################## RF ####################################
    elif MLmethod=="RF":
         rf=RFtrain(n_est,rnd_state,step,traindir,trainfile,BIOMASSlow,BIOMASShigh)
         pl.savefig(RFdir+RFfiguretrainfile)
         pl.show()
         ####################### Saving the RF ###############################
         print("**** Saving RF ****")
         joblib.dump(rf, RFdir+RFfile)  
         
############################## TESTING  #######################################
#Loading Images
if len(glob.glob(indir + 'IMAGES\\**\\*VV.tif', recursive=True))==0:
    print("input images missing, please revise configuration parameters: exiting ") 
    sys.exit()
    
for filename in glob.iglob(indir + 'IMAGES\\**\\*VV.tif', recursive=True):   
       
    ###################### defining in/out filenames ##########################
    VVfile=filename  
    file=os.path.basename(filename)                                          # shows the filename without path
    path=os.path.dirname(filename)                                           # shows the path
    ROIlistfile=path.replace("IMAGES","ROI") + "\\" + ROIfile    
    
    ######################### checking for files ##############################
    existSARfile=Path(VVfile) 
    existROIfile=Path(ROIlistfile)    

        
    if not existROIfile.is_file():
        print("ROI list missing, please revise configuration parameters: exiting ")
        break
   ########################## Loading dimensions ##############################     
    _,_,dim0,dim1,_,_,_=readband(VVfile)
    
   ########################### creating outputs ###############################     
    outtiff=filename.replace(indir+"IMAGES\\",outdir)
    
    if MLmethod=="ANN":
        outtiff=outtiff.replace("_VV.tif", "_ANN_BIOMASS.tif") 
           
    elif MLmethod=="RF":
        outtiff=outtiff.replace("_VV.tif", "_RF_BIOMASS.tif")         
    verifydir(os.path.dirname(outtiff)) 
    validationfile=outtiff.replace("_BIOMASS.tif", "_validation.png")  
    if testflag=="true":
        # defining input data
        HVfile=filename.replace("_VV.tif", "_HV.tif")
        VHfile=filename.replace("_VV.tif", "_VH.tif")
        HHfile=filename.replace("_VV.tif", "_HH.tif")
        LIAfile=filename.replace("_VV.tif","_LIA.tif")
        HLfile=filename.replace("_VV.tif","_HLidar.tif")
        #################### loading input data ###############################
        inp,ds,dim0,dim1,proj,geoinformation,driver,BIOMASSmax,mask=loadimages(VVfile,HVfile,VHfile,HHfile,HLfile,LIAfile,ANNdir,normfile)
        print("**** Data loaded, starting inversion ****")
        
        ##################### computing biomass ###############################
        start = time.process_time()
        if MLmethod=="ANN":
            # Loading the ANN
            net = nl.load(ANNdir+ANNfile)  
            BIOMASS = np.reshape(net.sim(inp)*BIOMASSmax,(dim0,dim1)) #
            
        elif MLmethod=="RF":
            rf=joblib.load(RFdir+RFfile)
            BIOMASS = np.reshape(rf.predict(inp),(dim0,dim1))
            
        BIOMASS=BIOMASS*mask
        BIOMASS[BIOMASS<BIOMASSlow]=BIOMASSlow
        BIOMASS[np.isnan(BIOMASS)]="NaN"

        # Saving Tiff
        print("**** saving output tiff image ****")
        savetiff(outtiff, dim1, dim0,BIOMASS,mask,driver,proj,geoinformation) 
        elapsed = (time.process_time() - start)  
    # Show preview
    print("**** Done, showing image ****")  
    showpng(outtiff,dim0,dim1)   
    
    ############################# VALIDATION ##################################
    rois,measuredBiomasses=dataload(ROIlistfile)
    stats = roiStatistics.getRoiStats(outtiff, shapeFolderPrefix, rois)
    estimatedBiomasses = stats['mean']
    statistics = roiStatistics.stats(measuredBiomasses,estimatedBiomasses)
    [slope, intercept, r_value, p_value, std_err, bias, covariance, rmsd] = statistics
    print('slope :' + str(slope))
    print('intercept :' + str(intercept))
    print('r_value :' + str(r_value))
    print('p_value :' + str(p_value))
    print('std_err :' + str(std_err))
    print('bias :' + str(bias))
    print('covariance :' + str(covariance))
    print('rmsd :' + str(rmsd))
    # Plotting scatterplot
    
    plotscatterplot(measuredBiomasses,estimatedBiomasses,BIOMASSlow,BIOMASShigh,slope,intercept,validationfile,r_value,p_value,rmsd)

    #Save the image as scatterplot between measured and estimated Biomass in outdir_ANN with this name. You have to
    #modify the name of the image for each elaboration

    ######################### cleaning variables  #############################
    # del outtiff,HHfile,HVfile,VHfile,VVfile,HLfile,ds,driver,proj,geoinformation,
    # HH,HV,VH,VV,dim0,dim1,mask,LIA,inp,start,BIOMASS,elapsed
print("**** end of loop ****")
elapsedtot = (time.process_time() - startot)
print("**** time elapsed ",round(elapsedtot/60,0),"minutes, ", round(elapsedtot,0)-round(elapsedtot/60,0)*60, " seconds ****" )
    



