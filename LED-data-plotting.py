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

#The maximum EQE value you are expecting
maximum_EQE= 2
#making a way for the code to work without copying into the data folder - the code now works one folder above the actual data, i.e. in your own EL data folder
data_folder_name = "sample_data"
# os.sep is a function which introduces the operating systems directory separater
data_folder_location = data_folder_name + os.sep
#get current working directory and add the data folder name to it so we can access the data
wd = os.getcwd() + os.sep + data_folder_location
#create a list of the files in the working directory ending in .ilv these are our current, voltage and EQE values
files = [f for f in os.listdir(wd) if (f.endswith('.ilv'))] 
#sort files alphabetically
files.sort()
#identifiers is an empty list
identifiers = []
#pixel is an empty list
pixel = []
#scan_number is an empty list
scan_number = []
#declaring a new variable called file which is one of the files in the list files. Each time we go through the loop 
#we go one down the list and split the filename into smaller chunks (separated by where there is a '_') and append 
#(this is a fancy word for add) the relevant chunks to the three lists we declared above. Here we have also used the 
#strip function to get rid of the file extension of the final chunk, we also converted the pixel number and scan number
#to integers from strings as this will likely be more useful to us.
for file in files:
    identifiers.append(file.split('_')[-3])
    pixel.append(int(file.split('_')[-2]))
    scan_number.append(int(file.split('_')[-1].strip('.ilv')))
#using the numpy unique function we are creating a list of all of the different variables    
unique_identifiers =  np.unique(identifiers)
#Creating an empty dictionary called data, a dictionary works by key value pairs soif we give it a key, i.e. voltage it can
#have all of our voltage data under that key
data = {}
#now we have isolated our unique identifiers and made a list of them we are entering a for loop which will repeat for each 
#item in that list. First we create an empty list called identifier_data which we will eventually fill with all of the data 
#which has that identifiers in our list of files 
for identifier in unique_identifiers:
    identifier_data = []
    #iterating through all of the files if we find the variable identifier in the file name create an empty dictionary called
    #this_data and then declare a new list called raw_data which is filled our raw data
    #we use the genfromtxt function to interpret and organise the raw data based on the tab delimiter and removing the headers
    for file in files:
        if identifier in file:
            this_data = {}
            raw_data = np.genfromtxt(data_folder_location+file, delimiter='\t', skip_header=1)
            #the data always comes out as an array of 12 columns and x rows so if there are less than two rows (I stopped the measurement)
            #continue out of the for loop and reject the data without using it
            if raw_data.size < 24:
                continue
            #now we are starting to fill the dictionary called this_data, we declare the key in the square brackets before the equals sign and the value is after the equals sign            
            this_data['I'] = -raw_data[:, 1]
            #masking erroneous current values and creating the key for corrected current data
            this_data['I_corrected'] = ma.masked_less(this_data['I'],-1000)
            this_data['V'] = -raw_data[:, 0] 
            # phi_e = raw_data[:, 2]
            # I_e_omega = raw_data[:, 3]
            # L_e_omega = raw_data[:, 4]
            this_data['EQE'] = raw_data[:, 8]
            #masking erroneous EQE values
            this_data['EQE_corrected'] = ma.masked_greater(this_data['EQE'], maximum_EQE)
            #add the newly written dictionary material in the dictionary this_data to the list identifier data 
            identifier_data.append(this_data)
    #now we are adding all of the data which we appended into the list idenifier_data and adding it to the dictionary data 
    data[identifier] = identifier_data

#plotting all EQE vs V curves for different variables in subfigures on a larger figure
fig, ax = plt.subplots(len(unique_identifiers), 1, figsize=(10,30))
plot_number = 0
for identifier, subax in zip(unique_identifiers, ax):
    plot_number = 0
    while plot_number < len(data[identifier]):
        label = plot_number +1
        subax.plot(data[identifier][plot_number]['V'],data[identifier][plot_number]['EQE_corrected'], label = f'{label}')
        plot_number += 1    
    subax.legend()
    subax.set_title(f'{identifier}')
    
fig.tight_layout()
#plotting all I vs V curves for different variables in subfigures on a larger figure
fig, ax = plt.subplots(len(unique_identifiers), 1, figsize=(10,30))
plot_number = 0
for identifier, subax in zip(unique_identifiers, ax):
    plot_number = 0
    while plot_number < len(data[identifier]):
        label = plot_number +1
        subax.semilogy(data[identifier][plot_number]['V'],data[identifier][plot_number]['I_corrected'], label = f'{label}')
        plot_number += 1    
    subax.legend()
    subax.set_title(f'{identifier}')
fig.tight_layout()
#plotting all EQE vs I curves for different variables in subfigures on a larger figure
fig, ax = plt.subplots(len(unique_identifiers), 1, figsize=(10,30))
plot_number = 0
for identifier, subax in zip(unique_identifiers, ax):
    plot_number = 0
    while plot_number < len(data[identifier]):
        label = plot_number +1
        subax.semilogx(data[identifier][plot_number]['I_corrected'],data[identifier][plot_number]['EQE_corrected'], label = f'{label}')
        plot_number += 1    
    subax.legend()
    subax.set_title(f'{identifier}')
fig.tight_layout()

#max_EQE boxplot
#generating a dictionary of the max data
max_EQE_data = {}
for identifier in unique_identifiers:
    data_point = 0
    max_EQE = []
    while data_point < len(data[identifier]):
        this_max = max(data[identifier][data_point]['EQE_corrected'])
        max_EQE.append(this_max)
        data_point += 1 
    max_EQE_data[identifier] = max_EQE

identifier_labels, the_data = max_EQE_data.keys(), max_EQE_data.values()
fig, ax = plt.subplots(figsize=(10,10))
ax.boxplot(the_data, labels = identifier_labels)
#ax.set_xticks(range(1, len(identifier_labels) + 1), identifier_labels)