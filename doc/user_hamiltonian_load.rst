.. _hamiltonian_load:

Loading a Hamiltonian from a file
#################################

Loading a Hamiltonian from a file is just the reverse process of :ref:`hamiltonian_dump`. For loading, the same two formats are supported: (i) an internal binary format based on HDF5 (extension ``.h5``) and Molpro's FCIDUMP text format (containing ``FCIDUMP`` somewhere in the file name).

All input and output of data in Horton is done through the :py:class:`horton.io.molecule.Molecule` class. Loading a file from disk is done with the following two steps:

1. Load the file by creating a ``Molecule`` instance with :py:meth:`horton.io.Molecule.from_file`.
2. Access the attribuates of the of ``Molecule`` instance.

The list of attributes is documented here: :py:class:`horton.io.molecule.Molecule`. (Not all of them are supported by each format.) The method :py:meth:`~horton.io.molecule.Molecule.from_file` takes one or more filenames as argument. The filename is used to determine the file format. When it has the extension ``.h5``, the internal format is used. When the file contains ``FCIDUMP``, the FCIDUMP format is used.


Horton's Internal format
========================

For more details in Horton's internal format, read :ref:`hamiltonian_dump_internal`.
The usage pattern is as follows:

.. literalinclude :: ../data/examples/hamiltonian/load_internal_ao.py
    :caption: data/examples/hamiltonian/load_internal_ao.py
    :lines: 2-


FCIDUMP format
==============

For more details in Horton's internal format, read :ref:`hamiltonian_dump_fcidump`.
The usage pattern is as follows:

.. literalinclude :: ../data/examples/hamiltonian/load_fcidump_ao.py
    :caption: data/examples/hamiltonian/load_fcidump_ao.py
    :lines: 2-
