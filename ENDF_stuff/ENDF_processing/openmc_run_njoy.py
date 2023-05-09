import openmc.data.njoy

# Input ENDF-6 file path
endf_file = 'ENDF_processing/N_ELMT2.txt'

# Tape numbers for input and output files
tapein = {21: endf_file}  # ENDF-6 file is on tape 21
tapeout = {33: 'covariance_matrix.txt'}  # Covariance matrix will be written to tape 33

# Input commands for NJOY
commands = """
    reconr
    21/
    22/
    bco
    0/
    0/
    moder
    21/
    22/
    0/
    0/
    0/
    heatr
    21/
    22/
    0/
    33/
    0/
    """

# Run NJOY with the given commands and tape mappings
openmc.data.njoy.run(commands, tapein, tapeout)

