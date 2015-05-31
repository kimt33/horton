Getting started
###############

How to run Horton
=================

Horton is essentially a Python library that can be used to do electronic structure calculations and the post-processing of such calculations. There are two different ways of working with Horton. The most versatile approach is to write Python scripts that use Horton as a Python library. This gives you full access to all features in Horton but it also requires some understanding of the Python programming language. Alternatively, some of the functionality is also accessible through built-in python scripts whose behaviour can be controlled through command line arguments. This requires less technical background from the user.


Running horton as a Python library
----------------------------------

There will be many examples in the following sections that explain what can be done with Horton by writing your own Python scripts. These scripts should all start with the following lines:

.. code-block:: python

    #!/usr/bin/env python

    # Import the Horton library
    from horton import *

    # Optionally import some other stuff
    import numpy as np, h5py as h5, matplotlib.pyplot as pt

    # Actual script

This header is then followed by some Python code that does the actual computation of interest. In such a script you basically write the `main` program of the calculation of interest, using the components Horton offers. The Horton library is designed such that all features are as modular as possible, allowing you to combine them in various ways.

Before you run your script, say ``run.py``, we recommend you make it executable (once):

.. code-block:: bash

    $ chmod +x run,py

When your script it completed, run it as follows:

.. code-block:: bash

    $ ./run.py

Do not use ``horton.py`` as a script name as that will interfer with loading
the ``horton`` library (due to a namespace collision).


Running horton with provided ``horton-*.py`` scripts
----------------------------------------------------

The builtin Horton scripts all have the following filename pattern: ``horton-*.py``. Through command line arguments, one can control the actual calculation. Basic usage informatoin is obtained with the ``--help`` flag, e.g.:

.. code-block:: bash

    $ horton-convert.py --help


Writing your first Horton Python script
=======================================

Horton scripts just run a in regular Python interpreter (like `ASE <https://wiki.fysik.dtu.dk/ase/>`_ and unlike `PSI4 <http://www.psicode.org/>`_ which uses a modified Python interpreter). This means you first need to learn basic Python. It may also be of interest to become familiar with the Python packages that are popular in Scientific computing. Here are some links to broaden your background knowledge:

* `Python <https://www.python.org/>`_, `Python documentation <https://docs.python.org/2.7>`_, `Getting started with Python <https://www.python.org/about/gettingstarted/>`_
* `NumPy <http://www.numpy.org/>`_ (array manipulation), `Getting started with NumPy <http://docs.scipy.org/doc/numpy/user/>`_
* `SciPy <http://www.scipy.org/>`_ (scientific computing library), `The SciPy tutorial <http://docs.scipy.org/doc/scipy/reference/tutorial/index.html>`_
* `Matplotlib <http://matplotlib.org/>`_ (plotting)
* `H5Py <http://www.h5py.org/>`_ (load/dump arrays from/to binary files)
* `Programming Q&A <http://stackoverflow.com/>`_
* `Python code snippets <http://code.activestate.com/recipes/langs/python/>`_

The following sections go through some basic features that will re-occur in many
other examples in the documentation.


Atomic units
------------

Horton internally works exclusively with atomic units. If you want to convert a value from a different unit to atomic units, multiply it with the appropriate unit constant, e.g. the following sets ``length`` to 5 Angstrom and prints it out in atomic units:

.. code-block:: python

    length = 5*angstrom
    print length

Conversly, if you want to print a value in a different unit than atomic units, divide it by the appropriate constant. For example, the following prints an energy of 0.001 Hartree in kJ/mol:

.. code-block:: python

    energy = 0.001
    print energy/kjmol

An overview of all units can be found here: :py:mod:`horton.units`.

There are some special cases in the way units are handled:

1. Angles are in radians but one can use the ``deg`` unit the work with degrees, e.g. ``90*deg`` and ``np.pi/2`` are equivalent.
2. Temperaturea are in Kelvin. (There is no atomic unit for temperature.)


Array indexing
--------------

All arrays (and list-like) objects in Python use zero-based indexing. This means that the first element of a vector is accessed as follows:

.. code-block:: python

    vector = np.array([1, 2, 3])
    print vector[0]

This convention thus also applies to all array-like objects in Horton, e.g. the first orbital in a Slater determinant has index 0.


Loading/Dumping data from/to a file
-----------------------------------

All input and output of data in Horton is done through the :py:class:`~horton.io.molecule.Molecule` class. Data can be loaded with a call to the class method :py:meth:`~horton.io.molecule.Molecule.from_file` of the :py:class:`~horton.io.molecule.Molecule` class, e.g.:

.. code-block:: python

    mol = Molecule.from_file('water.xyz')

The data read from file are accessible as attributes of the ``mol`` object, e.g. the following prints the coordinates of the nuclei in Angstrom:

.. code-block:: python

    print mol.coordinates/angstrom

Writing data to a file is done by first creating a :py:class:`~horton.io.molecule.Molecule` instance, followed by setting the appropriate attributes and finally followed by a call to the ``to_file`` method of the :py:class:`~horton.io.molecule.Molecule` class, e.g. the following creates a `.xyz` file with a Neon atom:

.. code-block:: python

    mol = Molecule(title='Neon')
    mol.coordinates = np.array([[0.0, 0.0, 0.0]])
    mol.numbers = np.array([10])
    mol.to_file('neon.xyz')

A Complete list of supported file formats for data input or output can be found here: :ref:`ref_file_formats`, including a list of :py:class:`~horton.io.molecule.Molecule` attributes supported by each file format. A definition of all possible :py:class:`~horton.io.molecule.Molecule` attributes can be found here: :py:class:`horton.io.molecule.Molecule`.


A complete example
------------------

This first example is kept very simple to illustrate the basics of a Horton Python script. (So, it does not do an electronic calculation yet.) The following example loads an ``.xyz`` file and computes the molecular mass. Finally, it writes out data read from the ``.xyz`` file and the mass into a ``.h5`` file, using Horton's internal data format.

.. literalinclude:: ../data/examples/getting_started/first.py
    :caption: data/examples/getting_started/first.py

Note that the part ``context.get_fn('test/water.xyz')`` is used to look up a data file from the Horton data directory. If you want to use your own file, load the molecule as follows instead:

.. code-block:: python

    mol = Molecule.from_file('your_file.xyz')
