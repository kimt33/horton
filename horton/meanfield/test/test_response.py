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


import numpy as np

from horton import *


def check_response(fn):
    mol = Molecule.from_file(fn)
    operators = get_mulliken_operators(mol.obasis, mol.lf)
    exps = [mol.exp_alpha]
    if hasattr(mol, 'exp_beta'):
        exps.append(mol.exp_beta)
    for exp in exps:
        response = compute_noninteracting_response(mol.exp_alpha, operators)
        assert abs(response.sum(axis=0)).max() < 1e-3
        evals = np.linalg.eigvalsh(response)
        assert (evals[:2] < 0).all()
        assert abs(evals[-1]) < 1e-10


def test_response_water_sto3g():
    fn_fchk = context.get_fn('test/water_sto3g_hf_g03.fchk')
    check_response(fn_fchk)


def test_response_h3_321g():
    fn_fchk = context.get_fn('test/h3_hfs_321g.fchk')
    check_response(fn_fchk)