iterable
========

Iterable datatype is used to operate on all Python's iterable types which are instances of
``collections.Iterable`` except for ``str``, ``unicode`` and ``bytearray`` in Python 2 and
``str``, ``bytes`` and ``bytearray`` in Python 3. If there is no need to apply any filter
but just to get all the iterables from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.finditerable().inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [{'a': 'b'}, ['bar', 5], (9.32,)]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.finditerable__exact({'a' : 'b'}).inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [{'a': 'b'}]

len
---

Checks that an iterable has specified length.

.. code-block:: python

   >>> instructions.finditerable__len(2).inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [['bar', 5]]

lenlt
-----

Checks that an iterable has length less than specified.

.. code-block:: python

   >>> instructions.finditerable__lenlt(2).inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [{'a': 'b'}, (9.32,)]

lenlte
------

Checks that an iterable has length less than or equal to specified.

.. code-block:: python

   >>> instructions.finditerable__lenlte(2).inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [{'a': 'b'}, ['bar', 5], (9.32,)]

lengt
-----

Checks that an iterable has length greater than specified.

.. code-block:: python

   >>> instructions.finditerable__lengt(1).inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [['bar', 5]]

lengte
------

Checks that an iterable has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.finditerable__lengte(1).inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [{'a': 'b'}, ['bar', 5], (9.32,)]

contains
--------

Checks that an iterable contains the specified value.

.. code-block:: python

   >>> instructions.finditerable__contains('bar').inside(['foo', True, ('foo', 'baz'), ['bar', 5], ('bar', 9.32)])
   [['bar', 5], ('bar', 9.32)]

contains_all
------------

Checks that an iterable contains all specified values.

.. code-block:: python

   >>> instructions.finditerable__contains_all(['foo', 'baz']).inside(['foo', True, ('foo', 'baz'), ['bar', 5], ('bar', 9.32)])
   [('foo', 'baz')]

contains_any
------------

Checks that an iterable contains any of specified values.

.. code-block:: python

   >>> instructions.finditerable__contains_any(['foo', 'bar']).inside(['foo', True, ('foo', 'baz'), ['bar', 5], ('bar', 9.32)])
   [('foo', 'baz'), ['bar', 5], ('bar', 9.32)]

str_contains_str
----------------

Checks that an iterable contains at least one string, which contains specified substring.

.. code-block:: python

   >>> instructions.finditerable__str_contains_str('ba').inside(['foo', True, ('foo', 'baz'), ['bar', 5], ('bar', 9.32)])
   [('foo', 'baz'), ['bar', 5], ('bar', 9.32)]
