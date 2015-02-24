bytearray
=========

Bytearray datatype is used to operate on Python's bytearray type. If there is no need to apply any
filter, but just to get all the bytearrays from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.findbytearray().inside([bytearray(b'foo'), True, 1, bytearray(b'bar'), 5, u'baz'])
   [bytearray(b'foo'), bytearray(b'bar')]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findbytearray__exact(bytearray(b'foo')).inside([bytearray(b'foo'), True, 1, bytearray(b'bar'), 5, u'baz'])
   [bytearray(b'foo')]

iexact
------

Case-insensitive version of the exact filter.

.. code-block:: python

   >>> instructions.findbytearray__iexact(bytearray(b'foo')).inside([bytearray(b'foo'), True, 1, bytearray(b'FOO'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'FOO')]

contains
--------

Checks that a bytearray contains another byte string or bytearray.

.. code-block:: python

   >>> instructions.findbytearray__contains(b'o').inside([bytearray(b'foo'), True, 1, bytearray(b'FOO'), 5, bytearray(b'bar')])
   [bytearray(b'foo')]

icontains
---------

Case-insensitive version of the contains filter.

.. code-block:: python

   >>> instructions.findbytearray__icontains(b'o').inside([bytearray(b'foo'), True, 1, bytearray(b'FOO'), 5, bytearray(b'bar']))
   [bytearray(b'foo'), bytearray(b'FOO')]

startswith
----------

Checks that a bytearray starts with another byte string or bytearray.

.. code-block:: python

   >>> instructions.findbytearray__startswith(b'f').inside([bytearray(b'foo'), True, 1, bytearray(b'FOO'), 5, bytearray(b'bar')])
   [bytearray(b'foo')]

istartswith
-----------

Case-insensitive version of the startswith filter.

.. code-block:: python

   >>> instructions.findbytearray__istartswith(b'f').inside([bytearray(b'foo'), True, 1, bytearray(b'FOO'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'FOO')]

endswith
--------

Checks that a bytearray ends with another byte string or bytearray.

.. code-block:: python

   >>> instructions.findbytearray__endswith(b'r').inside([bytearray(b'foo'), True, 1, bytearray(b'BAR'), 5, bytearray(b'bar')])
   [bytearray(b'bar')]

iendswith
---------

Case-insensitive version of the endswith filter.

.. code-block:: python

   >>> instructions.findbytearray__iendswith(b'r').inside([bytearray(b'foo'), True, 1, bytearray(b'BAR'), 5, bytearray(b'bar')])
   [bytearray(b'BAR'), bytearray(b'bar')]

len
---

Checks that a bytearray has specified length.

.. code-block:: python

   >>> instructions.findbytearray__len(3).inside([bytearray(b'foo'), True, 1, bytearray(b'blah'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'bar')]

lenlt
-----

Checks that a bytearray has length less than specified.

.. code-block:: python

   >>> instructions.findbytearray__lenlt(4).inside([bytearray(b'foo'), True, 1, bytearray(b'blah'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'bar')]

lenlte
------

Checks that a bytearray has length less than or equal to specified.

.. code-block:: python

   >>> instructions.findbytearray__lenlte(4).inside([bytearray(b'foo'), True, 1, bytearray(b'blah'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'blah'), bytearray(b'bar')]

lengt
-----

Checks that a bytearray has length greater than specified.

.. code-block:: python

   >>> instructions.findbytearray__lengt(3).inside([bytearray(b'foo'), True, 1, bytearray(b'blah'), 5, bytearray(b'bar')])
   [bytearray(b'blah')]

lengte
------

Checks that a bytearray has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.findbytearray__lengte(3).inside([bytearray(b'foo'), True, 1, bytearray(b'blah'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'blah'), bytearray(b'bar')]

isalnum
-------

Checks that all bytes in the bytearray are alphanumeric.

.. code-block:: python

   >>> instructions.findbytearray__isalnum().inside([bytearray(b'foo'), True, 1, bytearray(b'blah'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'blah'), bytearray(b'bar')]

isalnums
--------

Checks that all bytes in the bytearray are alphanumeric or space.

.. code-block:: python

   >>> instructions.findbytearray__isalnums().inside([bytearray(b'foo'), True, 1, bytearray(b'b lah'), 5, bytearray(b'b ar']))
   [bytearray(b'foo'), bytearray(b'b lah'), bytearray(b'b ar')]

isalpha
-------

Checks that all bytes in the bytearray are alphabetic.

.. code-block:: python

   >>> instructions.findbytearray__isalpha().inside([bytearray(b'foo'), True, 1, bytearray(b'blah'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'blah'), bytearray(b'bar')]

isalphas
--------

Checks that all bytes in the bytearray are alphabetic or space.

.. code-block:: python

   >>> instructions.findbytearray__isalphas().inside([bytearray(b'fo o'), True, 1, bytearray(b'blah'), 5, bytearray(b'b ar')])
   [bytearray(b'fo o'), bytearray(b'blah'), bytearray(b'b ar')]

isdigit
-------

Checks that all bytes in the bytearray are digits.

.. code-block:: python

   >>> instructions.findbytearray__isalpha().inside([bytearray(b'foo'), True, 1, bytearray(b'1'), 5, bytearray(b'2')])
   [bytearray(b'1'), bytearray(b'2')]

islower
-------

Checks that all bytes in the bytearray are lowercase.

.. code-block:: python

   >>> instructions.findbytearray__islower().inside([bytearray(b'foo'), True, 1, bytearray(b'BLAH'), 5, bytearray(b'bar')])
   [bytearray(b'foo'), bytearray(b'bar')]

isupper
-------

Checks that all bytes in the bytearray are uppercase.

.. code-block:: python

   >>> instructions.findbytearray__isupper().inside([bytearray(b'foo'), True, 1, bytearray(b'BLAH'), 5, bytearray(b'bar')])
   [bytearray(b'BLAH')]

isspace
-------

Checks that there are only whitespace bytes in the bytearray.

.. code-block:: python

   >>> instructions.findbytearray__isspace().inside([bytearray(b'foo'), True, 1, bytearray(b'   '), 5, bytearray(b'bar')])
   [bytearray(b'   ')]

istitle
-------

Checks that the bytearray is a titlecased string.

.. code-block:: python

   >>> instructions.findbytearray__istitle().inside([bytearray(b'Foo'), True, 1, bytearray(b'blah'), 5, bytearray(b'bar')])
   [bytearray(b'Foo')]
