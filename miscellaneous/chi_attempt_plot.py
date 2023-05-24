import pyne.endf
pyne.endf.EnergyDistribution
import pyne
from pyne import endf as sheesh
mike = pyne.endf.Evaluation('ENDF_stuff/ENDF_to_ACE/u235_ENDF_test/U235-n_rand_0000')
mike2 = pyne.endf.Evaluation('ENDF_stuff/ENDF_to_ACE/u235_ENDF_test/U235-n_rand_0001')

print(mike.read())


