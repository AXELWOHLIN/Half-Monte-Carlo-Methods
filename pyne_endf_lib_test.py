


import os
import requests    
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from pyne.endf import Library, Evaluation

with open("sens_textfiles/HEU-MET-FAST-001-001_MCNP_ENDF-B-VII.0-Continuous_SENS.txt", 'rb') as infile:
    endf_file_contents = infile.read()

# Write the contents to a new file
with open('new_file_endf.endf', 'wb') as outfile:
    outfile.write(endf_file_contents)
lib = Evaluation('new_file_endf.endf')
xs_data = lib.get_xs(922350000, 16)[0]

