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
    The left column in your csv file should contain energies in MeV and your right column the sensitivity vector values.  
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
        # ask the user to select a file using the filedialog
        file_path = filedialog.askopenfilename()
    except:
        print("Tkinter is not available. Please enter the file path manually:")
        file_path = input()
    data = np.array(np.loadtxt(file_path, delimiter=','))
    sens_vector_energy = data[:, 0]
    sens_vector_values = data[:, 1]
    return sens_vector_energy, sens_vector_values



def total_reactions_txt():
    name_dict = {'2':'elastic', '4':'inelastic', '16':'n,2n', '17':'n,3n', '18':'fission'}
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
        sens_vec = sens_vec[-len(energy_vector):]
        sensitivity_dict[reaction_ind] =( [energy_vector[::-1],sens_vec[::-1]] )


    return sensitivity_dict

def total_reactions_csv(directory):
    total_dict = {}
    choice = "y"
    print("You will now be prompted to select the available cross sections \
        with their corresponding sensitivity vectors in .csv format to create the \
            total directory \n")
    while choice == "y":
        reaction_ind = choose_reaction(directory)
        sens_vector_energy, sens_vector_values = choose_csv()
        total_dict[reaction_ind] = (sens_vector_energy, sens_vector_values)
        choice = input("Do you have more sensitivity vectors to add? [y/n]: ")
    return total_dict

def choose_reaction(directory):
    """Prompts the user to choose a reaction by presenting a series of reactions. The user chooses reaction 
    by typing the corresponding number. It then returns the MT number that corresponds to this reaction. 
    Parameters: 
        directory: A string with the name of the chosen directory of the ace files.
    Returns:
        reaction_ind: an integer that corresponds to the MT number of the reaction type.
    """
    #Dictionary of common reactions and the corresponding MT numbers, other can be chosen to use another reaction
    name_dict = {"n,2n":(16),"n,3n":(17),"n,4n":(37) \
                    ,"fission":(18), "elastic":(2) \
                        ,"inelastic":(4), "n,gamma":(102), "prompt,nu":(456), "nubar":(452), "total":(1),"other":("other")}

    # list all the keys in name_dict
    keys = list(name_dict.keys())

    # prompt the user to choose a key
    print("Choose a reaction:")
    for i, key in enumerate(keys):
        print(f"{i+1}. {key}")
    choice = input("Enter the number of the reaction: ")
    if int(choice) == 11:
        reaction_ind = int(input("Enter the MT number of your desired reaction: "))
        check_mt(directory, reaction_ind) #checks if valid MT number
    else:
    # get the corresponding value based on the user's choice
        chosen_key = keys[int(choice)-1]
        reaction_ind= int(name_dict[chosen_key])
        return reaction_ind

def check_mt(directory, reaction_ind):
    """
    Checks if the MT number is valid and exists in the ace files.
    Parameters: 
        directory: A string with the name of the chosen directory of the ace files.
        reaction_ind: The MT number.
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
        directory: A string with the name of the chosen directory of the ace files.
    Returns:
        reaction_dict: A dictionairy with the MT numbers as keys and the sensitivity vectors as values. 
    """
    choice = "y"
    reaction_dict = {}
    while choice == "y":
        reaction_ind = choose_reaction(directory)
        if int(reaction_ind) == 1:
            print("Do you want to specifiy a sensitivity vector for each cross section (.csv) [1] or \
              have it be automatically generated from a DICE text file (.txt)? [2] \n")
            total_meth = input("Enter 1 or 2: ")
            while total_meth not in ["1","2"]:
                print("Incorrect usage, please specify '1' or '2'")
                total_meth = input("Enter 1 or 2: ")
            if total_meth == "1":
                total_dictionary = total_reactions_csv(directory) 
            elif total_meth == "2":
                total_dictionary = total_reactions_txt() 
            reaction_dict[reaction_ind] = total_dictionary
        else:
            sens_vector_energy, sens_vector_values = choose_csv()
            reaction_dict[reaction_ind] = [sens_vector_energy, sens_vector_values]
        choice = input("Do you want to add another reaction? [y/n]: ")
    return reaction_dict

