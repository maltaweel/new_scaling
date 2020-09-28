# new_scaling

This Python (3.6) project applies scaling for data in the data folder. The code used for scaling is in the src/scale/fitAnalysis.py module.
The method applies the scaling approach in Lobo et al. 2013 and elsewhere (see module). Output is in the output folder. To run the code, you need an input.csv file in the
/data folder. The following columns are required:  Site, Structure Area,	Site Area,	Period n.
The Site column is the name of the site, the Structure Area (in m2) is the structure area, the Site Area
is the site's area in ha, and Period n. is the period number as an integer.

The output folder contains the output .csv file. A Jupyter Notebook file in the /src/scale/ folder is included to test the code.

Libraries used are in the requirements.txt. 
