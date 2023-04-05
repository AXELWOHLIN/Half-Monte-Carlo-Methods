import openmc
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

def process_file(index, input_filename, input_directory, output_directory):
    input_filepath = os.path.join(input_directory, input_filename)
    base_filename = "mp_ace" #os.path.splitext(input_filename)[0]
    output_filename = f"{index}_{base_filename}.ace"

    with open(os.path.join(output_directory, f"{index}_XsDir"), "w") as xsdir_file:
        openmc.data.njoy.make_ace(input_filepath,
                                  output_dir=output_directory,
                                  acer=True,
                                  xsdir=xsdir_file,
                                  error=0.001)

    # Rename the generated ACE file
    os.rename(os.path.join(output_directory, "ace_293.6"),
              os.path.join(output_directory, f"{index}_myAceFile"))

input_directory = "ENDF_to_ACE/endf_test_2"
output_directory = "ENDF_to_ACE/parallel_ace_files"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

pool = multiprocessing.Pool()

for i, filename in enumerate(os.listdir(input_directory)):
    #if filename.endswith(".endf"):
    pool.apply_async(process_file, args=(i, filename, input_directory, output_directory))

pool.close()
pool.join()
