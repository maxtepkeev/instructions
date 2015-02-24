Commands
========

Command is one of the building blocks of the instruction. Command specifies an action, i.e. what
the instruction should do. Each command supports several options as keyword arguments which can
influence on results of the instruction:

* ``limit`` - how many results to return, default is 0, which means to return all results.
* ``level`` - how deep inside nested iterable data structures to search, default is 0, which
  means to search inside everything. Let's have a look at the example to better understand
  this option. Imagine that we want to find all strings using the following code:

  .. code-block:: python

     >>> instructions.findstring(level=0).inside(['foo', ['bar', ['baz']]])

  Now if level will be set to 1, then only first level iterable will be searched and ``foo``
  will be the only result, if level will be set to 2, then the result will contain ``foo`` and
  ``bar``, finally if level will be set to 3, the result will contain ``foo``, ``bar`` and ``baz``.
  Level can be set to any positive integer value, e.g. if you set it to 54 then command will be
  searching 54 levels deep, of course if there are so many levels available, if not it will just
  stop at the deepest level available and return all the results it found.

* ``ignore`` - list or tuple of datatypes which should be ignored while searching, default is to
  search everything. Consider the following example:

  .. code-block:: python

     >>> instructions.findstring(ignore=[tuple]).inside(['foo', ['bar', ('baz',)]])

  Because ignore is set to a ``tuple``, only ``foo`` and ``bar`` will be in the search results.

find
----

Find command is used when you want to find something e.g. a string, an integer or maybe several
other datatypes all together inside iterable data structures i.e. list, tuple, dict, set etc.
Find command returns it's results in the form of generator object to be memory efficient. That
means that to see all the results immediately during debugging phase one needs to iterate over
it, ``list`` is a good candidate to do that, e.g.:

  .. code-block:: python

     >>> instructions.findnumeric__gte(7, level=1).inside([1, 3, 5, 7, 9.3, 11, [99]])
     <generator object _command at 0x103ca41e0>

     >>> list(instructions.findnumeric__gte(7, level=1).inside([1, 3, 5, 7, 9.3, 11, [99]]))
     [7, 9.3, 11]

first
-----

First command is the same as find, except that when it finds the first match it returns it and
stops searching for other results. This is actually the shortcut to find command with limit set
to 1, which means that setting a limit option doesn't make sense for this command.

  .. code-block:: python

     >>> instructions.firstnumeric__gte(7).inside([1, 3, 5, 7, 9.3, 11, [99]])
     7

last
----

Last command is the same as find, except that it will return last found result. Last command uses
some optimizations to make searching for the last element as fast as possible, that means that if
you need only last found result, use this command and not a find command with the last element
taken from result. Setting a limit option doesn't make sense for this command.

  .. code-block:: python

     >>> instructions.lastnumeric__gte(7).inside([1, 3, 5, 7, 9.3, 11, [99]])
     99

exists
------

Exists command checks whether there is at least one result inside a searchable container. That
means that it can only return ``True`` or ``False``. Setting a limit option doesn't make sense
for this command.

  .. code-block:: python

     >>> instructions.existsnumeric__gte(7).inside([1, 3, 5, 7, 9.3, 11, [99]])
     True

count
-----

Count command counts how many results are there inside a searchable container. It returns a number
of found results or 0 if nothing is found.

  .. code-block:: python

     >>> instructions.countnumeric__gte(7).inside([1, 3, 5, 7, 9.3, 11, [99]])
     4
