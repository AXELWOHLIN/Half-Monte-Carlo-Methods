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
for file in os.scandir('U235.nuss.10.10.2016'):
    filename = os.fsdecode(file)
    if ".ace" in filename:
        with open(filename, 'rb') as infile:
            ace_file_contents = infile.read()

            # Write the contents to a new file
        with open('ace_file.ace', 'wb') as outfile:
            outfile.write(ace_file_contents)
        lib = pyne.ace.Library('ace_file.ace')
        lib.read('92235.00c')
        lib.tables
        file_contents = lib.tables['92235.00c']
        edict[k] = file_contents.energy
        k += 1

e0 = edict[5]
e1 = edict[3]
e2 = edict[2]

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


diff = len(e1) - len(e0)

# Append zeros to the shorter array
if diff > 0:
    e0 = np.append(e0, np.zeros(diff))
else:
    e1 = np.append(e1, np.zeros(abs(diff)))


plt.loglog(e0, e1)
plt.show()