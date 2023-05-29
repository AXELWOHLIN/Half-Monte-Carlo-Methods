import os
import matplotlib.pyplot as plt
import pyne.ace
import pyne.rxname as rx
import numpy as np
from pyne.rxname import *
from tkinter import Tk
from tkinter import *
from tkinter import filedialog
from scipy.stats import skew
from scipy.stats import norm, kurtosis

def ace_directory(dir=0):
    """
    Creates a Tkinter root window and prompts the user to choose a directory with ace-files. 
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

def choose_csv(reaction_ind, directory):
    """
    Prompts the user to either choose a sensitivity vector by creating a Tkinter root window or fetch a sensiivity vector
    from a specified textfile generated with Dice. The sensitivity vectors is then saved in one vector with energies and one
    with the corresponding values. The left column in your csv file should contain energies in MeV and your right column the
    sensitivity vector values.  
    Parameters: 
        reaction_ind: an integer that corresponds to the MT number of the reaction type.
    Returns:
        sens_vector_energy: An energy vector for each sensitivity value in eV. 
        sens_vector_values: The corresponding values to the sensitivity energy vector. 
    """
    choice = input('To enter corresponding csv files press "1" otherwise press "2" to generate from dice textfile: ')
    if int(choice) == 1:
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
    elif int(choice) == 2:
        reaction_dict = total_reactions_txt(directory, reaction_ind)
        sens_vector_energy, sens_vector_values = reaction_dict[reaction_ind]
    return sens_vector_energy, sens_vector_values

def total_reactions_txt(directory, reaction_ind):
    """
    Creates a dictionary of sensitivity vectors by fetching data from a Dice texftile. The textfile is read with the help
    of a list of reactions.
    Parameters: 
        none
    Returns:
        sensitivity_dict: A dictionary containing sensitivity vectors with a corresponding energy vectors for each reaction.
    """
    energy_vector = []
    print("\nPlease choose a suitable Dice text file of sensitivity vectors:")
    root = Tk()
    # Hide the main window
    root.withdraw()
    # ask the user to select a file using the filedialog
    text_file_path = filedialog.askopenfilename()
    with open(text_file_path) as f:
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

    for entry in os.scandir(directory):
        if entry.is_file() and ".ace" in entry.name:
            dir_file = entry.path
            break
    with open(dir_file) as f:
        first_line = f.readline()
        first_word = first_line.split('.')[0]

    sensitivity_dict = {}

    sens_vec = []
    with open(text_file_path) as f:
        header_found = False
        correct_header = False
        skip = True
        for line in f:
            if first_word in line and str(reaction_ind) in line.split():
                header_found = True
                correct_header = False
                continue
            elif header_found == True:
                if line.split()[0] == '0':
                    correct_header = True
                header_found = False
            elif correct_header == True and line.startswith(' '):
                if skip==True:
                    f.readline()
                    skip=False
                    continue 
                data = [sens_vec.append(float(x)) for x in line.split()]
            else:   
                header_found = False
    sens_vec = np.array(sens_vec)
    sens_vec = sens_vec[:len(energy_vector)-1]
    sens_vec = np.append(sens_vec, 0.0)
    sensitivity_dict[reaction_ind] =( [energy_vector[::-1],sens_vec[::-1]] )
    return sensitivity_dict

def total_reactions_csv(directory):
    """
    Creates a dictionary containing sensitivity vectors specified through a tkinter prompt window where a csv file is selected. 
    This dictionary represents the reactions which accumulate to the total sensitivity vector. 
    Parameters: 
        directory: A string with the name of the chosen directory of the ace files.
    Returns:
        total_dict: A dictionary containing each reactions sensitivity vector to represent the total sensitivity vector,
    """
    total_dict = {}
    choice = "y"
    print("You will now be prompted to select the available cross sections \
        with their corresponding sensitivity vectors in .csv format to create the \
            total directory \n")
    while choice == "y":
        reaction_ind = choose_reaction(directory, 1)
        sens_vector_energy, sens_vector_values = choose_csv(reaction_ind, directory)
        total_dict[reaction_ind] = (sens_vector_energy, sens_vector_values)
        choice = input("Do you have more sensitivity vectors to add? [y/n]: ")
    return total_dict

def choose_reaction(directory, tot=0):
    """
    Prompts the user to choose a reaction by presenting a series of reactions. The user chooses reaction 
    by typing the corresponding number. It then returns the MT number that corresponds to this reaction. 
    Parameters: 
        directory: A string with the name of the chosen directory of the ace files.
    Returns:
        reaction_ind: An integer that corresponds to the MT number of the reaction type.
    """
    if tot==0:
        #Dictionary of common reactions and the corresponding MT numbers, other can be chosen to use another reaction
        name_dict = {"n,2n":(16),"n,3n":(17),"n,4n":(37) \
                        ,"fission":(18), "elastic":(2) \
                            ,"inelastic":(4), "n,gamma":(102), "prompt,nu":(456), "nubar":(452), "total":(1),"other":("other")}
    else:
        #Dictionary of common reactions and the corresponding MT numbers, other can be chosen to use another reaction
        name_dict = {"n,2n":(16),"n,3n":(17),"n,4n":(37) \
                        ,"fission":(18), "elastic":(2) \
                            ,"inelastic":(4), "n,gamma":(102), "prompt,nu":(456), "nubar":(452),"other":("other")}
    # list all the keys in name_dict
    keys = list(name_dict.keys())

    # prompt the user to choose a key
    print("Choose a reaction:")
    for i, key in enumerate(keys):
        print(f"{i+1}. {key}")
    choice = int(input("Enter the number of the reaction: "))
    if choice == len(name_dict):
        reaction_ind = int(input("Enter the MT number of your desired reaction: "))
        check_mt(directory, reaction_ind) #checks if valid MT number
    else:
    # get the corresponding value based on the user's choice
        chosen_key = keys[choice-1]
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
    """
    Gives the user the alternative to add a reaction to the calculations. 
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
            print("Do you want to specifiy a sensitivity vector for each cross section (.csv) [1] or " \
            "have it be automatically generated from a DICE text file (.txt)? [2] \n")
            total_meth = input("Enter 1 or 2: ")
            while total_meth not in ["1","2"]:
                print("Incorrect usage, please specify '1' or '2'")
                total_meth = input("Enter 1 or 2: ")
            if total_meth == "1":
                total_dictionary = total_reactions_csv(directory)
                reaction_dict[reaction_ind] = total_dictionary 
            elif total_meth == "2":
                choice = "y"
                print("You will now be prompted to select the available cross sections \
                     to create the total directory \n")
                reaction_dict[1] = {}
                while choice == "y":
                    reaction_ind = choose_reaction(directory, 1)
                    total_dictionary = total_reactions_txt(directory, reaction_ind)
                    choice = input("Do you have more reactions to add? [y/n]: ")
                    sens_vector_energy, sens_vector_values = total_dictionary[reaction_ind]
                    reaction_dict[1][reaction_ind] = [sens_vector_energy, sens_vector_values]
        else:
            sens_vector_energy, sens_vector_values = choose_csv(reaction_ind, directory)
            reaction_dict[reaction_ind] = [sens_vector_energy, sens_vector_values]
        choice = input("Do you want to add another reaction? [y/n]: ")
    return reaction_dict

