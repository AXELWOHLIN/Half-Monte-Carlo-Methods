import os
import matplotlib.pyplot as plt
import pyne.ace
import requests
import numpy as np
from pyne.rxname import *
from tkinter import Tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from scipy.stats import skew
from scipy.stats import norm, kurtosis




directory = 'U235.nuss.10.10.2016'


def cross_section(reaction_ind, ace_file, directory):
    """Picks out the cross sections from the ACE-files. 
    Parameters: 
        reaction_dict: A dictionairy with the MT numbers as keys and the sensitivity vectors as values. 
        reaction_ind: An integer that corresponds to the MT number of the reaction type.
        ace_file: A string with the name of the specific ACE-file.
        directory: A string with the name of the chosen directory of the ace files.
    Returns:
        xs: A vector with all the cross-sections from the chosen reaction.
        energy: A vector with all the energies from the chosen reaction.
    """
    data = ace_reader(ace_file, directory)
    reaction_ind = int(reaction_ind)
    if reaction_ind == 1:
        xs = data.sigma_t
        energy = data.energy
    else:
        xs = data.reactions[reaction_ind].sigma
        spec_reaction = data.reactions[reaction_ind]
        energy = data.energy[spec_reaction.IE:]
    return xs, energy


def ace_reader(ace_file, directory):
    """Reads the ace files. Creates a new file "new_file.ace" to write the file contents of the selected ace file.
    Only files with .ace in the filename is considered. A .xsdir file is needed to determine the used element. 
    Parameters: 
        ace_file: A string with the name of the specific ACE-file.
        directory: A string with the name of the chosen directory.
    Returns:
        file_contents: 
    """
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

    return file_contents


name_dict = {"n,2n":(16),"n,3n":(17),"n,4n":(37) \
                ,"fission":(18), "elastic":(2) \
                    ,"inelastic":(4), "n,gamma":(102) ,"total":(1)}

plot_dict = {}
file_dict = {}
i = 0
n = 0

for reaction_ind in name_dict.values():
    n = 0
    for file in os.scandir(directory):
        filename = os.fsdecode(file)
        if ".ace" in filename:
            xs, energy = cross_section(reaction_ind, filename, directory)
            file_dict[n] = ([xs, energy])
            n += 1
            print(n)
            
    plot_dict[i] = file_dict
    i += 1
    print(i)

print(len(plot_dict))
print(len(file_dict))