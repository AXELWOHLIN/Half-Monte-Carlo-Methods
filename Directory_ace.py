import os
import matplotlib.pyplot as plt
import pyne.ace
import requests
import np_csvimport
from scipy.interpolate import interp2d
from scipy.interpolate import interp1d
import numpy as np
from pyne.rxname import *
import tkinter as tk
from tkinter import filedialog

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
mt_number,filespec, = name_dict[chosen_key]
# use the filename and mt_number variables to do further processing

reaction_ind = mt(mt_number)

central_file_name = os.path.join('U235.nuss.10.10.2016', f'U235-n.ace_0000')
with open(central_file_name, 'rb') as infile:
    central_file_contents = infile.read()

    # Write the contents to a new file
with open('U235central.ace', 'wb') as outfile:
    outfile.write(central_file_contents)

lib = pyne.ace.Library('U235central.ace')
lib.read('92235.00c')
lib.tables
centralU235 = lib.tables['92235.00c']
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


#Following is changed and should make a function on its own
print("Choose a suitable directory with ace files!")
root = tk.Tk()
root.withdraw()
directory = filedialog.askdirectory()
print("Selected directory: ", directory)
results_vector = []
#directory = os.fsencode('U235.nuss.10.10.2016')

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if ".ace" in filename:
         # Navigate to the file within the directory
        file_path = os.path.join('U235.nuss.10.10.2016', filename)
         # Open the file and read its contents
        with open(file_path, 'rb') as infile:
            file_contents = infile.read()

        # Write the contents to a new file
        with open('U235.ace', 'wb') as outfile:
            outfile.write(file_contents)

        lib = pyne.ace.Library('U235.ace')
        lib.read('92235.00c')
        lib.tables
        u235 = lib.tables['92235.00c']
        if chosen_key == "total":
            xs = u235.sigma_t
        else:
            xs = u235.reactions[reaction_ind].sigma
        energy = u235.energy


        tmp = np.dot(sens_vec_values_adjusted,(xs.transpose()-central_xs.transpose()))
        results_vector.append(tmp)
        print(f"Our scalar is {tmp}")
    else:
        continue
    

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
plt.show()
print(f"Standard deviation is: {std_dev}")