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


total_reactions_txt()