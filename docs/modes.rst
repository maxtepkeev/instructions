Modes
=====

Instructions can operate in two modes: basic and advanced.

Basic
-----

Basic mode should be used if you need just some simple instructions, e.g.:

.. code-block:: python

   >>> import instructions

   >>> instructions.finddict__value_contains_str('foo').inside(container)

This will give you all dicts from container which have values that are strings and contain
``foo`` substring. All examples in the documentation are written using Instruction's basic
mode.

Advanced
--------

In advanced mode you can combine different filters together using operators, e.g.:

.. code-block:: python

   >>> from instructions import commands, datatypes

   >>> commands.count(
   ...     datatypes.string.startswith('foo') & datatypes.string.endswith('bar') & ~datatypes.string.contains('blah')
   ... ).inside(container)

This will give you the amount of strings inside a container which start with ``foo``, end
with ``bar`` but don't contain the ``blah`` substring, i.e. ``foobar`` will match but ``fooblahbar``
won't.

Here's the list of operators that can be used to combine filters together:

* ``&`` - logical AND operator
* ``|`` - logical OR operator
* ``~`` - logical NOT operator

While advanced mode requires one to write a little bit more code, it also gives maximum
flexibility and allows to combine different filters of different datatypes together,
constructing complex instructions.
