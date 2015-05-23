#!/usr/bin/env python
#JSON {"lot": "RKS/6-31G*",
#JSON  "scf": "CDIISSCFSolver",
#JSON  "linalg": "CholeskyLinalgFactory",
#JSON  "difficulty": 6,
#JSON  "description": "RKS DFT example with LDA and numerical Hartree"}

from horton import *

# Load the coordinates from file.
# Use the XYZ file from Horton's test data directory.
fn_xyz = context.get_fn('test/water.xyz')
mol = Molecule.from_file(fn_xyz)

# Create a Gaussian basis set
obasis = get_gobasis(mol.coordinates, mol.numbers, '6-31g*')

# Create a linalg factory
lf = CholeskyLinalgFactory(obasis.nbasis)

# Compute Gaussian integrals (not the ERI!)
olp = obasis.compute_overlap(lf)
kin = obasis.compute_kinetic(lf)
na = obasis.compute_nuclear_attraction(mol.coordinates, mol.pseudo_numbers, lf)

# Define a numerical integration grid needed the XC functionals. The mode='keep'
# option is need for the numerical Becke-Poisson solver.
grid = BeckeMolGrid(mol.coordinates, mol.numbers, mol.pseudo_numbers, mode='keep')

# Create alpha orbitals
exp_alpha = lf.create_expansion()

# Initial guess
guess_core_hamiltonian(olp, kin, na, exp_alpha)

# Construct the restricted HF effective Hamiltonian
external = {'nn': compute_nucnuc(mol.coordinates, mol.pseudo_numbers)}
terms = [
    RTwoIndexTerm(kin, 'kin'),
    RGridGroup(obasis, grid, [
        RBeckeHartree(lmax=8),
        RLibXCLDA('x'),
        RLibXCLDA('c_vwn'),
    ]),
    RTwoIndexTerm(na, 'ne'),
]
ham = REffHam(terms, external)

# Decide how to occupy the orbitals (5 alpha electrons)
occ_model = AufbauOccModel(5)

# Converge WFN with CDIIS SCF
# - Construct the initial density matrix (needes for CDIIS).
occ_model.assign(exp_alpha)
dm_alpha = exp_alpha.to_dm()
# - SCF solver
scf_solver = CDIISSCFSolver(1e-6)
scf_solver(ham, lf, olp, occ_model, dm_alpha)

# Assign results to the molecule object and write it to a file, e.g. for
# later analysis. Note that the CDIIS algorithm can only really construct an
# optimized density matrix and no orbitals.
mol.title = 'RHF computation on water'
mol.energy = ham.cache['energy']
mol.obasis = obasis
mol.dm_alpha = ham.cache['dm_alpha']

# useful for post-processing (results stored in double precision):
mol.to_file('water.h5')
