import os
import matplotlib.pyplot as plt
import pyne.ace
from pyne.xs import models
import pyne.rxname as rx
import requests
import numpy as np
from pyne.rxname import *
from tkinter import Tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from scipy.stats import skew
from scipy.stats import norm, kurtosis




ace_file = 'U235.nuss.10.10.2016/U235-n.ace_0000'
directory = 'U235.nuss.10.10.2016'

with open(ace_file, 'rb') as infile:
    ace_file_contents = infile.read()

# Write the contents to a new file
with open('new_file.ace', 'wb') as outfile:
    outfile.write(ace_file_contents)
lib = pyne.ace.Library('new_file.ace')
for entry in os.scandir(directory):
        if entry.is_file() and ".xsdir" in entry.name:
            dir_file = entry.path
            break
with open(dir_file) as f:
    first_line = f.readline()
    first_word = first_line.split()[0]
lib.read(first_word)
lib.tables
file_contents = lib.tables[first_word]


reaction = file_contents.reactions
print(file_contents.models.chi())
for key, value in reaction.items():
    mt_number = key
    print(rx.label(int(mt_number)))

if os.path.exists('new_file.ace'):
    os.remove('new_file.ace')
