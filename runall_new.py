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
from tkinter import filedialog
from tkinter.filedialog import askopenfilename


def ace_directory(dir=0):
    if dir == 0:
        print("Choose a suitable directory with ace files!")
        root = Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        print("Selected directory: ", directory)
    else:
        directory = dir
    return directory 

def csv_files():
    print("\nPlease choose a sensitivity vector in .csv format:")
    # Create a Tkinter root window to prompt user to choose sensitivity vector
    root = Tk()
    # Hide the main window
    root.withdraw()
    # Show the file dialog and get the selected file
    filename = askopenfilename()
    sens_vector_energy, sens_vector_values = np_csvimport.csv_import(filename)
    return sens_vector_energy, sens_vector_values

def choose_reaction():
    #First number is MT and second is filename
    name_dict = {"n,2n":("2n","n_2n"),"n,3n":("z_3n","n_3n"),"n,4n":("z_4n","n_4n") \
                    ,"fission":("fission","fission"), "elastic":("elastic","elastic") \
                        ,"inelastic":("inelastic","inelastic"),"total":("total","total")}

    # list all the keys in name_dict
    keys = list(name_dict.keys())

    # prompt the user to choose a key
    print("Choose a reaction:")
    for i, key in enumerate(keys):
        print(f"{i+1}. {key}")
    choice = input("Enter the number of the reaction: ")

    # get the corresponding value based on the user's choice
    chosen_key = keys[int(choice)-1]
    mt_number,filespec, = name_dict[chosen_key]
    # use the filename and mt_number variables to do further processing

    reaction_ind = mt(mt_number)
    return(reaction_ind)

def add_reactions():
    choice = "y"
    reaction_dict = {}
    while choice == "y":
        reaction_ind = choose_reaction()
        sens_vector_energy, sens_vector_values = csv_files()
        reaction_dict[reaction_ind] = [sens_vector_energy, sens_vector_values]
        choice = input("Do you want to add another reaction? [y/n]: ")
    return reaction_dict

def central_file_decider(directory):
    choice = input("Do you want to choose central file? [y/n]: ")
    if choice == "y":
        # Create a Tkinter root window to prompt user to choose sensitivity vector
        root = Tk()
        # Hide the main window
        root.withdraw()
        # Show the file dialog and get the selected file
        central_file = askopenfilename()
    elif choice == "n":
        for entry in os.scandir(directory):
            if entry.is_file() and ".ace" in entry.name:
                central_file = entry
                break
    return central_file




def sense_interp(reaction_dict, reaction_ind , ace_file):
    
    centralU235 = ace_reader(ace_file)
    
    if reaction_ind == 1:
        xs = centralU235.sigma_t
        energy = centralU235.energy
    else:
        xs = centralU235.reactions[reaction_ind].sigma
        spec_reaction = centralU235.reactions[reaction_ind]
        energy = centralU235.energy[spec_reaction.IE:]
        
    sens_vector_energy, sens_vector_values = reaction_dict[reaction_ind]
    energy *= 1e+06
    sens_vec_values_adjusted = np.interp(energy,sens_vector_energy,sens_vector_values)
    return  sens_vec_values_adjusted, xs




def ace_reader(ace_file):
    file_path = os.path.join('U235.nuss.10.10.2016', ace_file)
    with open(file_path, 'rb') as infile:
        ace_file_contents = infile.read()

    # Write the contents to a new file
    with open('U235central.ace', 'wb') as outfile:
        outfile.write(ace_file_contents)

    lib = pyne.ace.Library('U235central.ace')
    lib.read('92235.00c')
    lib.tables
    centralU235 = lib.tables['92235.00c']
    
    return centralU235



def HMCcalc(reaction_dict, reaction_ind, directory):
    results_vector = []
    
    central_file = central_file_decider(directory)
    _, central_xs = sense_interp(reaction_dict, reaction_ind, central_file)
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if ".ace" in filename:
            sens_vec_values_adjusted, xs = sense_interp(reaction_dict, reaction_ind, filename)
            tmp = np.dot(sens_vec_values_adjusted,(xs.transpose()-central_xs.transpose()))
            results_vector.append(tmp)
            #print(f"Our scalar is {tmp}")
        else:
            continue
    
    
    
    return results_vector


def main():
    directory = ace_directory()
    reaction_dir = add_reactions()
    reactions_ind = list(reaction_dir.keys())
    
    for reaction_ind in reactions_ind:
        results_vector = HMCcalc(reaction_dir, reaction_ind, directory)
        
        
        mean = np.mean(results_vector)
        std_dev = np.std(results_vector)

        plt.hist(results_vector, bins=25, density=False)

        # Set the plot title and axis labels
        plt.title(f'delta k_eff {reaction_ind}_xs')
        plt.xlabel('Values')
        plt.ylabel('Number of Cases')
        plt.figtext(.8, .8, f"mean = {round(mean,4)}")
        plt.figtext(.8, .5, f"std dev = {round(std_dev,4)}")

        plt.savefig(f'result_plots/figure_{reaction_ind}.png')
        plt.clf()
        
    return mean, std_dev

if __name__ == '__main__':
    main()