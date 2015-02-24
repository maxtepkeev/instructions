complex
=======

Complex datatype is used to operate on Python's complex type. If there is no need to apply any
filter, but just to get all the complex numbers from a searchable container, one can use this
code:

.. code-block:: python

   >>> instructions.findcomplex().inside(['foo', True, 1j, 'bar', 5, 9.32])
   [1j]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findcomplex__exact(1j).inside(['foo', True, 1j, 'bar', 5, 9.32])
   [1j]
