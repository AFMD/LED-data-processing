# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 17:18:49 2018

@author: warby
"""
import os
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import sys

data_folder_name = "sample_data"
data_folder_location = data_folder_name + os.sep
#get current working directory
wd = os.getcwd() + os.sep + data_folder_location
#create a list of the files in the current working directory ending in .ilv 
files = [f for f in os.listdir(wd) if (f.endswith('.ilv'))] 
#sort files alphabetically
files.sort()

identifiers = []
pixel = []
scan_number = []
for file in files:
    identifiers.append(file.split('_')[-3])
    pixel.append(int(file.split('_')[-2]))
    scan_number.append(int(file.split('_')[-1].strip('.ilv')))
    

# print(identifiers)
unique_identifiers =  np.unique(identifiers)

data = {}

for identifier in unique_identifiers:
    identifier_data = []
    for file in files:
        if identifier in file:
            this_data = {}
            raw_data = np.genfromtxt(data_folder_location+file, delimiter='\t', skip_header=1)
            if raw_data.size < 24:
                continue            
            this_data['I'] = -raw_data[:, 1]
            this_data['I_corrected'] = ma.masked_less(this_data['I'],-1000)
            this_data['V'] = -raw_data[:, 0] 
            # phi_e = raw_data[:, 2]
            # I_e_omega = raw_data[:, 3]
            # L_e_omega = raw_data[:, 4]
            this_data['EQE'] = raw_data[:, 8]
            this_data['EQE_corrected'] = ma.masked_greater(this_data['EQE'],2)
            identifier_data.append(this_data)
    data[identifier] = identifier_data
            

# here is how you read voltage fromone of the files    
some_voltage = data['0.6-1'][1]['V']
print(some_voltage)

sys.exit(-1)

# some example:
# 


#new_files = [x for x in files if (x.split('_')[-3] is '0.6-1')]



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
    

