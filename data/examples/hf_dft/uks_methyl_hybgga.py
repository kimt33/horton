#!/usr/bin/env python
#JSON {"lot": "UKS/6-31G*",
#JSON  "scf": "EDIIS2SCFSolver",
#JSON  "linalg": "CholeskyLinalgFactory",
#JSON  "difficulty": 5,
#JSON  "description": "Basic UKS DFT example with hyrbid GGA exhange-correlation functional (B3LYP)"}

from horton import *

# Load the coordinates from file.
# Use the XYZ file from Horton's test data directory.
fn_xyz = context.get_fn('test/methyl.xyz')
mol = Molecule.from_file(fn_xyz)

# Create a Gaussian basis set
obasis = get_gobasis(mol.coordinates, mol.numbers, '6-31g*')

# Create a linalg factory
lf = DenseLinalgFactory(obasis.nbasis)

# Compute Gaussian integrals
olp = obasis.compute_overlap(lf)
kin = obasis.compute_kinetic(lf)
na = obasis.compute_nuclear_attraction(mol.coordinates, mol.pseudo_numbers, lf)
er = obasis.compute_electron_repulsion(lf)

# Define a numerical integration grid needed the XC functionals
grid = BeckeMolGrid(mol.coordinates, mol.numbers, mol.pseudo_numbers)

# Create alpha orbitals
exp_alpha = lf.create_expansion()
exp_beta = lf.create_expansion()

# Initial guess
guess_core_hamiltonian(olp, kin, na, exp_alpha, exp_beta)

# Construct the restricted HF effective Hamiltonian
external = {'nn': compute_nucnuc(mol.coordinates, mol.pseudo_numbers)}
libxc_term = ULibXCHybridGGA('xc_b3lyp')
terms = [
    UTwoIndexTerm(kin, 'kin'),
    UDirectTerm(er, 'hartree'),
    UGridGroup(obasis, grid, [libxc_term]),
    UExchangeTerm(er, 'x_hf', libxc_term.get_exx_fraction()),
    UTwoIndexTerm(na, 'ne'),
]
ham = UEffHam(terms, external)

# Decide how to occupy the orbitals (5 alpha electrons, 4 beta electrons)
occ_model = AufbauOccModel(5, 4)

# Converge WFN with CDIIS+EDIIS SCF
# - Construct the initial density matrix (needed for CDIIS+EDIIS).
occ_model.assign(exp_alpha, exp_beta)
dm_alpha = exp_alpha.to_dm()
dm_beta = exp_beta.to_dm()
# - SCF solver
scf_solver = EDIIS2SCFSolver(1e-6)
scf_solver(ham, lf, olp, occ_model, dm_alpha, dm_beta)

# Assign results to the molecule object and write it to a file, e.g. for
# later analysis. Note that the CDIIS+EDIIS algorithm can only really construct
# an optimized density matrix and no orbitals.
mol.title = 'UHF computation on water'
mol.energy = ham.cache['energy']
mol.obasis = obasis
mol.dm_alpha = ham.cache['dm_alpha']
mol.dm_beta = ham.cache['dm_beta']

# useful for post-processing (results stored in double precision):
mol.to_file('methyl.h5')
