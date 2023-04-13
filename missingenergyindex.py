import os
import matplotlib.pyplot as plt
import pyne.ace
import requests
import np_csvimport
from scipy.interpolate import interp2d
from scipy.interpolate import interp1d
import numpy as np
from pyne.rxname import *
from tkinter import Tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
 
aceenergydict = {}

for file in os.scandir('ENDF_to_ACE/processed_ace_files'):
    filename = os.fsdecode(file)
    k = 0
    if ".ace" in filename:
        with open(ace_file0, 'rb') as infile:
            ace_file_contents = infile.read()

            # Write the contents to a new file
        with open('ace_file.ace', 'wb') as outfile:
            outfile.write(ace_file_contents)
        lib = pyne.ace.Library('new_file.ace')
        lib.read('92235.00c')
        lib.tables
        file_contents = lib.tables['92235.00c']
        aceenergydict[k] = [file_contents.energy]
        k =+ 1


plt.plot(aceenergydict[0], aceenergydict[1])
plt.show