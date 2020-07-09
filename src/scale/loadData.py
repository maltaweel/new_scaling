'''
Created on Jul 9, 2020

@author: mark
'''
import csv

import os
from load.site import Site
from libpysal.cg.shapely_ext import area
from newLoad.analysis import RunSites

class LoadData:
    
    def load(self,fle):
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        

        #The data file path is now created where the data folder and dataFile.csv is referenced
        path=os.path.join(pn,'data',fle)
        
        return path
    
    def openData(self,fle):
        
        directory=self.load(fle)
        sites=[]
       
        try:
            
            #open file to read
            with open(os.path.join(directory,fle),'r') as csvfile:
                reader = csv.DictReader(csvfile)
                    
                #read the rows
                for row in reader:
                    s=Site()
          
                    #get the tweet text
                    area=row['Area']
                    site=row['Site']
                    period=row['Period']
                    
                    s.area=float(area)
                    s.site=site
                    s.period=period
                    
                    s.top=0.0
                    s.bottom=0.0
                    
                    if 'Top' in row:
                        top=row['Top']
                        s.top=float(top)
                    
                    if 'Bottom' in row:
                        bottom=row['Bottom']
                        s.bottom=float(bottom ) 
                        
                    sites.append(s)
                    
        except IOError:
            print ("Could not read file:", csvfile)
            
        
        return sites   
    
    
    '''
    Method to run the sentiment analysis.
    '''
    def run(self):
       
        sites=self.openData("houses.csv")
        
        rs=RunSites()
        rs.doSites(sites)
        rs.printResults(sites)
        
        #finished
        print('Finished')

if __name__ == '__main__':
    ld=LoadData()
    ld.run()
    