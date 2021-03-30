'''
Created on Mar 30, 2021

@author: maltaweel
'''
import csv
import os

#The object descriptions to incorporate
objects=[]

#The prices of objects to incorporate
prices=[]

#The location of objects to incorporate
locations=[]

#The links of objects to incorporate
links=[]

#Extra objects to track and remove
totalThings=[]

#List keeping track of extra prices for the same object descriptions used to remove data
priceExtra=[]

#data on sellers
sellers=[]

#image data
images=[]

news=[]
'''
Method to load data from input files in the totalData folder.
'''
def loadData():
    
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'totalData')
    
    totals={}
   
    between=[]
    close=[]
    deg=[]
    harm=[]
    eige=[]
    eifficent=[]
    straight=[]
    currentF=[]
    kz=[]
    
  
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
            print(csvfile)
           
            for row in reader:   
                bteween=row['betweenness']
                closness=row['closeness']
                degree=row['degree']
                straigh=row['straightness']
#                image=row['Image']
                katz=row['katz']
                eigen=row['eigenvector']
                cFlow=row['current flow']
                harmonic=row['harmonic']
                eff=row['efficiency']
                
                between.append(bteween)
                close.append(closness)
                deg.append(degree)
                harm.append(harmonic)
                eige.append(eigen)
                eifficent.append(eff)
                straight.append(straigh)
                currentF.append(cFlow)
                kz.append(katz)
              
                        
          
                
    totals['Betweenness']=between
    totals['Closeness']=close
    totals['Degree']=deg
    totals['Harmonic']=harm
    totals['Eigenvector']=eige
    totals['Efficiency']=eifficent
    totals['Straightness']=straight
    totals['Current Flow']=currentF
    totals['Katz']=kz
    
              
    return totals            
     
'''
Method to print the results of the output
'''                   
def printResults(totals):

    fieldnames = ['Betweenness','Closeness','Degree', 'Current Flow','Katz'
                  'Harmonic','Eigenvector','Straightness','Efficiency']
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"totals.csv")
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        
        writer.writeheader()      
    
        between=totals['Betweenness']
        close=totals['Closeness']
        deg=totals['Degree']
        harm=totals['Harmonic']
        eigenvector=totals['Eigenvector']
        eifficiency=totals['Efficiency']
        straightness=totals['Straightness']
        currentFlow=totals['Current Flow']
        katz=totals['Katz']
        
        for i in between :
            b=between[i]
            c=close[i]
            d=deg[i]
            h=harm[i]
            e=eigenvector[i]
            ef=eifficiency[i]
            s=straightness[i]
            cf=currentFlow[i]
            k=katz[i]   
            writer.writerow({'Betweenness':str(b),'Closeness':str(c),'Degree':str(d),
                             'Harmonic':str(h),'Eigenvector':str(e),
                             'Straightness':str(s),'Current Flow':str(cf),'Katz':str(k),
                             'Eifficency':str(ef)})
'''
Method to run the module
'''           
def run():
#    train_model()
    totals=loadData()
    printResults(totals)
    print("Finished")
   
if __name__ == '__main__':
    run()