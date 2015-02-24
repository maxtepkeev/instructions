dict
====

Dict datatype is used to operate on Python's dict type. If there is no need to apply any
filter, but just to get all the dicts from a searchable container, one can use this code:

.. code-block:: python

   >>> instructions.finddict().inside(['foo', True, {'a': 'b'}, ['bar', 5], (9.32,)])
   [{'a': 'b'}]

exact
-----

An exact match.

.. code-block:: python

   >>> instructions.finddict__exact({'ab': 'ba'}).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'ab': 'ba'}]

len
---

Checks that a dict has specified length.

.. code-block:: python

   >>> instructions.finddict__len(2).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}]

lenlt
-----

Checks that a dict has length less than specified.

.. code-block:: python

   >>> instructions.finddict__lenlt(2).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'ab': 'ba'}, {'abc': 'bca'}]

lenlte
------

Checks that a dict has length less than or equal to specified.

.. code-block:: python

   >>> instructions.finddict__lenlte(2).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}]

lengt
-----

Checks that a dict has length greater than specified.

.. code-block:: python

   >>> instructions.finddict__lengt(1).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}]

lengte
------

Checks that a dict has length greater than or equal to specified.

.. code-block:: python

   >>> instructions.finddict__lengte(1).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}]

contains_key
------------

Checks that a dict contains key equals to the specified value.

.. code-block:: python

   >>> instructions.finddict__contains_key('ab').inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'ab': 'ba'}]

contains_all_keys
-----------------

Checks that a dict contains all keys equal to the specified values.

.. code-block:: python

   >>> instructions.finddict__contains_all_keys(['a', 'b']).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}]

contains_any_keys
-----------------

Checks that a dict contains any keys equal to the specified values.

.. code-block:: python

   >>> instructions.finddict__contains_any_keys(['a', 'ab']).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}, {'ab': 'ba'}]

key_contains_str
----------------

Checks that a dict contains at least one key which is a string, which contains specified substring.

.. code-block:: python

   >>> instructions.finddict__key_contains_str('ab').inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'ab': 'ba'}, {'abc': 'bca'}]

contains_value
--------------

Checks that a dict contains value equals to the specified.

.. code-block:: python

   >>> instructions.finddict__contains_value('ba').inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'ab': 'ba'}]

contains_all_values
-------------------

Checks that a dict contains all values equal to the specified.

.. code-block:: python

   >>> instructions.finddict__contains_all_values(['a', 'b']).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}]

contains_any_values
-------------------

Checks that a dict contains any values equal to the specified.

.. code-block:: python

   >>> instructions.finddict__contains_any_values(['b', 'ba']).inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}, {'ab': 'ba'}]

value_contains_str
------------------

Checks that a dict contains at least one value which is a string, which contains specified substring.

.. code-block:: python

   >>> instructions.finddict__value_contains_str('b').inside(['foo', True, {'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}])
   [{'a': 'b', 'b': 'a'}, {'ab': 'ba'}, {'abc': 'bca'}]
