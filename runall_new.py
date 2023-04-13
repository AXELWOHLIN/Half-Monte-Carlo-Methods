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


def ace_directory(dir=0):
    """Creates a Tkinter root window and prompts the user to choose a directory with ace-files. 
    Parameters: 
        dir=0: Automatically jumps to "Choose a suitable directory with ace files"
    Returns:
        directory: A string with the chosen directory. 
    """
    if dir==0:
        try:
            root = Tk()
            root.withdraw()
            directory = filedialog.askdirectory()
            print("Selected directory: ", directory)
        except:
            print("Tkinter is not available. Please enter the directory path manually:")
            directory = input()
        return directory
    else:
        directory = dir
    return directory

def choose_csv():
    """Prompts the user to choose a sensitivity vector by creating a Tkinter root window.
    The sensitivity vectors is then saved in one vector with energies and one with the corresponding values.  
    Parameters: 
        none
    Returns:
        sens_vector_energy: a sensitivity vector in eV 
        sens_vector_values: The corresponding values to the sensitivity vector 
    """
    try:
        print("\nPlease choose a sensitivity vector in .csv format:")
        root = Tk()
        # Hide the main window
        root.withdraw()
        # Show the file dialog and get the selected file
        filename = filedialog.askopenfilename()
    except:
        print("Tkinter is not available. Please enter the file path manually:")
        filename = input()
    sens_vector_energy, sens_vector_values = np_csvimport.csv_import(filename)
    return sens_vector_energy, sens_vector_values

def choose_reaction(directory):
    """Prompts the user to choose a reaction by presenting a series of reactions. The user chooses reaction 
    by typing the corresponding number. It then returns the MT number that corresponds to this reaction. 
    Parameters: 
        none
    Returns:
        reaction_ind: an integer that corresponds to the MT number of the reaction type.
    """
    #Dictionary of common reactions and the corresponding MT numbers, other can be chosen to use another reaction
    name_dict = {"n,2n":(16),"n,3n":(17),"n,4n":(37) \
                    ,"fission":(18), "elastic":(2) \
                        ,"inelastic":(4),"total":(1),"other":("other")}

    # list all the keys in name_dict
    keys = list(name_dict.keys())

    # prompt the user to choose a key
    print("Choose a reaction:")
    for i, key in enumerate(keys):
        print(f"{i+1}. {key}")
    choice = input("Enter the number of the reaction: ")
    if int(choice) == 8:
        reaction_ind = int(input("Enter the MT number of your desired reaction: "))
        check_mt(directory, reaction_ind) #checks if valid MT number
    else:
    # get the corresponding value based on the user's choice
        chosen_key = keys[int(choice)-1]
        reaction_ind= int(name_dict[chosen_key])
    return reaction_ind

def check_mt(directory, reaction_ind):
    """
    Parameters: 
        none
    Returns:
        reaction_ind: an integer that corresponds to the MT number of the reaction type.
    """
    for entry in os.scandir(directory):
            if entry.is_file() and ".ace" in entry.name:
                central_file = entry.path
                break
    ace_check = ace_reader(central_file, directory)
    if reaction_ind in ace_check.reactions:
        return
    else:
        print("MT number not found in corresponding ace files!")
        quit()
    return 

def add_reactions(directory):
    """Gives the user the alternative to add a reaction to the calculations. 
    Parameters: 
        none
    Returns:
        reaction_dict: A dictionairy with the MT numbers as keys and the sensitivity vectors as values. 
    """
    choice = "y"
    reaction_dict = {}
    while choice == "y":
        reaction_ind = choose_reaction(directory)
        sens_vector_energy, sens_vector_values = choose_csv()
        reaction_dict[reaction_ind] = [sens_vector_energy, sens_vector_values]
        choice = input("Do you want to add another reaction? [y/n]: ")
    return reaction_dict

