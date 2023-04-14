import numpy as np


first_word = '92235'
mt_number = ' 1 '

sense_values = []

with open('filename.txt') as f:
    header_found = False
    for line in f:
        if first_word and mt_number in line:
            header_found = True
            continue
        else:
            if header_found == True:
                if line.startswith(' '):
                    data = [float(x) for x in line.split()]
                    sense_values.append(data)
                else:   
                    header_found = false
        
sense_values = np.array(sense_values)