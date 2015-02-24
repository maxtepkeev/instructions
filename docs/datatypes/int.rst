int
===

Int datatype is used to operate on Python's int type. If there is no need to apply any
filter, but just to get all the ints from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.findint().inside(['foo', True, 1, 'bar', 5, 9.32])
   [1, 5]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findint__exact(1).inside(['foo', True, 1, 'bar', 5, 9.32])
   [1]

gt
--

Checks that an int is greater than specified.

.. code-block:: python

   >>> instructions.findint__gt(4).inside(['foo', True, 1, 'bar', 5, 9.32])
   [5]

gte
---

Checks that an int is greater than or equal to specified.

.. code-block:: python

   >>> instructions.findint__gte(5).inside(['foo', True, 1, 'bar', 5, 9.32])
   [5]

lt
--

Checks that an int is less than specified.

.. code-block:: python

   >>> instructions.findint__lt(7).inside(['foo', True, 1, 'bar', 5, 9.32])
   [1, 5]

lte
---

Checks that an int is less than or equal to specified.

.. code-block:: python

   >>> instructions.findint__lte(5).inside(['foo', True, 1, 'bar', 5, 9.32])
   [1, 5]

between
-------

Inclusively checks that an int is between two other ints.

.. code-block:: python

   >>> instructions.findint__between(5, 10).inside(['foo', True, 1, 'bar', 5, 9.32])
   [5]

ebetween
--------

Exclusively checks that an int is between two other ints.

.. code-block:: python

   >>> instructions.findint__ebetween(4, 10).inside(['foo', True, 1, 'bar', 5, 9.32])
   [5]

isodd
-----

Checks that an int is odd.

.. code-block:: python

   >>> instructions.findint__isodd().inside(['foo', True, 1, 'bar', 5, 9.32])
   [1, 5]

iseven
------

Checks that an int is even.

.. code-block:: python

   >>> instructions.findint__iseven().inside(['foo', True, 1, 'bar', 2, 9.32])
   [2]

divisibleby
-----------

Checks that an int is divisible by specified.

.. code-block:: python

   >>> instructions.findint__divisibleby(2).inside(['foo', True, 1, 'bar', 4, 9.32])
   [4]
