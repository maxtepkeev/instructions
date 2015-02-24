set
===

Set datatype is used to operate on Python's set type. If there is no need to apply any
filter, but just to get all the sets from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.findset().inside(['foo', True, {'a': 'b'}, set(['bar', 5]), (9.32,)])
   [{5, 'bar'}]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findset__exact(set((9.32,))).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{9.32}]

len
---

Checks that a set has specified length.

.. code-block:: python

   >>> instructions.findset__len(2).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}]

lenlt
-----

Checks that a set has length less than specified.

.. code-block:: python

   >>> instructions.findset__lenlt(2).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{9.32}]

lenlte
------

Checks that a set has length less than or equal to specified.

.. code-block:: python

   >>> instructions.findset__lenlte(2).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}, {9.32}]

lengt
-----

Checks that a set has length greater than specified.

.. code-block:: python

   >>> instructions.findset__lengt(1).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}]

lengte
------

Checks that a set has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.findset__lengte(1).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}, {9.32}]

contains
--------

Checks that a set contains the specified value.

.. code-block:: python

   >>> instructions.findset__contains('bar').inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}]

contains_all
------------

Checks that a set contains all specified values.

.. code-block:: python

   >>> instructions.findset__contains_all(['foo', 'baz']).inside(['foo', True, set(('foo', 'baz')), set(('bar', 5)), set((9.32,))])
   [{'baz', 'foo'}]

contains_any
------------

Checks that a set contains any of specified values.

.. code-block:: python

   >>> instructions.findset__contains_any(['foo', 'bar']).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}]

str_contains_str
----------------

Checks that a set contains at least one string, which contains specified substring.

.. code-block:: python

   >>> instructions.findset__str_contains_str('ba').inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}]

isdisjoint
----------

Checks that a set has no elements in common with specified set.

.. code-block:: python

   >>> instructions.findset__isdisjoint(set(['foo'])).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{5, 'bar'}, {9.32}]

issubset
--------

Checks that every element of a set is in the specified set.

.. code-block:: python

   >>> instructions.findset__issubset(set(['foo', 'bar'])).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}]

eissubset
---------

Checks that every element of a set is in the specified set and that they are not equal.

.. code-block:: python

   >>> instructions.findset__eissubset(set(['foo', 'bar', 'baz'])).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}]

issuperset
----------

Checks that every element of a specified set is in the set.

.. code-block:: python

   >>> instructions.findset__issuperset(set(['bar'])).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}]

eissuperset
-----------

Checks that every element of a specified set is in the set and that they are not equal.

.. code-block:: python

   >>> instructions.findset__eissuperset(set(['bar'])).inside(['foo', True, set(('foo', 'bar')), set(('bar', 5)), set((9.32,))])
   [{'bar', 'foo'}, {5, 'bar'}]
