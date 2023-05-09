# Axel, Olle, Tyra, Viktor's project

# Introduction:
This repository is a bachelors project with a aim to produce a generalized python script able to compute Half Monte Carlo calculation for error propagation of 
criticality in integral experiments. The Half Monte Carlo calculation is done with a combination of sensitivity vectors preferrably given by the Dice library 
and a suitable collection of randomfiles in ace format. Although the results will stand more correct when the sensitivity vector and randomfiles come from
the same library the script will still be able to produce a result when they are not.


# Installations:
* If you want to use the files using ENDFtk for ENDF file processing, see here for an installation tutorial: https://github.com/njoy/ENDFtk/blob/master/README.md
* The scripts found in this repository have an requirement of the PyNE module which installation instructions can be found on the pyne website: https://pyne.io/

# Scripts:
## bin_sol.py:
The python script used for the calculation of the error propagation is "bin_sol.py". To run the script properly a suitable collection of ace randomfiles and
sensitivity vectors corresponding to the desired reaction is required.
1. The script when run will open a window and prompt the user to select a directory where
the utilized randomfiles are.
2. It will then propose a list of reactions, whereas the last option is to manually add a reaction. The so called "other" option
in the reaction list will print an error message if the entered reaction is not included in the given ace randomfiles.
3. The user is then required to either propose corresponding sensivity vector for the reaction in the shape of either a csvfile or a textfile generated from
dice where the script wants the total sensitivity within bin.
4. After the user is given a option to add further reactions in the same run which will be formatted the same way as previous additions.
5. Finally the user is given the option to manually select the central ace file otherwise the first file in the directory will be automatically selected.

### In the case of total:
The total reaction is not calculated as the others but is instead a summation of several reactions, ideally all of them, although due to difference in libraries
between the randomfiles and Dice there will be reaction not found in both or either of them. Therefore the user will be prompted to manually add reactions like
previously mentioned for the calculation of several reactions. It's important here if you choose to import sensitivity vectors from csv files that the correct
csv file is chosen after every addition of a reaction.

### Example:
To calculate the error propagation for fission the terminal can look like this:
```
Choose a reaction:
1. n,2n
2. n,3n
3. n,4n
4. fission
5. elastic
6. inelastic
7. n,gamma
8. prompt,nu
9. nubar
10. total
11. other
Enter the number of the reaction: 4
To enter corresponding csv files press "1" otherwise press "2" to generate from dice textfile: 1
Please choose a sensitivity vector in .csv format:
Do you want to add another reaction? [y/n]: n
Do you want to choose central file? [y/n]: n
```
After a brief calculation the script will produce an output:
```
mean: 2.0078138155942216
std dev: 264.73216695302557
skewness: 0.060316093916077784
kurtosis: -0.10883104489764595
```
The script will also produce a graph:
![Graph for delta_k_eff in pcm for each randomfile](result_plots_binavg/figure_4.png)
# Conclusion:
We hope this readme.md and the scripts found in the repository will be useful. Thank you.

TYRA