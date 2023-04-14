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


edict = {}
k = 0
for file in os.scandir('ENDF_to_ACE/olle_mike_hawk'):
    filename = os.fsdecode(file)
    if ".ace" in filename:
        with open(filename, 'rb') as infile:
            ace_file_contents = infile.read()

            # Write the contents to a new file
        with open('ace_file.ace', 'wb') as outfile:
            outfile.write(ace_file_contents)
        lib = pyne.ace.Library('ace_file.ace')
        lib.read('74180.01c')
        lib.tables
        file_contents = lib.tables['74180.01c']
        edict[k] = [file_contents.energy, file_contents.sigma_t]
        k += 1

e0, t0 = edict[0]
e1, t1 = edict[1]


""""
b = 0
for i in range(len(e0)):
    if e0[i]==e1[i]:
        continue
    elif b>20:
        break
    else:
    
        print()
        print(e0[i])
        print(i)
        print(e1[i])
        print()
        b += 1
"""

diff = len(e1) - len(e0)
"""
# Append zeros to the shorter array
if diff > 0:
    e0 = np.append(e0, np.zeros(diff))
else:
    e1 = np.append(e1, np.zeros(abs(diff)))
"""

plt.loglog(e1, t1)
plt.show()