import openmc
import math
import os
import numpy as np
import matplotlib.pyplot as plt

filename = "ENDF_to_ACE/endf_test_2/n-W180-rand-0000"
output_directory = "ENDF_to_ACE/processed_ace_files"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

input_directory = "ENDF_to_ACE/u235_ENDF_test"
for i, filename in enumerate(os.listdir(input_directory)):
    openmc.data.njoy.make_ace(input_directory+"/"+filename, 
                            output_dir=output_directory,
                            acer="ENDF_to_ACE/processed_ace_files/{i}_AceFile",
                            error=0.001)