def central_file_decider(directory):
    """Decides which file to use as central file. 
    Parameters: 
        directory: A string with the name of the chosen directory.
    Returns:
        central file: A string with the name of the chosen central file.
    """
    choice = input("Do you want to choose central file? [y/n]: ")
    if choice == "y":
        try:
            # Create a Tkinter root window to prompt user to choose central file
            root = Tk()
            # Hide the main window
            root.withdraw()
            # Show the file dialog and get the selected file
            central_file = filedialog.askopenfilename()
        except:
            print("Tkinter is not available. Please enter the file path manually:")
            central_file = input()
    elif choice == "n":
        for entry in os.scandir(directory):
            if entry.is_file() and ".ace" in entry.name:
                central_file = entry.path
                break
    return central_file


def cross_section(reaction_dict, reaction_ind, ace_file, directory):
    """Picks out the cross sections from the ACE-files. 
    Parameters: 
        reaction_dict: A dictionairy with the MT numbers as keys and the sensitivity vectors as values. 
        reaction_ind: An integer that corresponds to the MT number of the reaction type.
        ace_file: A string with the name of the specific ACE-file.
        directory: A string with the name of the chosen directory.
    Returns:
        xs: A vector with all the cross-sections from the chosen reaction.
        energy: A vector with all the energies from the chosen reaction.
    """
    data = ace_reader(ace_file, directory)
    if reaction_ind == 1:
        xs = data.sigma_t
        energy = data.energy
    else:
        xs = data.reactions[reaction_ind].sigma
        spec_reaction = data.reactions[reaction_ind]
        energy = data.energy[spec_reaction.IE:]
    return xs, energy

def sense_interp(reaction_dict, reaction_ind, energy):
    """Since the vectors are of different size we interpolate them. 
    Parameters: 
        reaction_dict: A dictionairy with the MT numbers as keys and the sensitivity vectors as values. 
        reaction_ind: An integer that corresponds to the MT number of the reaction type.
        energy: A vector with all the energies from the chosen reaction
    Returns:
        sens_vec_values_adjusted: A vector of the same length as the sensitivity vector. 
    """
    sens_vector_energy, sens_vector_values = reaction_dict[reaction_ind]
    energy *= 1e+06
    sens_vec_values_adjusted = np.interp(energy,sens_vector_energy,sens_vector_values)
    return  sens_vec_values_adjusted


def ace_reader(ace_file, directory):
    """Fortsätt dokumentera här. 
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



def HMCcalc(reaction_dict, reaction_ind, directory, ace_file):
    results_vector = []

    central_xs, energy = cross_section(reaction_dict, reaction_ind, ace_file, directory)
    sens_vec_values_adjusted = sense_interp(reaction_dict, reaction_ind, energy)
    
    for file in os.scandir(directory):
        filename = os.fsdecode(file)
        if ".ace" in filename:
            xs, _ = cross_section(reaction_dict, reaction_ind, filename, directory)
            delta_k_eff = np.dot(sens_vec_values_adjusted,(xs.transpose()-central_xs.transpose()))
            results_vector.append(delta_k_eff)
            #print(f"Our scalar is {delta_k_eff}")
        else:
            continue
    return results_vector

def main():
    directory = ace_directory()
    reaction_dir = add_reactions(directory)
    reactions_ind = list(reaction_dir.keys())
    central_file=central_file_decider(directory)
    
    for reaction_ind in reactions_ind:
        results_vector = HMCcalc(reaction_dir, reaction_ind, directory, central_file)
        
        
        mean = np.mean(results_vector)
        std_dev = np.std(results_vector)

        plt.hist(results_vector, bins=25, density=False)

        # Set the plot title and axis labels
        plt.title(f'delta k_eff {reaction_ind}_xs')
        plt.xlabel('Values')
        plt.ylabel('Number of Cases')
        plt.figtext(.65, .8, f"mean = {round(mean,7)}")
        plt.figtext(.65, .7, f"std dev = {round(std_dev,7)}")

        plt.savefig(f'result_plots/figure_{reaction_ind}.png')
        plt.clf()
        print(mean)
        print(std_dev)
    return mean, std_dev

if __name__ == '__main__':
    main()