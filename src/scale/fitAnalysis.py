'''
Created on Aug 7, 2017

@author: maltaweel
'''

import math
import csv
import os
import numpy as np
from sklearn.metrics import r2_score
from scipy.stats import linregress

class FitAnalysis:
    
    def __init__(self):
        self.constants=[]
        self.bestFitConstant=1
        self.memory1=[0.0]
        self.memory2=[0.1]
        self.range={}
        self.goodB=1000.0
        self.best=1000000000.0
        self.dict=  {}
        self.llst=[]
        self.totalError=0
        self.totalL=0
        
        a=0
        for i in range(1,600):
            self.constants.append(a+0.1)
            a+=1.0
            i+=1
              
    def fitMeasure(self,constant,beta):
        error=0

        for i in range(0,len(self.site)):
            x=self.area[i]
            if(x<0):
                continue
            
            
            result=math.log(constant)+(beta*math.log(x))
            #result=constant*math.pow(x,beta)
                
            
            avg=math.log(self.avg_structure[i])
            #avg=self.avg_structure[i]
            
            error+=math.pow(result-avg,2)
          
         
        s=str(constant)+":"+str(beta)
        
        self.dict[s]=error
        
        return error
    
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

        #The data file path is now created where the data folder and dataFile.csv is referenced
        path=os.path.join(pn,"data","input.csv")
        
        f = open(path, 'rU')
        
        
        #We can use a try clause to read the file
        try:
            reader = csv.DictReader(f)
          
            #for loop, skipping the first line (i.e., when i is 0)
            for row in reader:
                
                site=row['Site']
                area=float(row['Site Area'])
                structure_area=float(row['Structure Area'])
                maximum_area=float(row['Maximum Area'])
                minimum_area=float(row['Minimum Area'])
                pn=int(row["Period n."])

                if pn>=5:
                    continue   
                                            
                self.site.append(site)
                self.area.append(area)
              
                self.avg_structure.append(float(structure_area))
                self.upper.append(float(maximum_area))
                self.lower.append(float(minimum_area))

       
        #then close the file
        finally:
            f.close()
            

    def cost(self,a,b):
        
        if a<0:
            a=0
        if b<0:
            b=0
            
       
        beta=b
        
        for t in range(0,len(self.constants)):
             
            fit=self.fitMeasure(self.constants[t], beta)
            print(str(self.constants[t])+":"+str(beta))
            if(fit<self.best):
                    self.best=fit
                    self.bestFitConstant=self.constants[t]
                    self.goodB=beta
        
        return self.best
            
    def rangeDetermine(self):
            
        solution=0.05
        i = 0
        old_cost = self.cost(0.0,0.0)
        currentI=0.01
   
        while i <150:
           
   
            
            new_cost = self.cost(currentI,currentI)
    
            if old_cost > new_cost:
                old_cost = new_cost
          
            i += 1
            currentI+=0.01
            

        return solution, old_cost

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
            
    def printErrorTable(self,method):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        
        #The data file path is now created where the data folder and dataFile.csv is referenced
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
                
                
                
                if(const>5.0):
                    continue
                
                
                if(beta>1.25):
                    continue
                
                writer.writerow({'Constant':str(const),
                                'Beta':str(beta),'Overall Error':str(v)})
    
    """
    Return R^2 where x and y are array-like.
    """
    def rsquared(self,x, y):

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        return r_value**2         
            
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

newllst=[]
const=[]
betas=[]
sizes=[]
method='max_road'
totalError=[]
totalLines=[]
medianError=[]
rsquared=[]
sampleNumber=[]


size=0.0
fa = FitAnalysis()
fa.loadData()
solution=fa.rangeDetermine()

fa.rangeOfFit()
fa.printResult('structure-area')
#fa.printErrorTable(method+str(i)+str("_"+str(n)))
    
#v=min(fa.llst)
nn=0
print("Finished")

'''
for s in fa.number:
    nn+=s
        
    if nn==0:
        continue
        
    error=v/float(nn)
    newllst.append(error)
    const.append(fa.bestFitConstant)
    betas.append(fa.goodB)
    sizes.append(fa.area[s])
    totalError.append(fa.totalError)
    totalLines.append(fa.totalL)
    medianError.append(np.median(fa.medianError))
        
    r2=fa.rsquared(fa.logSizes,fa.logHollows)
    rsquared.append(r2)
    sampleNumber.append(len(fa.site))
        
pn=os.path.abspath(__file__)
pn=pn.split("src")[0]
path=pn+'/output/'
        
filename=path+'best_fit_validation.csv'
        
fieldnames = ['Hollow.Ways','Site.Size','Constant','Beta','Error', 'Median Error', 'RSquared','Sample Number']     
with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()
        tt=sizes[0]
        hn=0           
        for t in range(0,len(newllst)):
            fa.medianError[:]
            
            if sizes[t] == tt:
                hn+=1
                tt=sizes[t]
            else:
                hn=1
                tt=sizes[t]
            
            print('Size: '+str(sizes[t])+ " Error: "+str(float(totalError[t]/totalLines[t]))+
                  " Median Error: "+str(medianError[t]) 
                  +" Constant: "+str(const[t])+ " Beta: "+str(betas[t]))
            writer.writerow({'Hollow.Ways':str(hn),'Site.Size': str(sizes[t]),'Beta':str(betas[t]),'Constant':str(const[t]),
                             'Error':str(float(totalError[t]/totalLines[t])),'Median Error':str(str(medianError[t])),
                             'RSquared':str(rsquared[t]), 'Sample Number':str(sampleNumber[t])})
'''