import numpy as np

file = 'csv_files/Godiva_total.csv'
# Load data from CSV file
def csv_import(filename):
    """
    Args: Filename as string
    Returns Energy np.array, k_sensitvity np.array
    """
    data = np.array(np.loadtxt(file, delimiter=','))
    energy_eV = data[:, 0]
    k_sensitivity = data[:, 1]
    return energy_eV,k_sensitivity
