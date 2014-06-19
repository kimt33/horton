# -*- coding: utf-8 -*-
# Horton is a development platform for electronic structure methods.
# Copyright (C) 2011-2013 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of Horton.
#
# Horton is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Horton is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--
#pylint: skip-file


import numpy as np
from horton import *
from nose.tools import assert_raises

def test_1D_Hubbard_hamiltonian():
    # Test the half-filled 1-D Hubbard model Hamiltonian
    # with 10 sites for U=2 and using PBC

    lf = DenseLinalgFactory(10)
    occ_model = AufbauOccModel(5)
    modelham = Hubbard(pbc=True)
    exp_alpha = lf.create_expansion(10)
    olp = modelham.compute_overlap(lf)
    # t-param, t = -1
    kin = modelham.compute_kinetic(lf, -1)
    # U-param, U = 2
    er = modelham.compute_er(lf, 2)
    # Guess
    guess_core_hamiltonian(olp, kin, exp_alpha)
    terms = [
        ROneBodyTerm(kin, 'kin'),
        RDirectTerm(er, 'hartree'),
        RExchangeTerm(er, 'x_hf'),
    ]
    ham = REffHam(terms)
    scf_solver = PlainSCFSolver()
    scf_solver(ham, lf, olp, occ_model, exp_alpha)
    energy = ham.compute()

    assert (abs(energy --7.94427) < 1e-4)


def test_1D_Hubbard_hamiltonian_no_pbc():
    # Test the half-filled 1-D Hubbard model Hamiltonian
    # with 10 sites for U=2 without PBC

    lf = DenseLinalgFactory(10)
    occ_model = AufbauOccModel(5)
    modelham = Hubbard(pbc=False)
    exp_alpha = lf.create_expansion(10)
    olp = modelham.compute_overlap(lf)
    # t-param, t = -1
    kin = modelham.compute_kinetic(lf, -1)
    # U-param, U = 2
    er = modelham.compute_er(lf, 2)
    # Guess
    guess_core_hamiltonian(olp, kin, exp_alpha)
    terms = [
        ROneBodyTerm(kin, 'kin'),
        RDirectTerm(er, 'hartree'),
        RExchangeTerm(er, 'x_hf'),
    ]
    ham = REffHam(terms)
    scf_solver = PlainSCFSolver()
    scf_solver(ham, lf, olp, occ_model, exp_alpha)
    energy = ham.compute()

    assert (abs(energy --7.0533) < 1e-4)