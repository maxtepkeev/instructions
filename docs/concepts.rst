Concepts
========

Before starting to work with Instructions you have to understand a few concepts which are used
across the whole project. There are 3 fundamental blocks: command, datatype and filter. Combined
together they form an instruction which can be executed.

Command
-------

Command is what you want your instruction to do, e.g. find, count, filter etc.

Datatype
--------

Datatype is what you're interested in, e.g. string, tuple, dict etc.

Filter
------

Filter is how you're limiting your result set, e.g. startswith, contains, len etc.

Instruction
-----------

Instruction is the combination of 3 previous concepts. Consider the following example:

.. code-block:: python

   >>> instructions.findint__between(3, 6)

Given this example, ``find`` is the command, ``int`` is the datatype and ``between`` is the filter.
``__`` is the divider between first part of the instruction and the filter. ``(3, 6)`` are the
arguments that this filter takes. That means that every instruction can be written as the following:

.. code-block:: python

   >>> XY__Z(*args, **kwargs)

where ``X`` is the command, ``Y`` is the datatype, ``Z`` is the filter, ``args`` are the filter arguments
and ``kwargs`` are the options that this instruction takes if any.
