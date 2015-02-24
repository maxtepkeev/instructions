"""
Defines all filters used across the project.
"""

from __future__ import unicode_literals

import re

from .compat import string, zip_longest
from .exceptions import FilterImplementationError, FilterUsageError


class Filter(object):
    """
    An abstract filter implementation.

    All filters should inherit from this base class.
    """
    datatype = None
    condition = None

    def __init__(self, condition=None, names=None, accept_types=None):
        """
        :param string condition: (optional). Condition to send to eval().
        :param dict names: (optional). Names to pass to eval().
        :param tuple accept_types: (optional). Types to accept.
        """
        self.names = names or {}
        self.accept_types = accept_types or ()

        if not isinstance(self.names, dict):
            raise FilterImplementationError('"names" is not a dict')

        if not isinstance(self.accept_types, tuple):
            raise FilterImplementationError('"accept_types" is not a tuple')

        if condition is not None:
            self.condition = condition

        if not isinstance(self.condition, string):
            raise FilterImplementationError('"condition" is not a string')

        self.raw_condition = self.condition

    def __call__(self, *args, **kwargs):
        """
        Fills in filter's condition placeholders with actual values.

        :param *args: (optional). Positional arguments that this filter takes if any.
        :param **kwargs: (optional). Keyword arguments that this filter takes if any.
        """
        amount_expected, amount_got = len(set(re.findall('{\d+}', self.raw_condition))), len(args)

        if amount_expected != amount_got:
            raise FilterUsageError('expected {0} argument(s), got {1}'.format(amount_expected, amount_got))

        if self.accept_types:
            for arg, types in zip_longest(args, self.accept_types, fillvalue=self.accept_types):
                if not isinstance(arg, types):
                    raise FilterUsageError('"{0}" argument should be of "{1}" type(s)'.format(
                        arg, types.__name__ if not isinstance(types, tuple) else ', '.join(t.__name__ for t in types)))

        self.condition = self.raw_condition.format(*[repr(arg) for arg in args], kwargs=kwargs)
        return self

    def __or__(self, other):
        """
        OR logical condition implementation.
        """
        return self._combine(other, 'or')

    def __and__(self, other):
        """
        AND logical condition implementation.
        """
        return self._combine(other, 'and')

    def __invert__(self):
        """
        NOT logical condition implementation.
        """
        self.condition = 'not {0}'.format(self.condition)
        return self

    def __str__(self):
        """
        Filter's informal string representation.
        """
        return self.condition

    def __repr__(self):
        """
        Filter's official string representation.
        """
        return '<{0}.{1} "{2}">'.format(self.__class__.__module__, self.__class__.__name__, self.condition)

    def _combine(self, other, condition):
        """
        Helper function used in constructing some logical conditions.
        """
        return Filter('{0} {1} {2}'.format(self.condition, condition, other.condition))


class AugmentedFilter(Filter):
    """
    Augmented filter implementation.

    This filter should be used only within datatype. The datatype should set the
    ``augmentation`` string variable, which AugmentedFilter will use to augment
    it's condition. See :class:`DataTypeMeta` for implementation details.
    """
    is_augmented = False  #: whether filter was already augmented
    org_condition = None  #: original condition before augmentation
