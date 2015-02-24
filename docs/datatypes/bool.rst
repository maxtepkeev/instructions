bool
====

Bool datatype is used to operate on Python's boolean type. If there is no need to apply any
filter, but just to get all the booleans from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.findbool().inside(['foo', True, 1, False, 5, True])
   [True, False, True]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findbool__exact(True).inside(['foo', True, 1, False, 5, True])
   [True, True]

true
----

Limits results to all ``True`` values.

.. code-block:: python

   >>> instructions.findbool__true().inside(['foo', True, 1, False, 5, True])
   [True, True]

false
-----

Limits results to all ``False`` values.

.. code-block:: python

   >>> instructions.findbool__false().inside(['foo', True, 1, False, 5, True])
   [False]
