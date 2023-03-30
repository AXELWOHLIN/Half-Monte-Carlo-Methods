import os
import matplotlib.pyplot as plt
import pyne.ace
import requests
import np_csvimport
from scipy.interpolate import interp2d
from scipy.interpolate import interp1d
import numpy as np

"""
#This is example code from the pyNE documentation for W_180 isotope

url = "https://www-nds.iaea.org/wolfram/w180/beta3/W180.ace"
r = requests.get(url)
with open("W180.ace", "wb") as outfile:
    outfile.write(r.content)

lib = pyne.ace.Library('W180.ace')
lib.read('74180.21c')
lib.tables
w180 = lib.tables['74180.21c']
total_xs = w180.sigma_t
energy = w180.energy
"""

# Navigate to the file within the directory
file_path = os.path.join('U235.nuss.10.10.2016', 'U235-n.ace_0000')

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

print(w180.reactions[2])