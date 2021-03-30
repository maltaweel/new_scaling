'''
Scaling analysis for urban contexts. 


Algorithm based on scaling such as from:
Lobo, J., Bettencourt, L.M.A., Strumsky, D., West, G.B., 2013. 
Urban Scaling and the Production Function for Cities. 
PLoS ONE 8, e58407. https://doi.org/10.1371/journal.pone.0058407

Created on Aug 7, 2017

@author: 
'''

import math
import csv
import os

from scipy.stats import linregress


class FitAnalysis:
    
    '''
    Initialization (constructor) for the class.
    '''
    def __init__(self):
        
        #constant is the constants to try in the scaling analysis
        self.constants=[]
        
        #start the initial constant with 1 as the default, with best fit fixed to this
        self.bestFitConstant=1
        
        #range of values for give site and area
        self.range={}
        
        #fitted beta to keep
        self.goodB=1000.0
        
        #best fit value
        self.best=1000000000.0
        
        #dictionary to contain error values
        self.dict=  {}
        
        #list for storing error values
        self.llst=[]
        
        #total error of the fit analysis
        self.totalError=0
        
        #total iterations
        self.totalL=0
        
        #set the initial constants to try
        a=0
        for i in range(1,600):
            self.constants.append(a+0.1)
            a+=0.1
            i+=1
        
    
    '''
    Method to apply the fit measure applying scaling based on Lobo et al. 2013.
    @param constant: the constant value in the function
    @param beta: the beta value
    @return: error from the constant and beta values attempted.
    '''       
    def fitMeasure(self,constant,beta):
        error=0

        for i in range(0,len(self.site)):
            x=self.area[i]
            if(x<0):
                continue
            
            
            try:
                result=math.log(constant)+(beta*math.log(x))
            except:
                print('stop')
            #result=constant*math.pow(x,beta)
                
            
            avg=math.log(self.avg_structure[i])
            #avg=self.avg_structure[i]
            
            error+=math.pow(result-avg,2)
          
         
        s=str(constant)+":"+str(beta)
        
        self.dict[s]=error
        
        return error
    
    '''
    Load data from input.csv file from data folder.
    '''
    def loadData(self):
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        
        self.site=[]
        self.area=[]
        self.upper=[]
        self.lower=[]
        self.weighted=[]
        self.avg_structure=[]
        self.std=[]

        #The data file path is now created where the data folder is referenced
        path=os.path.join(pn,"data","input.csv")
        
        f = open(path, 'rU')
        
        
        #use a try clause to read the file to catch input error
        try:
            reader = csv.DictReader(f)
          
            #for loop in the file rows
            for row in reader:
                
                #input the site and structure areas
                site=row['Town']
                area=float(row['Area'])
                structure_area=float(row['Straightness'])
            #   maximum_area=float(row['Maximum Area'])
            #   minimum_area=float(row['Minimum Area'])
            #   pn=int(row["Period n."])
                
                #this is to filter given periods (if needed)
                #if pn>=5:
                #    continue   
                                            
                self.site.append(site)
                self.area.append(area)
              
                self.avg_structure.append(float(structure_area))
            #   self.upper.append(float(maximum_area))
            #   self.lower.append(float(minimum_area))

       
        #then close the file
        finally:
            f.close()
            
    '''
    Method to find the best fits for constant under given beta.
    @param b: beta value for the fit function
    @return: best fit based on error of beta and constant values
    '''
    
    def cost(self,b):
        
    #    if b<0:
    #        b=0
            
       
        beta=b
        
        for t in range(0,len(self.constants)):
             
            fit=self.fitMeasure(self.constants[t], beta)
            print(str(self.constants[t])+":"+str(beta))
            if(fit<self.best):
                    self.best=fit
                    self.bestFitConstant=self.constants[t]
                    self.goodB=beta
        
        return self.best
    
    '''
    Method used to determine range to try for beta.
    '''     
    def rangeDetermine(self):
            
        solution=0.05
        i = 0
        old_cost = self.cost(0.0)
        currentI=0.01
        
        t=0
   
        while i <800:
           
   
            
            new_cost = self.cost(currentI)
    
            if old_cost > new_cost:
                old_cost = new_cost
            
            elif old_cost==new_cost and i<400:
                currentI-=0.01 
                t+=1 
            else:
                if currentI<0:
                    currentI=0.01
                currentI+=0.01
                
            i += 1
            
    '''
    Using all sites, method to find the range of best fit for 
    beta and constant and update fit for sites.
    '''
    def rangeOfFit(self):
        for i in range(0,len(self.site)):
            s=self.site[i]
            a=self.area[i]
  
    #      if(a<1):
    #          continue
            fst=math.log(self.avg_structure[i])
            #fst=self.avg_structure[i]
            if(1000000000.0==fa.best):
                continue
            
            
            result=((math.log(self.bestFitConstant))+(self.goodB*math.log(a)))-fst
            #result=self.bestFitConstant*math.pow(a,self.goodB)-fst
            bf=0.0
            
            ii=0
            if(result<0):
                while(result<0):
                    
                    bf+=0.01
                #    result=self.bestFitConstant*math.pow(a,self.goodB+bf)-fst
                    result=((math.log(self.bestFitConstant))+(self.goodB*math.log(a)+bf))-fst
               
                    print(str(bf)+":"+str(result))
                    ii+=1
                
            else:
                while(result>0):
                   
                    bf-=0.01
                #    result=self.bestFitConstant*math.pow(a,self.goodB+bf)-fst
                    result=((math.log(self.bestFitConstant))+(self.goodB*math.log(a)+bf))-fst
               
                    print(str(bf)+":"+str(result))
                    ii+=1
            
            
            self.range.update({s:bf})
    
    '''
    Error results for fits for given sites.
    Method outputs errors to error file in output.
    @param method: name of method for error results used for file name
    '''     
    def printErrorTable(self,method):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        
        #The data file path is now created 
        path=os.path.join(pn,'output')
        
        filename=path+'/'+'error_results'+method+'.csv'
        
        
        fieldnames = ['Constant','Beta',"Overall Error"]
        
        with open(filename, 'wb') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            self.llst=[]
            for s in self.dict:
                ss=s.split(":")
                v=self.dict[s]
                
                self.llst.append(v)
                const=float(ss[0])
                beta=float(ss[1])
                
                
                
                if(const>100.0):
                    continue
                
                
                if(beta>2.00):
                    continue
                
                writer.writerow({'Constant':str(const),
                                'Beta':str(beta),'Overall Error':str(v)})
    '''
    Print outputs from fit analysis for scaling.
    @param n: the typeof analysis used for the output file name
    
    '''            
    def printResult(self,n):
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        
        #The data file path is now created where the data folder and dataFile.csv is referenced
        path=os.path.join(pn,'output')
        
        filename=path+'/'+'scaling_avg_width_orig'+str(n)+'.csv'
        
        fieldnames = ['Site','Area',"Structure Size","Estimated Size","Constant","Beta","Fitted Beta","Estimate Ratio","Estimated Average",
                      "Estimate Error"]
        
       
        self.medianError=[]
        self.logSizes=[]
        self.logHollows=[]
        with open(filename, 'w') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            for s in range(0, len (self.site)):
                            site=self.site[s] 
                            rnge=0 
           
                           
                            if(self.area[s]<1):
                                #rnge='NA'
                                rnge=self.range[site]
                            else:
                                rnge=self.range[site]
                                 
                            obs=math.log(self.avg_structure[s])
                            
                            self.logHollows.append(obs)
                            self.logSizes.append(math.log(self.area[s]))
                            
                        #    calculated=self.bestFitConstant*math.pow(self.area[s],self.goodB)
                            calculated=math.log(self.bestFitConstant)+(self.goodB*math.log(self.area[s]))
                           
                            res=0
                            
                            if(calculated>0 and self.avg_structure[s]>1):
                                res=math.log(obs/calculated)
                            
                            est=math.pow(math.e,calculated)
                        #    est=calculated
                            rc=math.fabs(est-self.avg_structure[s])
                            
                            avgError=rc
                            
                            self.medianError.append(avgError)
                            self.totalError+=avgError
                            self.totalL+=1
                            writer.writerow({'Site': str(self.site[s]),'Area':str(self.area[s]),
                                'Structure Size':str(self.avg_structure[s]),"Estimated Size": str(calculated),'Constant':str(self.bestFitConstant),
                                'Beta':str(self.goodB),'Fitted Beta':str(rnge), "Estimate Ratio":str(res),"Estimated Average":str(est),
                                "Estimate Error":str(rc)})



#the main steps to run the analysis
fa = FitAnalysis()
fa.loadData()
fa.rangeDetermine()

fa.rangeOfFit()
fa.printResult('structure-area')
#fa.printErrorTable(method+str(i)+str("_"+str(n)))
    
#v=min(fa.llst)
nn=0
print("Finished")

