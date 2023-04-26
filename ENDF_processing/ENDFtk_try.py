import sys
import pyne
#Specify the path to your ENDFtk build path
sys.path.append('/home/axelwohlin/Desktop/ENDFtk/build')
import ENDFtk
#Specify the path back to your clone of the git directory
sys.path.append('/home/axelwohlin/Desktop/kand')
filename = 'ENDF_processing/N_ELMT2.txt'#'ENDF_processing/1_2_4_16_17_18_102.txt'
#'ENDF_processing/E4R18790_e4.txt'
#'ENDF_processing/N_ELMT2.txt'#

# Load ENDF-6 file
tape = ENDFtk.tree.Tape.from_file(filename)

# Update MAT code to 9228
mat = tape.material(9228).parse() # Update MAT code to 9228

# Access file and section for desired data
file = mat.file(33).parse()
section = mat.file(33).section(3).parse()

# Now you can work with the data in 'file' and 'section' objects
# for the desired material (Uranium-235 with MAT code 9228)