def central_file_decider(directory):
    """Decides which file to use as central file. 
    Parameters: 
        directory: A string with the name of the chosen directory of the ace files.
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
        sorted_entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        for entry in sorted_entries:
            if entry.is_file() and ".ace" in entry.name:
                central_file = entry.path
                break
    return central_file

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
    elif reaction_ind == 456:
        xs = data.nu_p_value
        energy_short = data.nu_t_energy
        energy = data.energy
        xs = xs_interp(energy, energy_short, xs)
    elif reaction_ind == 452:
        xs = data.nu_t_value
        energy_short = data.nu_t_energy
        energy = data.energy
        xs = xs_interp(energy, energy_short, xs)
    else:
        xs = data.reactions[reaction_ind].sigma
        spec_reaction = data.reactions[reaction_ind]
        energy = data.energy[spec_reaction.IE:]
    return xs, energy


def xs_interp(sens_energy, energy, xs):
    """Since the vectors are of different size we interpolate them. 
    Parameters: 
        reaction_dict: A dictionairy with the MT numbers as keys and the sensitivity vectors as values. 
        reaction_ind: An integer that corresponds to the MT number of the reaction type.
        energy: A vector with all the energies from the chosen reaction
    Returns:
        sens_vec_values_adjusted: A vector of the same length as the sensitivity vector. 
    """
    xs_values_adjusted = np.interp(sens_energy, energy, xs)
    return  xs_values_adjusted



def sense_interp(reaction_dict, reaction_ind, directory,type):
    """Since the vectors are of different size we interpolate them. 
    Parameters: 
        reaction_dict: A dictionairy with the MT numbers as keys and the sensitivity vectors as values. 
        reaction_ind: An integer that corresponds to the MT number of the reaction type.
        energy: A vector with all the energies from the chosen reaction
    Returns:
        sens_vec_values_adjusted: A vector of the same length as the sensitivity vector. 
    """
    if type == "1":
        xs, energy = cross_section(reaction_ind, ace_file, directory)
        sens_vector_energy, sens_vector_values = reaction_dict[reaction_ind]
        energy *= 1e+06
        sens_vec_values_adjusted = np.interp(sens_vector_energy,energy, xs)
        return  sens_vec_values_adjusted
    elif type == "2":
        sens_vector_energy, sens_vector_values = reaction_dict[reaction_ind]
        energy *= 1e+06
        # Static hold interpolation
        sens_vec_values_adjusted = np.zeros(len(energy))
        for i, e in enumerate(energy):
            idx = np.searchsorted(sens_vector_energy, e) - 1
            if idx < 0:
                idx = 0
            elif idx >= len(sens_vector_values):
                idx = len(sens_vector_values) - 1
            sens_vec_values_adjusted[i] = sens_vector_values[idx]
        return sens_vec_values_adjusted
    else: 
        print("Syntax error, try entering 1 or 2 to choose interp_type!")
        quit()

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

def HMCcalc(reaction_dict, reaction_ind, directory, central_file, interp_type):
    sens_vector_energy, sens_vector_values = reaction_dict[reaction_ind]
    if int(reaction_ind) == 1:
        results_vector = []
        for reaction_number in reaction_dict[reaction_ind].keys():
            central_xs, energy = cross_section(reaction_number, central_file, directory)
            energy *= 1e+06
            central_xs_values_adjusted = xs_interp(sens_vector_energy, energy, central_xs)
            

            for file in os.scandir(directory):
                filename = os.fsdecode(file)
                if filename==central_file:
                    continue
                elif ".ace" in filename:
                    xs, _ = cross_section(reaction_number, filename, directory)
                    xs_values_adjusted = xs_interp(sens_vector_energy, energy, xs)
                    delta_k_eff = np.multiply(np.array(sens_vector_values),np.array((xs_values_adjusted.transpose()-central_xs_values_adjusted.transpose())))
                    for k in range(len(central_xs_values_adjusted.transpose())):
                        if central_xs_values_adjusted.transpose()[k]!=0:
                            delta_k_eff[k]=delta_k_eff[k]/central_xs_values_adjusted.transpose()[k]
                        else:
                            delta_k_eff[k]=0
                    delta_k_eff=np.sum(delta_k_eff)
                    results_vector.append(delta_k_eff)
                    #print(f"Our scalar is {delta_k_eff}")
                else:
                    continue

        results_matrix = np.array(results_vector).reshape((len(reaction_dict[reaction_ind]),-1))
        results_vector = np.sum(results_matrix, axis=0)
    else:
        results_vector = []

        sens_vector_energy, sens_vector_values = reaction_dict[reaction_ind]
        central_xs, energy = cross_section(reaction_ind, central_file, directory)
        energy *= 1e+06
        central_xs_values_adjusted = xs_interp(sens_vector_energy, energy, central_xs)

        for file in os.scandir(directory):
                filename = os.fsdecode(file)
                if filename==central_file:
                    continue
                elif ".ace" in filename:
                    xs, _ = cross_section(reaction_ind, filename, directory)
                    xs_values_adjusted = xs_interp(sens_vector_energy, energy, xs)
                    delta_k_eff = np.multiply(np.array(sens_vector_values),np.array((xs_values_adjusted.transpose()-central_xs_values_adjusted.transpose())))
                    for k in range(len(central_xs_values_adjusted.transpose())):
                        if central_xs_values_adjusted.transpose()[k]!=0:
                            delta_k_eff[k]=delta_k_eff[k]/central_xs_values_adjusted.transpose()[k]
                        else:
                            delta_k_eff[k]=0
                    delta_k_eff=np.sum(delta_k_eff)
                    results_vector.append(delta_k_eff)
                    #print(f"Our scalar is {delta_k_eff}")
                else:
                    continue
    return results_vector


def choose_interpolation():
    print("Linear interpolation == 1\
    \n Static hold interplation == 2")
    interp_type = input("What type of interpolation do you want to use for the sensitivity vector?: ")
    return interp_type

def main():
    directory = ace_directory()
    reaction_dir = add_reactions(directory)
    reactions_ind = list(reaction_dir.keys())
    central_file=central_file_decider(directory)
    interp_type = choose_interpolation()
    
    for reaction_ind in reactions_ind:
        results_vector = HMCcalc(reaction_dir, reaction_ind, directory, central_file, interp_type)
        mean = np.mean(results_vector)
        std_dev = np.std(results_vector)
        kurt = kurtosis(results_vector)
        skewness = skew(results_vector)
        plt.hist(results_vector, bins=25, density=False)

        # Set the plot title and axis labels
        plt.title(f'% delta k_eff {reaction_ind}_xs')
        plt.xlabel('% delta k_eff')
        plt.ylabel('Number of Cases')
        plt.figtext(.65, .85, f"mean = {round(mean,4)}")
        plt.figtext(.65, .8, f"std dev = {round(std_dev,4)}")
        plt.figtext(.65, .75, f"kurtosis = {round(kurt,4)}")
        plt.figtext(.65, .7, f"skewness = {round(skewness,4)}")

        if interp_type == "1":
            plt.savefig(f'result_plots_linear_interp/figure_{reaction_ind}.png')
        elif interp_type == "2":
            plt.savefig(f'result_plots_static_interp/figure_{reaction_ind}.png')
        plt.clf()
        print(f"mean: {mean}")
        print(f"std dev: {std_dev}")
        print(f"skewness: {skewness}")
        print(f"kurtosis: {kurt}")
    return mean, std_dev

if __name__ == '__main__':
    main()










