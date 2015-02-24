unicode
=======

Unicode datatype changes it's behaviour under different Python versions. If used with Python 2,
it will operate on ``unicode`` Python type, while on Python 3 the ``str`` will be it's target.
If there is no need to apply any filter, but just to get all the unicode strings from a searchable
container, one can use this code:

.. code-block:: python

   >>> instructions.findunicode().inside([u'foo', True, 1, 'bar', 5, u'baz'])
   [u'foo', u'baz']

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.findunicode__exact(u'foo').inside([u'foo', True, 1, 'bar', 5, u'baz'])
   [u'foo']

iexact
------

Case-insensitive version of the exact filter.

.. code-block:: python

   >>> instructions.findunicode__iexact(u'foo').inside([u'foo', True, 1, u'FOO', 5, u'bar'])
   [u'foo', u'FOO']

contains
--------

Checks that a unicode string contains another unicode string.

.. code-block:: python

   >>> instructions.findunicode__contains(u'o').inside([u'foo', True, 1, u'FOO', 5, u'bar'])
   [u'foo']

icontains
---------

Case-insensitive version of the contains filter.

.. code-block:: python

   >>> instructions.findunicode__icontains(u'o').inside([u'foo', True, 1, u'FOO', 5, u'bar'])
   [u'foo', u'FOO']

startswith
----------

Checks that a unicode string starts with another unicode string.

.. code-block:: python

   >>> instructions.findunicode__startswith(u'f').inside([u'foo', True, 1, u'FOO', 5, u'bar'])
   [u'foo']

istartswith
-----------

Case-insensitive version of the startswith filter.

.. code-block:: python

   >>> instructions.findunicode__istartswith(u'f').inside([u'foo', True, 1, u'FOO', 5, u'bar'])
   [u'foo', u'FOO']

endswith
--------

Checks that a unicode string ends with another unicode string.

.. code-block:: python

   >>> instructions.findunicode__endswith(u'r').inside([u'foo', True, 1, u'BAR', 5, u'bar'])
   [u'bar']

iendswith
---------

Case-insensitive version of the endswith filter.

.. code-block:: python

   >>> instructions.findunicode__iendswith(u'r').inside([u'foo', True, 1, u'BAR', 5, u'bar'])
   [u'BAR', u'bar']

len
---

Checks that a unicode string has specified length.

.. code-block:: python

   >>> instructions.findunicode__len(3).inside([u'foo', True, 1, u'blah', 5, u'bar'])
   [u'foo', u'bar']

lenlt
-----

Checks that a unicode string has length less than specified.

.. code-block:: python

   >>> instructions.findunicode__lenlt(4).inside([u'foo', True, 1, u'blah', 5, u'bar'])
   [u'foo', u'bar']

lenlte
------

Checks that a unicode string has length less than or equal to specified.

.. code-block:: python

   >>> instructions.findunicode__lenlte(4).inside([u'foo', True, 1, u'blah', 5, u'bar'])
   [u'foo', u'blah', u'bar']

lengt
-----

Checks that a unicode string has length greater than specified.

.. code-block:: python

   >>> instructions.findunicode__lengt(3).inside([u'foo', True, 1, u'blah', 5, u'bar'])
   [u'blah']

lengte
------

Checks that a unicode string has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.findunicode__lengte(3).inside([u'foo', True, 1, u'blah', 5, u'bar'])
   [u'foo', u'blah', u'bar']

isalnum
-------

Checks that all characters in the unicode string are alphanumeric.

.. code-block:: python

   >>> instructions.findunicode__isalnum().inside([u'foo', True, 1, u'blah', 5, u'bar'])
   [u'foo', u'blah', u'bar']

isalnums
--------

Checks that all characters in the unicode string are alphanumeric or space.

.. code-block:: python

   >>> instructions.findunicode__isalnums().inside([u'foo', True, 1, u'b lah', 5, u'b ar'])
   [u'foo', u'b lah', u'b ar']

isalpha
-------

Checks that all characters in the unicode string are alphabetic.

.. code-block:: python

   >>> instructions.findunicode__isalpha().inside([u'foo', True, 1, u'blah', 5, u'bar'])
   [u'foo', u'blah', u'bar']

isalphas
--------

Checks that all characters in the unicode string are alphabetic or space.

.. code-block:: python

   >>> instructions.findunicode__isalphas().inside([u'fo o', True, 1, u'blah', 5, u'b ar'])
   [u'fo o', u'blah', u'b ar']

isdigit
-------

Checks that all characters in the unicode string are digits.

.. code-block:: python

   >>> instructions.findunicode__isalpha().inside([u'foo', True, 1, u'1', 5, u'2'])
   [u'1', u'2']

islower
-------

Checks that all characters in the unicode string are lowercase.

.. code-block:: python

   >>> instructions.findunicode__islower().inside([u'foo', True, 1, u'BLAH', 5, u'bar'])
   [u'foo', u'bar']

isupper
-------

Checks that all characters in the unicode string are uppercase.

.. code-block:: python

   >>> instructions.findunicode__isupper().inside([u'foo', True, 1, u'BLAH', 5, u'bar'])
   [u'BLAH']

isspace
-------

Checks that there are only whitespace characters in the unicode string.

.. code-block:: python

   >>> instructions.findunicode__isspace().inside([u'foo', True, 1, u'   ', 5, u'bar'])
   ['   ']

istitle
-------

Checks that the unicode string is a titlecased string.

.. code-block:: python

   >>> instructions.findunicode__istitle().inside([u'Foo', True, 1, u'blah', 5, u'bar'])
   [u'Foo']

isnumeric
---------

Checks that all characters in the unicode string are numeric.

.. code-block:: python

   >>> instructions.findunicode__isnumeric().inside([u'Foo', True, 1, u'⅕', 5, u'bar'])
   [u'⅕']

isdecimal
---------

Checks that all characters in the unicode string are decimal.

.. code-block:: python

   >>> instructions.findunicode__isdecimal().inside([u'Foo', True, 1, u'٠', 5, u'bar'])
   [u'٠']
