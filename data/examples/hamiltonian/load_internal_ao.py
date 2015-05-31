#!/usr/bin/env python

from horton import *

# Load the integrals from the file
data = IOData.from_file('hamiltonian_ao.h5')

# Access some attributes. In more realistic cases, some code follows that does a
# useful calculation.
print data.kin.nbasis
