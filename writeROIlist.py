# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 16:39:31 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import numpy as np
mainpath="D:\OneDrive - Consiglio Nazionale delle Ricerche\BIOMASS_BRIX\PYTHON\\DataIN\\ROI\\"
targetfile="ROIlist.npy"

# LOPE
rois=["ANGK","COL1","COL2","OKO1","OKO2","SAV1","SAV2","LOP01h","LOP02h","LOP03h","LOP07h","LOP08h","LOP09h","LOP10h","LOP11h","LOP12h"] #,"LPG02h"
measuredBiomasses=np.array([460.0,247.3,57.3,340.6,315.5,0.6,2.3,0.0,0.3,15.5,317.9,290.4,348.6,375.1,349.7,321.4]) # ,547.3
targetpath=mainpath+"LOPE\\"
np.save(targetpath+targetfile,[rois,measuredBiomasses])

#MABOUNIE 
rois=["MAB01h","MAB02h","MAB03h","MAB04h","MAB05h","MAB06h","MAB07h","MAB08h","MAB09h","MAB10h","MAB11h","MAB12h","Mabou001","Mabou003", "Mabou004", "Mabou006", "Mabou008", "Mabou012"]
measuredBiomasses=np.array([327.7,302.4, 333.6, 459, 438.8, 309.4, 247, 290.9 ,411.0 ,344.8 ,523.2, 171.8, 295.7, 342.1, 456.8, 308.0, 293.7, 152.1])
targetpath=mainpath+"MABOUNIE\\"
np.save(targetpath+targetfile,[rois,measuredBiomasses])

#MONDAH 
rois=["MNG03h","MNG04h","MON01h","MON02h","MON03h","MON05h","MON09h","MON10h","MON11h","MON13h","MON14h","MON19h","MON20h","MON21h","MON21Ah","MON22h","MON23h"]
measuredBiomasses=np.array([510.6,444.0,25.6,294.7,56.8,93.2,2.3,103.4,35.0,247.8,149.9,3.4,70.3,2.4,160.3,289.1,128.8])
targetpath=mainpath+"MONDAH\\"
np.save(targetpath+targetfile,[rois,measuredBiomasses])

#RABI
rois=["RAB01h","RAB02h","RAB03h","RAB04h","RAB05h","RAB06h","RAB07h","RAB08h","RAB09h","RAB10h","RAB11h","RAB12h","RAB13h","RAB14h","RAB15h","RAB16h","RAB17h","RAB18h","RAB19h","RAB20h","RAB21h","RAB22h","RAB23h","RAB24h","RAB25h"]
measuredBiomasses=np.array([210.7,280.3,303.2,300.1,320.6,301.0,413.2,209.4,280.1,323.3,287.8,310.1,246.4,245.6,313.1,253.7,265.9,262.5,255.1,348.5,301.2,246.7,296.1,511.8,293.4])
targetpath=mainpath+"RABI\\"
np.save(targetpath+targetfile,[rois,measuredBiomasses])
    