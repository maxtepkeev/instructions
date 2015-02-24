string
======

String datatype is an aggregated datatype which changes it's behaviour under different Python
versions. If used with Python 2, it will operate on ``str``, ``unicode`` and ``bytearray``
Python types, while on Python 3 the ``str``, ``bytes`` and ``bytearray`` will be it's targets.
If there is no need to apply any filter, but just to get all the strings from a searchable
container, one can use this code:

.. code-block:: python

   >>> instructions.findstring().inside(['foo', True, 1, 'bar', 5, bytearray(b'baz')])
   ['foo', 'bar', bytearray(b'baz')]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findstring__exact('foo').inside(['foo', True, 1, 'bar', 5, bytearray(b'baz')])
   ['foo']

iexact
------

Case-insensitive version of the exact filter.

.. code-block:: python

   >>> instructions.findstring__iexact('foo').inside(['foo', True, 1, 'FOO', 5, 'bar'])
   ['foo', 'FOO']

contains
--------

Checks that a string contains another string.

.. code-block:: python

   >>> instructions.findstring__contains('o').inside(['foo', True, 1, 'FOO', 5, 'bar'])
   ['foo']

icontains
---------

Case-insensitive version of the contains filter.

.. code-block:: python

   >>> instructions.findstring__icontains('o').inside(['foo', True, 1, 'FOO', 5, 'bar'])
   ['foo', 'FOO']

startswith
----------

Checks that a string starts with another string.

.. code-block:: python

   >>> instructions.findstring__startswith('f').inside(['foo', True, 1, 'FOO', 5, 'bar'])
   ['foo']

istartswith
-----------

Case-insensitive version of the startswith filter.

.. code-block:: python

   >>> instructions.findstring__istartswith('f').inside(['foo', True, 1, 'FOO', 5, 'bar'])
   ['foo', 'FOO']

endswith
--------

Checks that a string ends with another string.

.. code-block:: python

   >>> instructions.findstring__endswith('r').inside(['foo', True, 1, 'BAR', 5, 'bar'])
   ['bar']

iendswith
---------

Case-insensitive version of the endswith filter.

.. code-block:: python

   >>> instructions.findstring__iendswith('r').inside(['foo', True, 1, 'BAR', 5, 'bar'])
   ['BAR', 'bar']

len
---

Checks that a string has specified length.

.. code-block:: python

   >>> instructions.findstring__len(3).inside(['foo', True, 1, 'blah', 5, 'bar'])
   ['foo', 'bar']

lenlt
-----

Checks that a string has length less than specified.

.. code-block:: python

   >>> instructions.findstring__lenlt(4).inside(['foo', True, 1, 'blah', 5, 'bar'])
   ['foo', 'bar']

lenlte
------

Checks that a string has length less than or equal to specified.

.. code-block:: python

   >>> instructions.findstring__lenlte(4).inside(['foo', True, 1, 'blah', 5, 'bar'])
   ['foo', 'blah', 'bar']

lengt
-----

Checks that a string has length greater than specified.

.. code-block:: python

   >>> instructions.findstring__lengt(3).inside(['foo', True, 1, 'blah', 5, 'bar'])
   ['blah']

lengte
------

Checks that a string has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.findstring__lengte(3).inside(['foo', True, 1, 'blah', 5, 'bar'])
   ['foo', 'blah', 'bar']

isalnum
-------

Checks that all characters in the string are alphanumeric.

.. code-block:: python

   >>> instructions.findstring__isalnum().inside(['foo', True, 1, 'blah', 5, 'bar'])
   ['foo', 'blah', 'bar']

isalnums
--------

Checks that all characters in the string are alphanumeric or space.

.. code-block:: python

   >>> instructions.findstring__isalnums().inside(['foo', True, 1, 'b lah', 5, 'b ar'])
   ['foo', 'b lah', 'b ar']

isalpha
-------

Checks that all characters in the string are alphabetic.

.. code-block:: python

   >>> instructions.findstring__isalpha().inside(['foo', True, 1, 'blah', 5, 'bar'])
   ['foo', 'blah', 'bar']

isalphas
--------

Checks that all characters in the string are alphabetic or space.

.. code-block:: python

   >>> instructions.findstring__isalphas().inside(['fo o', True, 1, 'blah', 5, 'b ar'])
   ['fo o', 'blah', 'b ar']

isdigit
-------

Checks that all characters in the string are digits.

.. code-block:: python

   >>> instructions.findstring__isalpha().inside(['foo', True, 1, '1', 5, '2'])
   ['1', '2']

islower
-------

Checks that all characters in the string are lowercase.

.. code-block:: python

   >>> instructions.findstring__islower().inside(['foo', True, 1, 'BLAH', 5, 'bar'])
   ['foo', 'bar']

isupper
-------

Checks that all characters in the string are uppercase.

.. code-block:: python

   >>> instructions.findstring__isupper().inside(['foo', True, 1, 'BLAH', 5, 'bar'])
   ['BLAH']

isspace
-------

Checks that there are only whitespace characters in the string.

.. code-block:: python

   >>> instructions.findstring__isspace().inside(['foo', True, 1, '   ', 5, 'bar'])
   ['   ']

istitle
-------

Checks that the string is a titlecased string.

.. code-block:: python

   >>> instructions.findstring__istitle().inside(['Foo', True, 1, 'blah', 5, 'bar'])
   ['Foo']
