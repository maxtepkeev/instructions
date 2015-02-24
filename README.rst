Instructions
============

.. image:: https://badge.fury.io/py/instructions.svg
   :target: https://badge.fury.io/py/instructions

.. image:: https://img.shields.io/pypi/dm/instructions.svg
   :target: https://pypi.python.org/pypi/instructions

.. image:: https://img.shields.io/travis/maxtepkeev/instructions/master.svg
   :target: https://travis-ci.org/maxtepkeev/instructions

.. image:: https://img.shields.io/coveralls/maxtepkeev/instructions/master.svg
   :target: https://coveralls.io/r/maxtepkeev/instructions?branch=master

All developers are doing the same thing everyday - they're searching for some values inside
iterable data structures, trying to filter them somehow or count elements inside which satisfy
some requirements. We keep writing the same code over and over again from project to project.
There's no more need to do this, Instructions to the rescue. Instructions is a library, written
in Python to simplify lives of Python developers. This is how we could write some code using
Instructions which searches for a string with a length of 3 inside a list of values:

.. code-block:: python

   >>> instructions.findstring__len(3).inside(['foo', 'bar', 'blah', 1, 2])

Instructions does all the hard work for you, just tell it what do you want to do in plain english
and it will magically execute your instruction.

Features
--------

* Supports Python 2.6 - 3.4, PyPy and PyPy3
* Supports all built-in Python data types
* Easily extendable
* Extensively documented
* Comes with more than 100 filters

Installation
------------

To install Instructions, simply:

.. code-block:: bash

   $ pip install instructions

or:

.. code-block:: bash

   $ easy_install instructions

Documentation
-------------

Documentation is available at https://instructions.readthedocs.org.

Contacts and Support
--------------------

I will be glad to get your `feedback <https://github.com/maxtepkeev/instructions/issues>`_, `pull requests
<https://github.com/maxtepkeev/instructions/pulls>`_, `issues <https://github.com/maxtepkeev/instructions/issues>`_,
whatever. Feel free to contact me for any questions.

Donations and Sponsorship
-------------------------

If you like this project and want to support it you have 3 options:

#. Just give this project a star at the top of the page.
#. You can express your gratitude via `Gratipay <https://gratipay.com/maxtepkeev/>`_.
#. Become a sponsor. Contact me via ``tepkeev at gmail dot com`` if you are interested in becoming a sponsor
   and we will discuss the terms and conditions.

Copyright and License
---------------------

Instructions is licensed under Apache 2.0 license. Check the `LICENSE
<https://github.com/maxtepkeev/instructions/blob/master/LICENSE>`_ for details.
