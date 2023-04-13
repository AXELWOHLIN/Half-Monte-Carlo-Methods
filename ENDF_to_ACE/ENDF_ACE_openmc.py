import openmc
import math
import os
import numpy as np
import matplotlib.pyplot as plt

filename = "ENDF_to_ACE/endf_test_2/n-W180-rand-0000"
output_directory = "ENDF_to_ACE/olle_mike_hawk"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

input_directory = "ENDF_to_ACE/endf_test_2"
for i, filename in enumerate(os.listdir(input_directory)):
    openmc.data.njoy.make_ace(input_directory+"/"+filename, 
                            output_dir=output_directory,
                            acer="ENDF_to_ACE/olle_mike_hawk/{i}_AceFile",
                            error=0.00001)