import numpy as np

# Load data from CSV file
data = np.array(np.loadtxt('csv_files/totalgodiva-Sheet1.csv', delimiter=','))

# Split the data into two separate arrays
energy_eV = data[:, 0]
k_sensitivity = data[:, 1]

print(energy_eV)
