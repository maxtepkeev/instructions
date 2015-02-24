long
====

Long datatype is used to operate on Python's long type, because there is no more long type
in Python 3, Instructions will emulate it for you. If there is no need to apply any filter,
but just to get all the longs from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.findlong().inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
   [18446744073709551616L, 3433683820292512484657849089281L]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findlong__exact(2 ** 64).inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
   [18446744073709551616L]

gt
--

Checks that a long is greater than specified.

.. code-block:: python

   >>> instructions.findlong__gt(2 ** 64).inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
   [3433683820292512484657849089281L]

gte
---

Checks that a long is greater than or equal to specified.

.. code-block:: python

   >>> instructions.findlong__gte(2 ** 64).inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
   [18446744073709551616L, 3433683820292512484657849089281L]

lt
--

Checks that a long is less than specified.

.. code-block:: python

   >>> instructions.findlong__lt(3 ** 64).inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
   [18446744073709551616L]

lte
---

Checks that a long is less than or equal to specified.

.. code-block:: python

   >>> instructions.findlong__lte(3 ** 64).inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
   [18446744073709551616L, 3433683820292512484657849089281L]

between
-------

Inclusively checks that a long is between two other longs.

.. code-block:: python

   >>> instructions.findlong__between(2 ** 64, 3 ** 64).inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
   [18446744073709551616L, 3433683820292512484657849089281L]

ebetween
--------

Exclusively checks that a long is between two other longs.

.. code-block:: python

   >>> instructions.findlong__ebetween(2 ** 64, 3 ** 64).inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
   []

isodd
-----

Checks that a long is odd.

.. code-block:: python

   >>> instructions.findlong__isodd().inside(['foo', True, 2 ** 64, 'bar', 5, 3 ** 64])
      [3433683820292512484657849089281L]

iseven
------

Checks that a long is even.

.. code-block:: python

   >>> instructions.findlong__iseven().inside(['foo', True, 2 ** 64, 'bar', 2, 3 ** 64])
   [18446744073709551616L]

divisibleby
-----------

Checks that a long is divisible by specified.

.. code-block:: python

   >>> instructions.findlong__divisibleby(2).inside(['foo', True, 2 ** 64, 'bar', 4, 3 ** 64])
   [18446744073709551616L]
