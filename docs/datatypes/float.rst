float
=====

Float datatype is used to operate on Python's float type. If there is no need to apply any
filter, but just to get all the floats from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.findfloat().inside(['foo', True, 1.0, 'bar', 5, 9.32])
   [1.0, 9.32]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findfloat__exact(9.32).inside(['foo', True, 1.0, 'bar', 5, 9.32])
   [9.32]

gt
--

Checks that a float is greater than specified.

.. code-block:: python

   >>> instructions.findfloat__gt(5).inside(['foo', True, 1.0, 'bar', 5, 9.32])
   [9.32]

gte
---

Checks that a float is greater than or equal to specified.

.. code-block:: python

   >>> instructions.findfloat__gte(5).inside(['foo', True, 1, 'bar', 5.0, 9.32])
   [5.0, 9.32]

lt
--

Checks that a float is less than specified.

.. code-block:: python

   >>> instructions.findfloat__lt(7).inside(['foo', True, 1.0, 'bar', 5, 9.32])
   [1.0]

lte
---

Checks that a float is less than or equal to specified.

.. code-block:: python

   >>> instructions.findfloat__lte(5).inside(['foo', True, 1, 'bar', 5.0, 9.32])
   [5.0]

between
-------

Inclusively checks that a float is between two other numerics.

.. code-block:: python

   >>> instructions.findfloat__between(5, 10).inside(['foo', True, 1, 'bar', 5.0, 9.32])
   [5.0, 9.32]

ebetween
--------

Exclusively checks that a float is between two other numerics.

.. code-block:: python

   >>> instructions.findfloat__ebetween(5, 10).inside(['foo', True, 1, 'bar', 5, 9.32])
   [9.32]

isodd
-----

Checks that a float is odd. Float is casted to an int before applying the filter.

.. code-block:: python

   >>> instructions.findfloat__isodd().inside(['foo', True, 1, 'bar', 5.0, 9.32])
   [5.0, 9.32]

iseven
------

Checks that a float is even. Float is casted to an int before applying the filter.

.. code-block:: python

   >>> instructions.findfloat__iseven().inside(['foo', True, 1, 'bar', 2.02, 9.32])
   [2.02]

divisibleby
-----------

Checks that a float is divisible by specified. Float is casted to an int before applying the filter.

.. code-block:: python

   >>> instructions.findfloat__divisibleby(2).inside(['foo', True, 1, 'bar', 4.34, 9.32])
   [4.34]

isinteger
---------

Checks that a float is finite with integral value.

.. code-block:: python

   >>> instructions.findfloat__isinteger().inside(['foo', True, 1.0, 'bar', 4.0, 9.32])
   [1.0, 4.0]
