..
    : Horton is a development platform for electronic structure methods.
    : Copyright (C) 2011-2015 The Horton Development Team
    :
    : This file is part of Horton.
    :
    : Horton is free software; you can redistribute it and/or
    : modify it under the terms of the GNU General Public License
    : as published by the Free Software Foundation; either version 3
    : of the License, or (at your option) any later version.
    :
    : Horton is distributed in the hope that it will be useful,
    : but WITHOUT ANY WARRANTY; without even the implied warranty of
    : MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    : GNU General Public License for more details.
    :
    : You should have received a copy of the GNU General Public License
    : along with this program; if not, see <http://www.gnu.org/licenses/>
    :
    : --

Writing unit tests
##################

Horton uses the `Nosetests <https://nose.readthedocs.org/en/latest/>`_
program to run all the unit tests. The goal of a unit test is to check whether
as small piece of code works as expected.


Running the tests
-----------------

The tests are run as follows (including preparation steps)::

    toony@poony ~/.../horton:master> ./cleanfiles.sh
    toony@poony ~/.../horton:master> ./setup.py build_ext -i
    toony@poony ~/.../horton:master> nosetests -v

This will run the tests with the version of Horton in the source tree, i.e. not
the one that is installed with ``python setup.py install``. There are some cases
where the first two commands are not needed. You will figure out.

When working on a specific part of the code, it is often convenient to limit the
number of tests that are checked. The following runs only the tests in ``horton/test/test_cell.py``::

    toony@poony ~/.../horton:master> nosetests -v horton/test/test_cell.py

Within one file, one may also select one test function::

    toony@poony ~/.../horton:master> nosetests -v horton/test/test_cell.py:test_from_parameters3


Writing new tests
-----------------

All tests in Horton are located in the directories ``horton/test`` and
``horton/*/test``. All module files containing tests have a filename that starts
with ``test_``. In these modules, all functions with a name that starts with
``test_`` are picked up by Nosetests. Tests that do not follow this convention,
are simply ignored.

The basic structure of a test is as follows::

    def test_sum():
        a = 1
        b = 2
        assert a+b == 3

Horton currently contains many examples that can be used as a starting point
for new tests. The easiest way to write new tests is to just copy an existing
test (similar to what you have in mind) and start modifying it.

Most test packages in ``horton`` contain a ``common`` module that contains useful
functions that facilitate the development of tests. An important example is the
``check_delta`` function to test of analytical derivatives are properly
implemented. This is a simple example::


    import numpy as np
    from horton.common import check_delta

    def test_quadratic():
        # a vector function that computes the squared norm divided by two
        def fun(x):
            return np.dot(x, x)/2

        # the gradient of that vector function
        def deriv(x):
            return x

        # the dimension of the vector x
        ndim = 5
        # the number of small displacements used in the test
        ndisp = 100
        # a reference point used for the test of the analytical derivatives
        x0 = np.random.uniform(-1, 1, ndim)
        # the small displacements, i.e. each row is one (small) relative vector
        dxs = np.random.uniform(1e-5, 1e5, (ndisp, ndim))

        check_delta(fun, deriv, x0, dxs)


Writing tests that need a temporary directory
---------------------------------------------

A context manager is implemented in ``horton.test.common`` to simplify tests
that need a temporary working directory. It can be used as follows::

    from horton.test.common import tmpdir

    def test_something():
        with tmpdir('horton.somemodule.test.test_something') as dn:
            # dn is a string with the temporary directory name.
            # put here the part of the test that operates in the temporary directory.

On most systems, this temporary directory is a subdirectory of ``/tmp``. The
argument ``'horton.somemodule.test.test_something'`` will occur in the directory
name, such that it can be easily recognized if needed.
