import openmc
import os

filename = "ENDF_processing/N_ELMT2.txt"
endfds = openmc.data.endf.Evaluation(filename)
print(endfds.target)
print(endfds.reaction_list)
print(dir(endfds))
#rint(endfds.section)

filename = 'ENDF_processing/ENDF_test.bin'
with open(filename, 'rb') as file:
    # Pass the file object to get_intg_record() function
    majd = openmc.data.endf.get_intg_record(file)
