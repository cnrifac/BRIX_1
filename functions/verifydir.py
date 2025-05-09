# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 14:38:28 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import os
#
def verifydir(target_dir):    
    outdirexist=os.path.exists(target_dir)
    if outdirexist==False:
        print("**** creating output directory ****")
        os.makedirs(target_dir)
    