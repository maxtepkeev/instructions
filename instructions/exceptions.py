"""
Instructions tries it's best to provide human readable errors in all situations.
This is a list of all exceptions that Instructions can throw.
"""

from __future__ import unicode_literals


class InstructionsError(Exception):
    """
    Base exception class for Instructions exceptions.
    """
    def __init__(self, *args, **kwargs):
        super(InstructionsError, self).__init__(*args, **kwargs)


class FilterImplementationError(InstructionsError):
    """
    Filter not implemented correctly.
    """
    def __init__(self, reason):
        super(FilterImplementationError, self).__init__('Filter is not usable because {0}'.format(reason))


class FilterUsageError(InstructionsError):
    """
    Incorrect usage of Filter.
    """
    def __init__(self, reason):
        super(FilterUsageError, self).__init__('Incorrect usage of filter: {0}'.format(reason))


class FilterTypeError(InstructionsError, TypeError):
    """
    Provided filter should be of Filter type.
    """
    def __init__(self):
        super(FilterTypeError, self).__init__('Provided filter should be of Filter type')


class DataTypeInitializationError(InstructionsError):
    """
    DataType class can't be initialized.
    """
    def __init__(self, cls, reason):
        super(DataTypeInitializationError, self).__init__(
            "{0} class can't be initialized because {1}".format(cls, reason))


class CommandOptionError(InstructionsError):
    """
    Command option error.
    """
    def __init__(self, option, message):
        super(CommandOptionError, self).__init__('{0} option {1}'.format(option, message))


class CommandOptionTypeError(InstructionsError, TypeError):
    """
    Provided option doesn't have the needed type.
    """
    def __init__(self, option, type_):
        super(CommandOptionTypeError, self).__init__('{0} option should be of "{1}" type'.format(option, type_))
