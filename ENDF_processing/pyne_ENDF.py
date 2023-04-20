"""
Tried showing energy vector for the ENDF file, but it gives
key error.

"""

import requests
from pyne.xs.data_source import ENDFDataSource
from pyne import nucname
from os.path import isfile
import os
import requests    
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from tabulate import tabulate
from pyne.endf import Library, Evaluation

filename = "ENDF_to_ACE/u235_ENDF_test/U235-n_rand_0000"
with open(filename, "rb") as infile:
    content = infile.read()
    with open("ENDF_test.bin", "wb") as outfile:
        outfile.write(content)

"""
endfds = ENDFDataSource("ENDF_test.bin")
central_rx = endfds.reaction(922350000, 1, 922350000)

central_e = central_rx['e_int']
central_xs = central_rx['xs']
"""

u235 = Library("ENDF_test.bin")
xs_data = u235.get_xs(92235, 16)[0]
fig = plt.figure()
Eints, sigmas = xs_data['e_int'], xs_data['xs']
plt.step(Eints, sigmas, where = "pre")
plt.suptitle(r'(n, 2n) Reaction in $^{235}$U')
plt.ylabel(r'$\sigma(E)$ (barns)')
plt.xlabel(r'$E_{int} (eV)$')
plt.xscale('log')
plt.yscale('log')
plt.show()
"""
filename2 = "ENDF_to_ACE/u235_ENDF_test/U235-n_rand_0001"
with open(filename2) as r:
    with open("ENDF_test2.txt" ,"wb") as outfile:
            outfile.write(r.content)

endfds = ENDFDataSource("ENDF_test.txt")
central_rx = endfds.reaction("ENDF_test.txt", "total")

file1_e = central_rx['e_int']
file1_xs = central_rx['xs']
"""