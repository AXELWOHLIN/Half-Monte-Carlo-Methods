import openmc
import math
import os
import numpy as np
import matplotlib.pyplot as plt

filename = "ENDF_to_ACE/endf_test_2/n-W180-rand-0000"
output_directory = "processed_ace_files"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
openmc.data.njoy.make_ace(filename, 
                          output_dir="processed_ace_files",
                          acer="myAceFile",
                          xsdir = "myXsDir",
                          error=0.001)

