import os
import pyne.ace
from pyne.rxname import *

# Navigate to the file within the directory
file_path = os.path.join('U235.nuss.10.10.2016', 'U235-n.ace_0000')

# Open the file and read its contents
with open(file_path, 'rb') as infile:
    file_contents = infile.read()

# Write the contents to a new file
with open('U235.ace', 'wb') as outfile:
    outfile.write(file_contents)

# Load the ACE file and access the reactions
lib = pyne.ace.Library('U235.ace')
lib.read('92235.00c')
w180 = lib.tables['92235.00c']
reactions = w180.reactions

#print(reactions)
sigma = reactions[2].sigma
print(sigma)

print(name(37))
