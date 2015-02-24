list
====

List datatype is used to operate on Python's list type. If there is no need to apply any
filter, but just to get all the lists from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.findlist().inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [['bar', 5]]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findlist__exact([9.32]).inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [[9.32]]

len
---

Checks that a list has specified length.

.. code-block:: python

   >>> instructions.findlist__len(2).inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [['foo', 'bar'], ['bar', 5]]

lenlt
-----

Checks that a list has length less than specified.

.. code-block:: python

   >>> instructions.findlist__lenlt(2).inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [[9.32]]

lenlte
------

Checks that a list has length less than or equal to specified.

.. code-block:: python

   >>> instructions.findlist__lenlte(2).inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [['foo', 'bar'], ['bar', 5], [9.32]]

lengt
-----

Checks that a list has length greater than specified.

.. code-block:: python

   >>> instructions.findlist__lengt(1).inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [['foo', 'bar'], ['bar', 5]]

lengte
------

Checks that a list has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.findlist__lengte(1).inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [['foo', 'bar'], ['bar', 5], [9.32]]

contains
--------

Checks that a list contains the specified value.

.. code-block:: python

   >>> instructions.findlist__contains('bar').inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [['foo', 'bar'], ['bar', 5]]

contains_all
------------

Checks that a list contains all specified values.

.. code-block:: python

   >>> instructions.findlist__contains_all(['foo', 'baz']).inside(['foo', True, ['foo', 'baz'], ['bar', 5], [9.32]])
   [['foo', 'baz']]

contains_any
------------

Checks that a list contains any of specified values.

.. code-block:: python

   >>> instructions.findlist__contains_any(['foo', 'bar']).inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [['foo', 'bar'], ['bar', 5]]

str_contains_str
----------------

Checks that a list contains at least one string, which contains specified substring.

.. code-block:: python

   >>> instructions.findlist__str_contains_str('ba').inside(['foo', True, ['foo', 'bar'], ['bar', 5], [9.32]])
   [['foo', 'bar'], ['bar', 5]]
