# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 07:12:23 2025

@author: code developed @ CNR-IFAC by Emanuele Santi in the framework of 
NEU4BRIX project
"""
import pylab as pl
#
def plotscatterplot(estimatedBiomasses,measuredBiomasses,BIOMASSlow,BIOMASShigh,slope,intercept,validationfile,R,pval,RMSE):
    fig = pl.figure() #figsize=(10,5)    
    pl.rcParams.update(pl.rcParamsDefault)
    # Plot values:
    fig, ax = pl.subplots()
    ax.plot(estimatedBiomasses, measuredBiomasses, 'bo')

    # Plot 1:1:
    ax.plot([BIOMASSlow,BIOMASShigh], [BIOMASSlow,BIOMASShigh], '-k')

    # Plot trendline:
    ax.plot([BIOMASSlow,BIOMASShigh], [intercept, BIOMASShigh * slope + intercept], '-g')
    # blue_line = mlines.Line2D([], [], color='green', label='Trendline ($a$=' + str(round(slope, 2)) + ' | $b$=' + str(round(intercept, 2)) + ')')
    # ax.legend(handles=[blue_line], fancybox = True, shadow = True, loc = 'best', prop={'size':12})
    string = "a=%.2f\nb=%.2f\nR=%.3f\np-val=%.2f\nRMSE=%.2f t/ha\nN=%.0f" % (round(slope, 2),round(intercept, 2),R,pval,RMSE,len(estimatedBiomasses))
    pl.xlim(BIOMASSlow, BIOMASShigh)
    pl.ylim(BIOMASSlow, BIOMASShigh)
    pl.text(1,BIOMASShigh-160,string)    
    # define axis:
    ax.axis([BIOMASSlow,BIOMASShigh, BIOMASSlow,BIOMASShigh])

    # Set figure Layout:
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('Estimated biomass (ton/ha)')
    ax.set_ylabel('Ground truth biomass (ton/ha)')
    ax.grid(True)
    fig.savefig(validationfile)
    pl.draw() 
    

