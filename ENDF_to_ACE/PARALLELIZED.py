import openmc
import math
import os
import numpy as np
import matplotlib.pyplot as plt

filename = "ENDF_to_ACE/endf_test_2/n-W180-rand-0000"
openmc.data.njoy.make_ace(filename)

openmc.data.njoy.make_ace(filename, acer="processed_ace_files/mike", xsdir="processed_ace_files/mikexs",\
                        pendf=False, error=0.001, broadr=False, \
                        heatr=False, gaspr=False, purr=False, evaluation=None, \
                        smoothing=True)