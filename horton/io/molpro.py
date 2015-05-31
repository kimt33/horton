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
'''The Molpro 2012 FCIDUMP format.

   .. note ::

       One- and two-electron integrals are stored in chemists' notation in an
       FCIDUMP file while Horton internally uses Physicist's notation.
'''

from horton.orbital_utils import transform_integrals
from horton.utils import check_type, check_options


__all__ = ['load_fcidump', 'dump_fcidump']


def load_fcidump(filename, lf):
    '''Read one- and two-electron integrals from a Molpro 2012 FCIDUMP file.

       Works only for restricted wavefunctions.

       Keep in mind that the FCIDUMP format changed in Molpro 2012, so files
       generated with older versions are not supported.

       **Arguments:**

       filename
            The filename of the fcidump file.

       lf
            A LinalgFactory instance.
    '''
    with open(filename) as f:
        # check header
        line = f.next()
        if not line.startswith(' &FCI NORB='):
            raise IOError('Error in FCIDUMP file header')

        # read info from header
        words = line[5:].split(',')
        header_info = {}
        for word in words:
            if word.count('=') == 1:
                key, value = word.split('=')
                header_info[key.strip()] = value.strip()
        nbasis = int(header_info['NORB'])
        nelec = int(header_info['NELEC'])
        ms2 = int(header_info['MS2'])
        if lf.default_nbasis is not None and lf.default_nbasis != nbasis:
            raise TypeError('The value of lf.default_nbasis does not match NORB reported in the FCIDUMP file.')
        lf.default_nbasis = nbasis

        # skip rest of header
        for line in f:
            words = line.split()
            if words[0] == "&END" or words[0] == "/END" or words[0]=="/":
                break

        # read the integrals
        one_mo = lf.create_two_index()
        two_mo = lf.create_four_index()
        core_energy = 0.0

        for line in f:
            words = line.split()
            if len(words) != 5:
                raise IOError('Expecting 5 fields on each data line in FCIDUMP')
            if words[3] != '0':
                ii = int(words[1])-1
                ij = int(words[2])-1
                ik = int(words[3])-1
                il = int(words[4])-1
                two_mo.set_element(ii,ik,ij,il,float(words[0]))
            elif words[1] != '0':
                ii = int(words[1])-1
                ij = int(words[2])-1
                one_mo.set_element(ii,ij,float(words[0]))
            else:
                core_energy = float(words[0])

    return {
        'lf': lf,
        'nelec': nelec,
        'ms2': ms2,
        'one_mo': one_mo,
        'two_mo': two_mo,
        'core_energy': core_energy,
    }


def dump_fcidump(filename, mol):
    '''Write one- and two-electron integrals in the Molpro 2012 FCIDUMP format.

       Works only for restricted wavefunctions.

       Keep in mind that the FCIDUMP format changed in Molpro 2012, so files
       written with this function cannot be used with older versions of Molpro

       filename
            The filename of the FCIDUMP file. This is usually "FCIDUMP".

       mol
            A Molecule instance. Must contain ``one_mo``, ``two_mo``,
            and optionally ``core_energy``, ``nelec`` and ``ms``
    '''
    with open(filename, 'w') as f:
        one_mo = mol.one_mo
        two_mo = mol.two_mo
        nactive = one_mo.nbasis
        core_energy = getattr(mol, 'core_energy', 0.0)
        nelec = getattr(mol, 'nelec', 0)
        ms2 = getattr(mol, 'ms2', 0)

        # Write header
        print >> f, ' &FCI NORB=%i,NELEC=%i,MS2=%i,' % (nactive, nelec, ms2)
        print >> f, '  ORBSYM= '+",".join(str(1) for v in xrange(nactive))+","
        print >> f, '  ISYM=1'
        print >> f, ' &END'

        # Write integrals and core energy
        for i in xrange(nactive):
            for j in xrange(i+1):
                for k in xrange(nactive):
                    for l in xrange(k+1):
                        # old code
                        #if (i+1)*(j+1) >= (k+1)*(l+1):
                        if (i*(i+1))/2+j >= (k*(k+1))/2+l:
                            value = two_mo.get_element(i,k,j,l)
                            if value != 0.0:
                                print >> f, '%23.16e %4i %4i %4i %4i' % (value, i+1, j+1, k+1, l+1)
        for i in xrange(nactive):
            for j in xrange(i+1):
                value = one_mo.get_element(i,j)
                if value != 0.0:
                    print >> f, '%23.16e %4i %4i %4i %4i' % (value, i+1, j+1, 0, 0)
        if core_energy != 0.0:
            print >> f, '%23.16e %4i %4i %4i %4i' % (core_energy, 0, 0, 0, 0)
