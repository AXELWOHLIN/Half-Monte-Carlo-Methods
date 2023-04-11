import os
import matplotlib.pyplot as plt
import pyne.ace
import requests
import np_csvimport
from scipy.interpolate import interp2d
from scipy.interpolate import interp1d
import numpy as np
from pyne.rxname import *

#First number is MT and second is filename
name_dict = {"n,2n":("2n","n_2n"),"n,3n":("z_3n","n_3n"),"n,4n":("z_4n","n_4n") \
                ,"fission":("fission","fission"), "elastic":("elastic","elastic") \
                    ,"inelastic":("inelastic","inelastic"),"total":("total","total")}

# list all the keys in name_dict
keys = list(name_dict.keys())

# prompt the user to choose a key
print("Choose a reaction:")
for i, key in enumerate(keys):
    print(f"{i+1}. {key}")
choice = input("Enter the number of the reaction: ")

# get the corresponding value based on the user's choice
chosen_key = keys[int(choice)-1]
mt_number,filespec = name_dict[chosen_key]
# use the filename and mt_number variables to do further processing

reaction_ind = mt(mt_number)

#central_file_name = os.path.join('U235.nuss.10.10.2016', f'U235-n.ace_0000')
central_file_name = os.path.join('ENDF_to_ACE/processed_ace_files/', f'0_AceFile.ace')
with open(central_file_name, 'rb') as infile:
    central_file_contents = infile.read()

    # Write the contents to a new file
with open('U235central.ace', 'wb') as outfile:
    outfile.write(central_file_contents)

lib = pyne.ace.Library('U235central.ace')
lib.read('92235.01c')
lib.tables
centralU235 = lib.tables['92235.01c']
if chosen_key == "total":
    central_xs = centralU235.sigma_t
    energy = centralU235.energy
else:
    central_xs = centralU235.reactions[reaction_ind].sigma
    spec_reaction = centralU235.reactions[reaction_ind]
    energy = centralU235.energy[spec_reaction.IE:]

filename = f'csv_files/Godiva_{filespec}.csv'
sens_vector_energy, sens_vector_values = np_csvimport.csv_import(filename)
energy *= 1e+06
sens_vec_values_adjusted = np.interp(energy,sens_vector_energy,sens_vector_values)
print(centralU235.energy)
print(np.shape(centralU235.energy))
print(centralU235.energy[:-10])

results_vector = np.zeros(shape = (98,1))
file_indxs = ["01","02","03","04","05","06","07","08","09"] + list(range(10,100))
#for i in file_indxs:
for i in range(9):
    if int(i) == 44:
        continue
    # Navigate to the file within the directory
    #file_path = os.path.join('U235.nuss.10.10.2016', f'U235-n.ace_00{i}')
    file_path = os.path.join('ENDF_to_ACE/processed_ace_files/', f'{i}_AceFile.ace')
    # Open the file and read its contents
    with open(file_path, 'rb') as infile:
        file_contents = infile.read()

    # Write the contents to a new file
    with open('U235.ace', 'wb') as outfile:
        outfile.write(file_contents)

    lib = pyne.ace.Library('U235.ace')
    lib.read('92235.01c')
    lib.tables
    u235 = lib.tables['92235.01c']
    if chosen_key == "total":
        xs = u235.sigma_t
        energy = u235.energy
    else:
        xs = u235.reactions[reaction_ind].sigma
        spec_reaction = u235.reactions[reaction_ind]
        energy = u235.energy[spec_reaction.IE:]
    energy *= 1e+06
    sens_vec_values_adjusted = np.interp(energy,sens_vector_energy,sens_vector_values)
    print(u235.energy)
    print(np.shape(u235.energy))
    print(u235.energy[-10:])
mean = np.mean(results_vector)
std_dev = np.std(results_vector)

# Create a histogram of the vector with 25 bins
plt.hist(results_vector, bins=25, density=True)

# Create a range of x values for the PDF plot
x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)

# Calculate the PDF values for the x values
pdf = 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

# Plot the PDF as a line
plt.plot(x, pdf)

# Set the plot title and axis labels
plt.title(f'delta k_eff {filespec}_xs')
plt.xlabel('Values')
plt.ylabel('Probability Density')

# Show the plot
#plt.show()
plt.savefig(f'results_new_endf2ace/figure_{filespec}.png')
plt.clf()