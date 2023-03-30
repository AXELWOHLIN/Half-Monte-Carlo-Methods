import os
import matplotlib.pyplot as plt
import pyne.ace
import requests
import np_csvimport
from scipy.interpolate import interp2d
from scipy.interpolate import interp1d
import numpy as np

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
central_total_xs = centralU235.sigma_t


results_vector = np.zeros(shape = (98,1))
file_indxs = ["01","02","03","04","05","06","07","08","09"] + list(range(10,100))
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

    filename = 'csv_files/Godiva_total.csv'
    sens_vector_energy, sens_vector_values = np_csvimport.csv_import(filename)
    energy *= 1e+06

    sens_vec_values_adjusted = np.interp(energy,sens_vector_energy,sens_vector_values)
    tmp = np.dot(sens_vec_values_adjusted,(total_xs.transpose()-central_total_xs.transpose()))
    if int(i)>=44:
        results_vector[int(i)-2,0] = tmp
    else:
        results_vector[int(i)-1,0] = tmp
    print(f"Our scalar is {tmp}")

mean = np.mean(results_vector)
std_dev = np.std(results_vector)

# Create a histogram of the vector with 10 bins
plt.hist(results_vector, bins=25, density=True)

# Create a range of x values for the PDF plot
x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)

# Calculate the PDF values for the x values
pdf = 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

# Plot the PDF as a line
plt.plot(x, pdf)

# Set the plot title and axis labels
plt.title('k_eff ')
plt.xlabel('Values')
plt.ylabel('Probability Density')

# Show the plot
plt.show()