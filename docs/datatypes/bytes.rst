bytes
=====

Bytes datatype changes it's behaviour under different Python versions. If used with Python 2,
it will operate on ``str`` Python type, while on Python 3 the ``bytes`` will be it's target.
If there is no need to apply any filter, but just to get all the byte strings from a searchable
container, one can use this code:

.. code-block:: python

   >>> instructions.findbytes().inside([b'foo', True, 1, b'bar', 5, u'baz'])
   [b'foo', b'bar']

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findbytes__exact(b'foo').inside([b'foo', True, 1, b'bar', 5, u'baz'])
   [b'foo']

iexact
------

Case-insensitive version of the exact filter.

.. code-block:: python

   >>> instructions.findbytes__iexact(b'foo').inside([b'foo', True, 1, b'FOO', 5, b'bar'])
   [b'foo', b'FOO']

contains
--------

Checks that a byte string contains another byte string.

.. code-block:: python

   >>> instructions.findbytes__contains(b'o').inside([b'foo', True, 1, b'FOO', 5, b'bar'])
   [b'foo']

icontains
---------

Case-insensitive version of the contains filter.

.. code-block:: python

   >>> instructions.findbytes__icontains(b'o').inside([b'foo', True, 1, b'FOO', 5, b'bar'])
   [b'foo', b'FOO']

startswith
----------

Checks that a byte string starts with another byte string.

.. code-block:: python

   >>> instructions.findbytes__startswith(b'f').inside([b'foo', True, 1, b'FOO', 5, b'bar'])
   [b'foo']

istartswith
-----------

Case-insensitive version of the startswith filter.

.. code-block:: python

   >>> instructions.findbytes__istartswith(b'f').inside([b'foo', True, 1, b'FOO', 5, b'bar'])
   [b'foo', b'FOO']

endswith
--------

Checks that a byte string ends with another byte string.

.. code-block:: python

   >>> instructions.findbytes__endswith(b'r').inside([b'foo', True, 1, b'BAR', 5, b'bar'])
   [b'bar']

iendswith
---------

Case-insensitive version of the endswith filter.

.. code-block:: python

   >>> instructions.findbytes__iendswith(b'r').inside([b'foo', True, 1, b'BAR', 5, b'bar'])
   [b'BAR', b'bar']

len
---

Checks that a byte string has specified length.

.. code-block:: python

   >>> instructions.findbytes__len(3).inside([b'foo', True, 1, b'blah', 5, b'bar'])
   [b'foo', b'bar']

lenlt
-----

Checks that a byte string has length less than specified.

.. code-block:: python

   >>> instructions.findbytes__lenlt(4).inside([b'foo', True, 1, b'blah', 5, b'bar'])
   [b'foo', b'bar']

lenlte
------

Checks that a byte string has length less than or equal to specified.

.. code-block:: python

   >>> instructions.findbytes__lenlte(4).inside([b'foo', True, 1, b'blah', 5, b'bar'])
   [b'foo', b'blah', b'bar']

lengt
-----

Checks that a byte string has length greater than specified.

.. code-block:: python

   >>> instructions.findbytes__lengt(3).inside([b'foo', True, 1, b'blah', 5, b'bar'])
   [b'blah']

lengte
------

Checks that a byte string has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.findbytes__lengte(3).inside([b'foo', True, 1, b'blah', 5, b'bar'])
   [b'foo', b'blah', b'bar']

isalnum
-------

Checks that all bytes in the byte string are alphanumeric.

.. code-block:: python

   >>> instructions.findbytes__isalnum().inside([b'foo', True, 1, b'blah', 5, b'bar'])
   [b'foo', b'blah', b'bar']

isalnums
--------

Checks that all bytes in the byte string are alphanumeric or space.

.. code-block:: python

   >>> instructions.findbytes__isalnums().inside([b'foo', True, 1, b'b lah', 5, b'b ar'])
   [b'foo', b'b lah', b'b ar']

isalpha
-------

Checks that all bytes in the byte string are alphabetic.

.. code-block:: python

   >>> instructions.findbytes__isalpha().inside([b'foo', True, 1, b'blah', 5, b'bar'])
   [b'foo', b'blah', b'bar']

isalphas
--------

Checks that all bytes in the byte string are alphabetic or space.

.. code-block:: python

   >>> instructions.findbytes__isalphas().inside([b'fo o', True, 1, b'blah', 5, b'b ar'])
   [b'fo o', b'blah', b'b ar']

isdigit
-------

Checks that all bytes in the byte string are digits.

.. code-block:: python

   >>> instructions.findbytes__isalpha().inside([b'foo', True, 1, b'1', 5, b'2'])
   [b'1', b'2']

islower
-------

Checks that all bytes in the byte string are lowercase.

.. code-block:: python

   >>> instructions.findbytes__islower().inside([b'foo', True, 1, b'BLAH', 5, b'bar'])
   [b'foo', b'bar']

isupper
-------

Checks that all bytes in the byte string are uppercase.

.. code-block:: python

   >>> instructions.findbytes__isupper().inside([b'foo', True, 1, b'BLAH', 5, b'bar'])
   [b'BLAH']

isspace
-------

Checks that there are only whitespace bytes in the byte string.

.. code-block:: python

   >>> instructions.findbytes__isspace().inside([b'foo', True, 1, b'   ', 5, b'bar'])
   [b'   ']

istitle
-------

Checks that the byte string is a titlecased string.

.. code-block:: python

   >>> instructions.findbytes__istitle().inside([b'Foo', True, 1, b'blah', 5, b'bar'])
   [b'Foo']
