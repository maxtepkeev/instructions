frozenset
=========

Frozenset datatype is used to operate on Python's frozenset type. If there is no need to
apply any filter, but just to get all the frozensets from a searchable container, one can
use this code:

.. code-block:: python

   >>> instructions.findfrozenset().inside(['foo', True, {'a': 'b'}, frozenset(['bar', 5]), (9.32,)])
   [frozenset({5, 'bar'})]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findfrozenset__exact(frozenset((9.32,))).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({9.32})]

len
---

Checks that a frozenset has specified length.

.. code-block:: python

   >>> instructions.findfrozenset__len(2).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'})]

lenlt
-----

Checks that a frozenset has length less than specified.

.. code-block:: python

   >>> instructions.findfrozenset__lenlt(2).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({9.32})]

lenlte
------

Checks that a frozenset has length less than or equal to specified.

.. code-block:: python

   >>> instructions.findfrozenset__lenlte(2).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'}), frozenset({9.32})]

lengt
-----

Checks that a frozenset has length greater than specified.

.. code-block:: python

   >>> instructions.findfrozenset__lengt(1).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'})]

lengte
------

Checks that a frozenset has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.findfrozenset__lengte(1).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'}), frozenset({9.32})]

contains
--------

Checks that a frozenset contains the specified value.

.. code-block:: python

   >>> instructions.findfrozenset__contains('bar').inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'})]

contains_all
------------

Checks that a frozenset contains all specified values.

.. code-block:: python

   >>> instructions.findfrozenset__contains_all(['foo', 'baz']).inside(['foo', True, frozenset(('foo', 'baz')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'baz', 'foo'})]

contains_any
------------

Checks that a frozenset contains any of specified values.

.. code-block:: python

   >>> instructions.findfrozenset__contains_any(['foo', 'bar']).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'})]

str_contains_str
----------------

Checks that a frozenset contains at least one string, which contains specified substring.

.. code-block:: python

   >>> instructions.findfrozenset__str_contains_str('ba').inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'})]

isdisjoint
----------

Checks that a frozenset has no elements in common with specified set or frozenset.

.. code-block:: python

   >>> instructions.findfrozenset__isdisjoint(set(['foo'])).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({5, 'bar'}), frozenset({9.32})]

issubset
--------

Checks that every element of a frozenset is in the specified set or frozenset.

.. code-block:: python

   >>> instructions.findfrozenset__issubset(set(['foo', 'bar'])).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'})]

eissubset
---------

Checks that every element of a frozenset is in the specified set or frozenset and that they are not equal.

.. code-block:: python

   >>> instructions.findfrozenset__eissubset(set(['foo', 'bar', 'baz'])).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'})]

issuperset
----------

Checks that every element of a specified set or frozenset is in the frozenset.

.. code-block:: python

   >>> instructions.findfrozenset__issuperset(set(['bar'])).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'})]

eissuperset
-----------

Checks that every element of a specified set or frozenset is in the frozenset and that they are not equal.

.. code-block:: python

   >>> instructions.findfrozenset__eissuperset(set(['bar'])).inside(['foo', True, frozenset(('foo', 'bar')), frozenset(('bar', 5)), frozenset((9.32,))])
   [frozenset({'bar', 'foo'}), frozenset({5, 'bar'})]
