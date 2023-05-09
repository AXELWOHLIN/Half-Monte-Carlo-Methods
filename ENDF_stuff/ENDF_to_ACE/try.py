import openmc
import math
import os
import numpy as np
import matplotlib.pyplot as plt

filename = "ENDF_to_ACE/endf_test_2/n-W180-rand-0000"
output_directory = "ENDF_to_ACE/processed_ace_files"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(os.path.join(output_directory, "myXsDir"), "w") as xsdir_file:
    openmc.data.njoy.make_ace(filename,
                              output_dir=output_directory,
                              acer=True,
                              xsdir=xsdir_file,
                              error=0.001)

# Rename the generated ACE file
os.rename(os.path.join(output_directory, "ace_293.6"),
          os.path.join(output_directory, "myAceFile"))
