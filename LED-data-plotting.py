# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 17:18:49 2018

@author: warby
"""
import os
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
#get current working directory
cwd = os.getcwd() 
#create a list of the files in the current working directory ending in .ilv 
files = [f for f in os.listdir(cwd) if (f.endswith('.ilv'))] 
#sort files alphabetically
files.sort()
#for x in files:
#    identifier = x.split('_')[-3]
## iterate through the list of files, opening each, picking out the necessary data
#    print(identifier)
    

for f in files:
    data = np.genfromtxt(f, delimiter='\t', skip_header=1)
#    badvalues = np.where(data > 1e30)
#    new_data = np.delete(data, (badvalues[0]), axis=0)
    if data.size < 24:
        continue
    I = -data[:, 1]
    I_corrected = ma.masked_less(I,-1000)
    V = -data[:, 0] 
    phi_e = data[:, 2]
    I_e_omega = data[:, 3]
    L_e_omega = data[:, 4]
    EQE = data[:, 8]
    EQE_corrected = ma.masked_greater(EQE,2)
    splitlabel = f.split('_')
    label = '_'.join(splitlabel[-4:-1])
    plt.plot(V,EQE_corrected, label = f'{label}') 
    
plt.legend()
    