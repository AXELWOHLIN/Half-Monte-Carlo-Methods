import os
import matplotlib.pyplot as plt
import pyne.ace
import numpy as np
from pyne.rxname import *
from tkinter import Tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import csv



first_word = '92235'
mt_number = '1'

sense_values = []

with open('csv_files/HEU-MET-FAST-001-001_MCNP_ENDF-B-VII.0-Continuous_SENS.txt') as f:
    header_found = False
    for line in f:
        if first_word in line and mt_number in line and 'total' in line:
            header_found = True
            continue
        else:
            if header_found == True and line.startswith(' '):
                data = [sense_values.append(float(x)) for x in line.split()]
            else:   
                header_found = False
        

sense_array1 = np.array(sense_values)

first_word = 'energy boundries:'

sense_values = []

with open('csv_files/HEU-MET-FAST-001-001_MCNP_ENDF-B-VII.0-Continuous_SENS.txt') as f:
    header_found = False
    for line in f:
        if 'energy' in line:
            header_found = True
            continue
        else:
            if header_found == True and line.startswith(' '):
                data = [sense_values.append(float(x)) for x in line.split()]
            else:   
                header_found = False
        
sense_array2 = np.array(sense_values)

sense_array1 = sense_array1[len(sense_array2):]
sense_array1 = sense_array1[:-9]


sense_array1 = sense_array1[::-1]
sense_array2 = sense_array2[::-1]

data = list(zip(sense_array2, sense_array1))

print("\nPlease choose a sensitivity vector in .csv format:")
root = Tk()
# Hide the main window
root.withdraw()
# ask the user to select a file using the filedialog
file_path = filedialog.askopenfilename()
print(file_path)
data = np.array(np.loadtxt(file_path, delimiter=','))
sens_vector_energy = data[:, 0]
sens_vector_values = data[:, 1]

sense_vector_values = np.multiply(sens_vector_values, sens_vector_energy)

plt.plot(sens_vector_energy, sense_vector_values)


#plt.plot(sense_array2, sense_array1)
plt.show()

# write the data to a CSV file
godiva=1
if godiva==0:
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)  # write data rows