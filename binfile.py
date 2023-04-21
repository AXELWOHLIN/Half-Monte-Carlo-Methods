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
ace_file = 'U235.nuss.10.10.2016/U235-n.ace_0000'


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


def total_reactions_txt():
    name_dict = {'2':'elastic', '4':'inelastic', '16':'n,2n', '17':'n,3n', '18':'fission','452':'nubar','456':'prompt,nu', '102':'n,gamma'}
    energy_vector = []

    with open('csv_files/HEU-MET-FAST-001-001_MCNP_ENDF-B-VII.0-Continuous_SENS.txt') as f:
        header_found = False
        for line in f:
            if 'energy' in line:
                header_found = True
                continue
            else:
                if header_found == True and line.startswith(' '):
                    data = [energy_vector.append(float(x)) for x in line.split()]
                else:   
                    header_found = False

    energy_vector = np.array(energy_vector)

    first_word = '92235'
    sensitivity_dict = {}
    for reaction_ind, reaction_name  in name_dict.items():
        sens_vec = []
        with open('csv_files/HEU-MET-FAST-001-001_MCNP_ENDF-B-VII.0-Continuous_SENS.txt') as f:
            header_found = False
            for line in f:
                if first_word in line and reaction_ind in line and reaction_name in line:
                    header_found = True
                    continue
                else:
                    if header_found == True and line.startswith(' '):
                        data = [sens_vec.append(float(x)) for x in line.split()]
                    else:   
                        header_found = False
        sens_vec = np.array(sens_vec)
        sens_vec = sens_vec[11:(len(energy_vector)+10)]
        sens_vec = np.append(sens_vec,0)
        sensitivity_dict[reaction_ind] =( [energy_vector[::-1],sens_vec[::-1]] )


    return sensitivity_dict



def bin_averager(xs, xs_energy, sens_energy):
    bin_avg = []
    bin_plot = []
    for i in range(len(sens_energy)-1):
        bin_ind = np.where((xs_energy >= sens_energy[i]) & (xs_energy < sens_energy[i+1]))[0]
        print(bin_ind)   
        if len(bin_ind) != 0:
            bin_avg = np.append(bin_avg, np.mean(xs[bin_ind], axis=0))
        elif i>0:
            bin_avg = np.append(bin_avg, bin_avg[i-1])
        else:
            bin_avg = np.append(bin_avg, 0)
    return bin_avg, bin_plot

reaction = '17'

xs, xs_energy = cross_section(int(reaction), ace_file, directory)
xs_energy = xs_energy*10e6
ind_e = np.where(xs_energy == 2e6)[0][0] 
print(ind_e)
xs_avg = np.mean(xs[0])
sens_dict = total_reactions_txt()
sens_energy, _ = sens_dict[reaction]
print(xs_energy[ind_e]==sens_energy[-1])
print(sens_energy[-20:])
bin_averages, bin_plot = bin_averager(xs, xs_energy, sens_energy)
y_values = sens_energy[:-1]

x_values = bin_averages


plt.loglog(y_values, x_values)
plt.show()
