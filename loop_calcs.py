import os
import matplotlib.pyplot as plt
import pyne.ace
import requests
import np_csvimport
from scipy.interpolate import interp2d
from scipy.interpolate import interp1d
import numpy as np

results_vector = np.zeros(shape = (99,1))
file_indxs = ["00","01","02","03","04","05","06","07","08","09"] + list(range(10,100))
for i in file_indxs:
    if int(i) == 44:
        continue
    # Navigate to the file within the directory
    file_path = os.path.join('U235.nuss.10.10.2016', f'U235-n.ace_00{i}')
    # Open the file and read its contents
    with open(file_path, 'rb') as infile:
        file_contents = infile.read()

    # Write the contents to a new file
    with open('U235.ace', 'wb') as outfile:
        outfile.write(file_contents)

    lib = pyne.ace.Library('U235.ace')
    lib.read('92235.00c')
    lib.tables
    w180 = lib.tables['92235.00c']
    total_xs = w180.sigma_t
    energy = w180.energy

    filename = 'csv_files/totalgodiva-Sheet1.csv'
    sens_vector_energy, sens_vector_values = np_csvimport.csv_import(filename)
    energy *= 1e+06

    sens_vec_values_adjusted = np.interp(energy,sens_vector_energy,sens_vector_values)
    if int(i)>=44:
        results_vector[int(i)-1,0] = np.dot(sens_vec_values_adjusted,total_xs.transpose())
    else:
        results_vector[int(i),0] = np.dot(sens_vec_values_adjusted,total_xs.transpose())
    print(f"Our scalar is {np.dot(sens_vec_values_adjusted,total_xs.transpose())}")