"""
Defines all commands used across the project. All commands in this module,
except the base one, are exposed to the world as a lowercase with Command
part cut out, i.e. ``instructions.commands.find()``.
"""

from __future__ import unicode_literals

import itertools
import collections

from ..compat import stringlike, iterkeys, itervalues
from ..filters import Filter
from ..exceptions import (
    FilterTypeError,
    CommandOptionError,
    CommandOptionTypeError
)


class Command(object):
    """
    An abstract command implementation.

    All commands should inherit from this base class.
    """
    def __init__(self, filtr, **options):
        """
        :param filtr: (required). Filter to use while constructing result set.
        :type filtr: class or object
        :param integer limit: (optional). How many results to return.
        :param integer level: (optional). How deep inside nested iterable data structures to search.
        :param ignore: (optional). What datatypes should be ignored while searching.
        :type ignore: list or tuple
        :param string indict: Whether to search in dict's keys or values.
        """
        if not isinstance(filtr, Filter):
            if isinstance(filtr, type) and issubclass(filtr, Filter):
                filtr = filtr()
            else:
                raise FilterTypeError

        if filtr.datatype is not None:
            names = filtr.datatype.names
            condition = '{0} and {1}'.format(filtr.datatype.condition, filtr.condition)
        else:
            names = {}
            condition = filtr.condition

        self.filter = filtr
        self.raw_condition = condition
        self.condition = compile(condition, '<string>', 'eval')
        self.names = dict(names, **filtr.names)
        self.limit = options.get('limit', 0)
        self.level = options.get('level', 0)
        self.ignore = options.get('ignore', ())
        self.indict = options.get('indict', 'values')

        if not isinstance(self.limit, int):
            raise CommandOptionTypeError('limit', 'int')

        if not isinstance(self.level, int):
            raise CommandOptionTypeError('level', 'int')

        if not isinstance(self.ignore, (list, tuple)):
            raise CommandOptionTypeError('ignore', 'list or tuple')

        if self.indict not in ('keys', 'values'):
            raise CommandOptionError('indict', 'should be set to either "keys" or "values"')

    def inside(self, searchable):
        """
        Triggers the command execution

        :param iterable searchable: (required). An iterable data structure to be searched.
        """
        result = self._command(searchable)

        if self.limit == 0:
            return result
        elif self.limit == 1:
            return next(result, None)
        else:
            return itertools.islice(result, self.limit)

    def _command(self, searchable):
        """
        An implementation of the command.
        """
        raise NotImplementedError('Method "_command" not implemented in: {0}'.format(self.__class__.__name__))


class FindCommand(Command):
    """
    Find command is used when you want to find something.

    Find command returns it's results in the form of generator object to be memory efficient.
    """
    def _command(self, searchable, _level=1):
        for obj in searchable:
            if type(obj) in self.ignore:
                continue

            if (
                isinstance(obj, collections.Iterable)
                and not isinstance(obj, stringlike)
                and (self.level == 0 or self.level > _level)
            ):
                if self.filter.datatype.py is not dict and isinstance(obj, dict):
                    obj = iterkeys(obj) if self.indict == 'keys' else itervalues(obj)

                for inner in self._command(obj, _level+1):
                    yield inner

            # This is where Python's code evaluation from filter takes place
            if eval(self.condition, dict(locals(), **self.names)):
                yield obj


class FirstCommand(FindCommand):
    """
    First command searches for the first match found and returns it.
    """
    def __init__(self, *args, **kwargs):
        """
        :param filtr: (required). Filter to use while constructing result set.
        :type filtr: class or object
        :param integer level: (optional). How deep inside nested iterable data structures to search.
        :param ignore: (optional). Which datatypes should be ignored while searching.
        :type ignore: list or tuple
        :param string indict: Whether to search in dict's keys or values.
        """
        super(FirstCommand, self).__init__(*args, **kwargs)
        self.limit = 1


class LastCommand(FindCommand):
    """
    Last command returns last found result.
    """
    def __init__(self, *args, **kwargs):
        """
        :param filtr: (required). Filter to use while constructing result set.
        :type filtr: class or object
        :param integer level: (optional). How deep inside nested iterable data structures to search.
        :param ignore: (optional). Which datatypes should be ignored while searching.
        :type ignore: list or tuple
        :param string indict: Whether to search in dict's keys or values.
        """
        super(LastCommand, self).__init__(*args, **kwargs)
        self.limit = 0

    def inside(self, *args, **kwargs):
        try:
            return collections.deque(super(LastCommand, self).inside(*args, **kwargs), maxlen=1).pop()
        except IndexError:
            return None


class ExistsCommand(FirstCommand):
    """
    Exists command checks whether there is at least one result inside searchable.
    """
    def inside(self, *args, **kwargs):
        return True if super(ExistsCommand, self).inside(*args, **kwargs) is not None else False


class CountCommand(FindCommand):
    """
    Count command counts how many results are there inside a searchable.
    """
    def inside(self, *args, **kwargs):
        result = super(CountCommand, self).inside(*args, **kwargs)

        if result is None:
            return 0
        elif isinstance(result, collections.Iterator):
            return sum(1 for _ in result)
        else:
            return 1
