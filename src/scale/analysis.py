'''
Created on Jul 22, 2017

@author: maltaweel
'''
from load.site import Site
import numpy as np
import csv
import math
import scipy.optimize as scp
import os


class RunSites:
    
    def doSites(self,sites):
        
        for s in sites:
            area=s.area
            site=s.site
            top=s.top
            bottom=s.bottom



    def regression(self,areas,hollows):
        result=0
        scp.curve_fit(lambda t,a,b: math.pow(a*areas,t),  areas,  hollows, p0=(4, 0.1))
        return result
    
    def getEnds(self,sites):
        
        endss=[]
        for s in sites:
            firsts=s.firsts  
            if len(firsts)==0:
                continue
            
            #ends=math.log(s.endV)
            ends=s.endV
            endss.append(ends)
        
        return np.array(endss)
    
    def getFirsts(self,sites):
        
        firstss=[]
        for s in sites:
            
            firsts=s.firsts  
            if len(firsts)==0:
                continue
            
            #firsts=math.log(s.firstsV)
            firsts=s.firstsV
            firstss.append(firsts)
        
        return np.array(firstss)
    
    def getMids(self,sites):
        
        midss=[]
        for s in sites:
            firsts=s.firsts  
            if len(firsts)==0:
                continue
            
            #mids=math.log(s.midV)
            mids=s.midV
            midss.append(mids)
        
        return np.array(midss)
    
    
    def getAreas(self,sites):
        
        areas=[]
        for s in sites:
            
            # area=math.log(s.area)
            area=s.area
            areas.append(area)
        
        return np.array(areas)
    
    def getChalAreas(self,sites):
        
        areas=[]
        for s in sites:
            
            #area=math.log(s.chalc)
            area=s.chalc
            areas.append(area)
        
        return np.array(areas)
    
    def getEBAAreas(self,sites):
        
        areas=[]
        for s in sites:
            
            #area=math.log(s.eba)
            area=s.eba
            areas.append(area)
        
        return np.array(areas)
    
    def getMBAAreas(self,sites):
        
        areas=[]
        for s in sites:
            
            #area=math.log(s.mba)
            area=s.mba
            areas.append(area)
        
        return np.array(areas)
    
    def printResults(self,sites):
    
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        

        #The data file path is now created where the data folder and dataFile.csv is referenced
        path=os.path.join(pn,'output')
        
        filename=path+'/'+'site_results_original.csv'
        
        fieldnames = ['Name','Period','Area','Temple Area']
        
        with open(filename, 'w') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            for s in sites:  
                if s.area==0:
                    continue
          
                 
                writer.writerow({'Name': str(s.name),'Period': str(s.idd),'Site Area':str(s.area),
                                     'Structure Area':str(s.eba)})
        