#!/usr/bin/env python

from horton import *
import numpy as np

# Set up Neon atom, define basis set
# ----------------------------------
coordinates = np.array([[0.0, 0.0, 0.0]])
numbers = np.array([10])
obasis = get_gobasis(coordinates, numbers, 'cc-pvdz')
lf = DenseLinalgFactory(obasis.nbasis)

# Construct Hamiltonian
# ---------------------
one_mo = lf.create_two_index()
obasis.compute_kinetic(one_mo)
obasis.compute_nuclear_attraction(coordinates, numbers.astype(float), one_mo)
two_mo = obasis.compute_electron_repulsion(lf)
core_energy = compute_nucnuc(coordinates, numbers.astype(float))

# Write to a HDF5 file
# --------------------
mol = Molecule()
mol.one_mo = one_mo
mol.two_mo = two_mo
mol.core_energy = core_energy
mol.nelec = 10
mol.ms2 = 0
mol.to_file('hamiltonian_ao_fcidump.h5')
