import requests
from pyne.xs.data_source import ENDFDataSource
from pyne import nucname
from os.path import isfile
import os
import requests    
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from tabulate import tabulate
from pyne.endf import Library, Evaluation

filename = "ENDF_processing/1_2_4_16_17_18_102.txt"
with open(filename, "rb") as infile:
    content = infile.read()
    with open("ENDF_processing/covar_test.bin", "rb") as outfile:
        #outfile.write(content)
        endfds = Evaluation(outfile)
        majd = endfds.read( reactions = (30,2))
        mike = endfds.read( reactions = (1,451))


print(majd)
print(mike)