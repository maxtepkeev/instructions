"""
Produces instructions in it's basic form, i.e. ``findstring__len(3)``.
"""

from __future__ import unicode_literals

from .prototypes import Command
from ..filters import Filter
from ..datatypes import DataType


def make_instruction(for_filter):
    """
    Produces instruction in it's basic form.

    Uses some global module variables defined in the end of the module.

    :param boolean for_filter: (required). Whether this instruction is for filter or datatype.
    """
    command_name = command.__name__.lower().replace('command', '')
    datatype_name = datatype.__name__.lower().replace('type', '')

    if not for_filter:
        filtr = datatype
        instruction = '{0}{1}'.format(command_name, datatype_name)
    else:
        filtr = value
        instruction = '{0}{1}__{2}'.format(command_name, datatype_name, name)

    # This is the place where magic happens, a new scope is created
    # every time when a new lambda is produced, allowing to create a
    # new instruction in the globals() dictionary
    globals()[instruction] = (lambda c, f: lambda *args, **options: c(f(*args), **options))(command, filtr)


def get_classes(module, level, cls, ignore):
    """
    Returns classes from a given module.

    :param string module: (required). Module to inspect.
    :param integer level: (required). Number of parent directories to search relative to the current directory.
    :param class cls: (required). Return only classes that are subclasses of given class.
    :param tuple ignore: (required). Classes to ignore.
    """
    names = __import__(module, globals(), level=level).__dict__.values()
    return [obj for obj in names if isinstance(obj, type) and issubclass(obj, cls) and obj.__name__ not in ignore]

commands = get_classes('prototypes', 1, Command, ('Command',))
datatypes = get_classes('datatypes', 2, DataType, ('DataType',))

for command in commands:
    for datatype in datatypes:
        make_instruction(False)
        for name, value in datatype.__dict__.items():
            if isinstance(value, Filter):
                make_instruction(True)

# Because this module should be used as from compounds import *
# we have to clean current namespace of unnecessary variables
del Filter, Command, DataType, make_instruction, get_classes, value
del name, commands, datatypes, command, datatype, unicode_literals