def central_file_decider(directory):
    """
    Decides which file to use as central file. 
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
    """
    Fetches the cross sections from the ACE-files and it's corresponding energy vector. 
    Parameters:  
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
        energy = data.nu_t_energy
    elif reaction_ind == 452:
        xs = data.nu_t_value
        energy = data.nu_t_energy
    else:
        xs = data.reactions[reaction_ind].sigma
        spec_reaction = data.reactions[reaction_ind]
        energy = data.energy[spec_reaction.IE:]
    return xs, energy

def ace_reader(ace_file, directory):
    """
    Reads the ace files. Creates a new file "new_file.ace" to write the file contents of the selected ace file.
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
            if entry.is_file() and ".ace" in entry.name:
                dir_file = entry.path
                break
    with open(dir_file) as f:
        first_line = f.readline()
        first_word = first_line.split()[0]
    lib.read(first_word)
    lib.tables
    
    file_contents = lib.tables[first_word]

    return file_contents

def HMCcalc(reaction_dict, reaction_ind, directory, central_file):
    """
    Calculates the difference in cross section between central and random file for specified reaction. The difference
    is then accumulated for each bin in the sensitivity vectors energy spectrum and multiplied with the total sensitivity
    within each bin.The solution is then returned as a vector where each element represents each file difference in pcm.
    Parameters: 
        reaction_dict: A dictionairy with the MT numbers as keys and the sensitivity vectors as values.
        reaction_ind: An integer that corresponds to the MT number of the reaction type.
        directory: A string with the name of the chosen directory of the ace files.
        central_file: A string with the path to the chosen central file.
    Returns:
        results_vector: A numpy vector consisting of the difference between central file and random files in pcm.
    """
    if int(reaction_ind) == 1:
        results_vector = []
        for reaction_number in reaction_dict[reaction_ind].keys():
            sens_energy, sens_values = reaction_dict[1][reaction_number]
            central_xs, energy = cross_section(reaction_number, central_file, directory)
            bin_avg_central = bin_averager(central_xs, energy, sens_energy)

            for file in os.scandir(directory):
                filename = os.fsdecode(file)
                if filename==central_file:
                    continue
                elif ".ace" in filename:
                    xs, energy = cross_section(reaction_number, filename, directory)
                    bin_avg = bin_averager(xs, energy, sens_energy)
                    delta_k_eff = np.multiply(sens_values, np.array((bin_avg.transpose()-bin_avg_central.transpose())))
                    for k in range(len(bin_avg_central.transpose())):
                        if bin_avg_central.transpose()[k]!=0:
                            delta_k_eff[k]=delta_k_eff[k]/bin_avg_central.transpose()[k]
                        else:
                            delta_k_eff[k]=0
                    delta_k_eff=np.sum(delta_k_eff)
                    results_vector.append(delta_k_eff*1e+05)
                else:
                    continue

        results_matrix = np.array(results_vector).reshape((len(reaction_dict[reaction_ind]),-1))
        results_vector = np.sum(results_matrix, axis=0)
    else:
        results_vector = []
        sens_energy, sens_values = reaction_dict[reaction_ind]
        central_xs, energy = cross_section(reaction_ind, central_file, directory)
        bin_avg_central = bin_averager(central_xs, energy, sens_energy)

        for file in os.scandir(directory):
            filename = os.fsdecode(file)
            if filename==central_file:
                continue
            elif ".ace" in filename:
                xs, energy = cross_section(reaction_ind, filename, directory)
                bin_avg = bin_averager(xs, energy, sens_energy)
                delta_k_eff = np.multiply(sens_values, np.array((bin_avg.transpose()-bin_avg_central.transpose())))
                for k in range(len(bin_avg_central.transpose())):
                    if bin_avg_central.transpose()[k]!=0:
                        delta_k_eff[k]=delta_k_eff[k]/bin_avg_central.transpose()[k]
                    else:
                        delta_k_eff[k]=0
                delta_k_eff=np.sum(delta_k_eff)
                results_vector.append(delta_k_eff*1e+05)
                #print(f"Our scalar is {delta_k_eff}")
            else:
                continue
    return results_vector

def bin_averager(xs, xs_energy, sens_energy):
    """
    Computes the average cross section from vectors of cross section and corresponding energy value with
    the energy bins defined by the sensitivity energy vector.
    Parameters: 
        xs: A vector with all the cross-sections from the chosen reaction.
        xs_energy: A vector of energy values corresponding to each cross section.
        sens_energy: A vector representing 
    Returns:
        bin_avg: A vector of the average cross section within a each energy bin.
    """
    bin_avg = []
    xs_energy = xs_energy*1e+06
    for i in range(len(sens_energy)-1):
        bin_ind = np.where((xs_energy >= sens_energy[i]) & (xs_energy < sens_energy[i+1]))[0]
        if len(bin_ind) != 0:
            bin_avg = np.append(bin_avg, np.mean(xs[bin_ind], axis=0))
        elif i>0:
            bin_avg = np.append(bin_avg, bin_avg[i-1])
        else:
            bin_avg = np.append(bin_avg, 0)
    bin_ind = np.where((xs_energy>= sens_energy[-1]))[0]
    if len(bin_ind) != 0:
        bin_avg = np.append(bin_avg, np.mean(xs[bin_ind], axis=0))
    else:
        bin_avg = np.append(bin_avg, bin_avg[-1])
    return bin_avg

def main():
    print("Please select directory for the ACE-files: ")
    directory = ace_directory()
    reaction_dir = add_reactions(directory)
    reactions_ind = list(reaction_dir.keys())
    central_file=central_file_decider(directory)
    results_dir = 'results/results_new'

    for reaction_ind in reactions_ind:
        results_vector = HMCcalc(reaction_dir, reaction_ind, directory, central_file)
        mean = np.mean(results_vector)
        std_dev = np.std(results_vector)
        kurt = kurtosis(results_vector)
        skewness = skew(results_vector)
        plt.hist(results_vector, bins=25, density=False)

        # Set the plot title and axis labels
        plt.title(r'$\Delta$ $k_{{eff}}$ for ' + 'nubar')
        plt.xlabel(r'$\Delta$ $k_{{eff}}$ (pcm)')
        plt.ylabel('Number of Cases')
        plt.figtext(.65, .85, f"mean = {round(mean,4)}")
        plt.figtext(.65, .8, f"std dev = {round(std_dev,4)}")
        plt.figtext(.65, .75, f"kurtosis = {round(kurt,4)}")
        plt.figtext(.65, .7, f"skewness = {round(skewness,4)}")

        plt.savefig(results_dir+f'/MT_{reaction_ind}_deltakeff.png')
        plt.clf()
        print(f"mean: {mean}")
        print(f"std dev: {std_dev}")
        print(f"skewness: {skewness}")
        print(f"kurtosis: {kurt}")
        if os.path.exists('new_file.ace'):
            os.remove('new_file.ace')
    return mean, std_dev

if __name__ == '__main__':
    main()