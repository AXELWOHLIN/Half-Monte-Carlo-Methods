import os
import matplotlib.pyplot as plt
import pyne.ace
import numpy as np
from pyne.rxname import *
from tkinter import Tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import csv



def total_reactions_txt(reaction_dict):
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
    for reaction_ind, reaction_name  in reaction_dict.items():
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
        sens_vec = sens_vec[-len(energy_vector):]
        sensitivity_dict[reaction_ind] =( [energy_vector[::-1],sens_vec[::-1]] )


    return sensitivity_dict


reaction_dict = {'2':'elastic', '4':'inelastic', '16':'n,2n', '17':'n,3n', '18':'fission'}

sensitivity_dict = total_reactions_txt(reaction_dict)

print(sensitivity_dict)