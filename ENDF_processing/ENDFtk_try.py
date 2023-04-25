import sys
import pyne
#Specify the path to your ENDFtk build path
sys.path.append('/home/axelwohlin/Desktop/ENDFtk/build')
import ENDFtk
#Specify the path back to your clone of the git directory
sys.path.append('/home/axelwohlin/Desktop/kand')
filename = "ENDF_processing/N_ELMT2.txt"
tape = ENDFtk.tree.Tape.from_file(filename)
print(tape.MAT(9228))
