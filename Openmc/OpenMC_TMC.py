import openmc
import math
import os
from time import perf_counter
os.environ['OPENMC_CROSS_SECTIONS']='/home/rfp/kand/Openmc_godiva/hdf5_files/cross_sections.xml'
os.system('rm %s%output')
os.system('rm s*.h5')
import numpy as np
import matplotlib.pyplot as plt

def KandGodiva(particles):
    u02 = openmc.Material(1, "U235", temperature=293.6)
    # Add nuclides to uo2
    u02.add_nuclide('U235', 0.937)
    u02.add_nuclide('U234', 0.01)
    u02.add_nuclide('U238', 0.053)

    u02.set_density('g/cm3', 18.7)

    r_godiva=8.69696
    u02.volume = 4*math.pi*r_godiva**2/3


    mats = openmc.Materials([u02])
    mats.export_to_xml()

    fuel_or = openmc.Sphere(r=r_godiva)

    fuel_region = -fuel_or

    fuel = openmc.Cell(1, 'fuel')
    fuel.fill = u02
    fuel.region = fuel_region

    pitch = 50
    #we define the x and y planes with boundary condition
    left = openmc.XPlane(x0=-pitch/2, boundary_type='vacuum')
    right = openmc.XPlane(x0=pitch/2, boundary_type='vacuum')
    bottom = openmc.YPlane(y0=-pitch/2, boundary_type='vacuum')
    top = openmc.YPlane(y0=pitch/2, boundary_type='vacuum')
    z1 = openmc.ZPlane(z0=pitch/2, boundary_type='vacuum')
    z2 = openmc.ZPlane(z0=-pitch/2, boundary_type='vacuum')

    #outside of left and inside of right, outside of bottom, and inside of top and outside of fuel outer cylinder
    outer_region = +left & -right & +bottom & -top & +fuel_or & -z1 & +z2

    outer = openmc.Cell(name='outer')
    outer.region = outer_region

    root = openmc.Universe(cells=(fuel, outer))

    geom = openmc.Geometry()
    geom.root_universe = root
    geom.export_to_xml()

    point = openmc.stats.Point((0, 0, 0))
    src = openmc.Source(space=point)

    settings = openmc.Settings()
    settings.source = src
    settings.batches = 100
    settings.inactive = 10
    settings.particles = particles
    settings.output = {'tallies': False}
    settings.export_to_xml()

    model = openmc.model.Model(geom, mats, settings)
    
    return model

"""
particles_vector=[100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000, 25000, 50000, 75000, 100000, 250000, 500000, 1000000]
keff_vector=[]
for particles in particles_vector:
    output=KandGodiva(particles).run()
    keff_vector.append(openmc.StatePoint(output).k_combined.nominal_value)

plt.plot(particles_vector, keff_vector)
plt.title('k value depending on the amount of particles in each batch')
plt.xlabel('Particles')
plt.ylabel('k value')
plt.savefig('openmcplot.png')
"""

def Ace_to_hdf5(dir_ace,dir_hdf5,ace_files):
    
    ace_files=[]

    os.chdir(dir_ace)
    for entry in os.scandir('.'):
        if entry.is_file() and ".ace" in entry.name:
            ace_files.append(str(entry.name))

    ace_files=sorted(ace_files)
    print(ace_files)
    for ace_file in ace_files:
        if os.path.isfile('U235.h5'):#If files already exist remove
            os.remove('U235.h5')
        if os.path.isfile('cross_sections.xml'):#If files already exist remove
            os.remove('cross_sections.xml')
        os.chdir(dir_ace) #Make sure dir is with all ace files
        U235 = openmc.data.IncidentNeutron.from_ace(ace_file)
        os.chdir(dir_hdf5) #The hdf5 files is created in the right folder
        U235.export_to_hdf5(f'U235.h5')

        #Create library
        library = openmc.data.DataLibrary()
        library.register_file('U235.h5')
        library.register_file('U234.h5')
        library.register_file('U238.h5')
        library.export_to_xml()
        return

def main():
    
    t1_start = perf_counter()
    ace_files=[]
    k_effs=[]
    keff12=[]
    dir_ace='/home/rfp/kand/u235.nuss.30.04.2023/'
    dir_hdf5='/home/rfp/kand/Openmc_godiva/hdf5_files'
    dir_godiva ='/home/rfp/kand/Openmc_godiva'

    os.chdir(dir_ace)
    for entry in os.scandir('.'):
        if entry.is_file() and ".ace" in entry.name:
            ace_files.append(str(entry.name))
            
            
    print(ace_files)
    ace_files=sorted(ace_files)
    print(ace_files)

    for ace_file in ace_files:
        os.chdir(dir_hdf5)
        if os.path.isfile('U235.h5'):#If files already exist remove
            os.remove('U235.h5')
        if os.path.isfile('cross_sections.xml'):#If files already exist remove
            os.remove('cross_sections.xml')
        os.chdir(dir_ace) #Make sure dir is with all ace files
        U235 = openmc.data.IncidentNeutron.from_ace(ace_file)
        os.chdir(dir_hdf5) #The hdf5 files is created in the right folder
        U235.export_to_hdf5('U235.h5')

        #Create library
        library = openmc.data.DataLibrary()
        library.register_file('U235.h5')
        library.register_file('U234.h5')
        library.register_file('U238.h5')
        library.export_to_xml()
        os.chdir(dir_godiva)
        output=KandGodiva(600000).run()
        keff=openmc.StatePoint(output).k_combined.nominal_value
        keff2=openmc.StatePoint('/home/rfp/kand/Openmc_godiva/statepoint.100.h5').k_combined
        keff12.append(keff2)
        k_effs.append(keff)
        print(keff)

        print(k_effs)

        delta_keff=[]
        for element in k_effs:
            delta_keff.append(element-k_effs[0])
        delta_keff=delta_keff[1:]
        print(delta_keff)
        print(keff12)
    t1_stop = perf_counter()
    print("Elapsed time during TMC OpenMC:", t1_stop-t1_start)
if __name__ == '__main__':
    main()