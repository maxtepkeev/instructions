numeric
=======

Numeric datatype is an aggregated datatype which changes it's behaviour under different Python
versions. If used with Python 2, it will operate on ``int``, ``float`` and ``long`` Python
types, while on Python 3 the ``int`` and ``float`` will be it's targets. If there is no need to
apply any filter, but just to get all the numerics from a searchable container, one can use this
code:

.. code-block:: python

   >>> instructions.findnumeric().inside(['foo', True, 1, 'bar', 5, 9.32])
   [1, 5, 9.32]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findnumeric__exact(1).inside(['foo', True, 1, 'bar', 5, 9.32])
   [1]

gt
--

Checks that a numeric is greater than specified.

.. code-block:: python

   >>> instructions.findnumeric__gt(5).inside(['foo', True, 1, 'bar', 5, 9.32])
   [9.32]

gte
---

Checks that a numeric is greater than or equal to specified.

.. code-block:: python

   >>> instructions.findnumeric__gte(5).inside(['foo', True, 1, 'bar', 5, 9.32])
   [5, 9.32]

lt
--

Checks that a numeric is less than specified.

.. code-block:: python

   >>> instructions.findnumeric__lt(7).inside(['foo', True, 1, 'bar', 5, 9.32])
   [1, 5]

lte
---

Checks that a numeric is less than or equal to specified.

.. code-block:: python

   >>> instructions.findnumeric__lte(9.5).inside(['foo', True, 1, 'bar', 5, 9.32])
   [1, 5, 9.32]

between
-------

Inclusively checks that a numeric is between two other numerics.

.. code-block:: python

   >>> instructions.findnumeric__between(5, 10).inside(['foo', True, 1, 'bar', 5, 9.32])
   [5, 9.32]

ebetween
--------

Exclusively checks that a numeric is between two other numerics.

.. code-block:: python

   >>> instructions.findnumeric__ebetween(5, 10).inside(['foo', True, 1, 'bar', 5, 9.32])
   [9.32]

isodd
-----

Checks that a numeric is odd. If the numeric is a float, it is casted to an int.

.. code-block:: python

   >>> instructions.findnumeric__isodd().inside(['foo', True, 1, 'bar', 5, 9.32])
   [1, 5, 9.32]

iseven
------

Checks that a numeric is even. If the numeric is a float, it is casted to an int.

.. code-block:: python

   >>> instructions.findnumeric__iseven().inside(['foo', True, 1, 'bar', 2, 9.32])
   [2]

divisibleby
-----------

Checks that a numeric is divisible by specified. If the numeric is a float, it is casted to an int.

.. code-block:: python

   >>> instructions.findnumeric__divisibleby(2).inside(['foo', True, 1, 'bar', 4, 9.32])
   [4]
