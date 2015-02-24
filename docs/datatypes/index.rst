Datatypes
=========

Datatype is another important block of the instruction. Datatype specifies the target of the
instruction, i.e. what the instruction should return. Datatype is also a way to group a set
of filters together. While each datatype has it's own filters, there are some of them which
are shared across different datatypes. It is also worth noting that each datatype is also a
filter by itself, that is why it is possible to use it inside instructions.

.. note::

   All examples are written using Python 2. They may have a slightly different syntax in Python 3.

.. note::

   To better illustrate how datatypes and filters work, all examples in this section will be
   shown using the ``find`` command. For the sake of readability all examples won't be wrapped
   in a ``list()`` call, however keep in mind that in reality ``find`` command returns it's
   results in the form of generator object.

.. toctree::
   :maxdepth: 1

   bool
   string
   unicode
   bytes
   bytearray
   numeric
   int
   float
   long
   complex
   iterable
   list
   tuple
   set
   frozenset
   dict
