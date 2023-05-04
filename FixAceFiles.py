import os

dir_ace='/home/rfp/kand/u235.nuss.30.04.2023/'

os.chdir(dir_ace)
for entry in os.scandir('.'):
    if entry.is_file() and ".ace" in entry.name:
        ace_files.append(str(entry.name))
            
            
    ace_files=sorted(ace_files)
    ace_files=ace_files[1:]


for ace_file in ace_files:
    file=open(ace_file,'r+')
    content = file.read()
    lines = content.splitlines()
    lines[-1]=lines[-1][:20]
    
    file.seek(0)

    file.write
