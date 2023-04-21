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

filename = "ENDF_processing/N_ELMT2.txt"
with open(filename, "rb") as infile:
    content = infile.read()
    with open("ENDF_processing/covar_test.bin", "wb") as outfile:
        outfile.write(content)
        with open("ENDF_processing/covar_test.bin", "rb") as outfile:
            #outfile.write(content)      
            endfds = Evaluation(outfile)
            print(endfds.target)
            print(endfds.reaction_list)
            print(endfds.read(reactions=(33,2)))