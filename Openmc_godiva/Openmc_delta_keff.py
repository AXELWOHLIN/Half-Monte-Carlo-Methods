
import math
import os
os.environ['OPENMC_CROSS_SECTIONS']='/home/rfp/kand/Openmc_godiva/hdf5_files/cross_sections.xml'
os.system('rm %s%output')
os.system('rm s*.h5')
import numpy as np
import matplotlib.pyplot as plt




keff=[1.0056457910509333, 0.9708947762492609, 0.9817897617731475, 0.9824299565878541, 0.9672115030966415, 0.9681543995799965, 0.9935385256633708, 0.9928286056553759, 0.9850651735380225]
delta_keff=[]
for element in keff:
    delta_keff.append(element-keff[0])
delta_keff=delta_keff[1:]
print(np.mean(delta_keff))
print(np.std(delta_keff))
