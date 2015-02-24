"""
Defines datatypes for Python's built-in types. All datatypes in this module,
except the base one, are exposed to the world as a lowercase with Type part
cut out, i.e. ``instructions.datatypes.string()``.
"""

from __future__ import unicode_literals

import copy
import collections
import itertools as it

from ..compat import unicode, string, stringlike, long, numeric, with_metaclass, itervalues, MAXSIZE
from ..filters import Filter, AugmentedFilter
from ..exceptions import DataTypeInitializationError


class DataTypeMeta(type):
    """
    A metaclass for all datatypes that prepares them to function properly.
    """
    def __init__(cls, name, bases, dct):
        super(DataTypeMeta, cls).__init__(name, bases, dct)

        if name == 'DataType':  # nothing should be done for the base class
            return

        if cls.py is None:
            raise DataTypeInitializationError(name, '"py" wasn\'t specified')

        # Because a datatype is a filter by itself and all filter
        # conditions are usual Python strings that are eval'ed in
        # the command, we have to gather names used in datatype to
        # pass them to eval() later in the command
        if isinstance(cls.py, tuple):
            cls.names = dict((obj.__name__, obj) for obj in cls.py)
        else:
            cls.names = {cls.py.__name__: cls.py}

        cls.datatype = cls
        cls.condition = 'isinstance(obj, ({0},))'.format(', '.join(cls.names.keys()))

        if cls.pyex is not None:
            if isinstance(cls.pyex, tuple):
                pyex_names = dict((obj.__name__, obj) for obj in cls.pyex)
            else:
                pyex_names = {cls.pyex.__name__: cls.pyex}

            cls.names.update(pyex_names)
            cls.condition += ' and not isinstance(obj, ({0},))'.format(', '.join(pyex_names.keys()))

        if cls.spec is not None:
            if not isinstance(cls.spec, tuple) and not len(cls.spec) == 2:
                raise DataTypeInitializationError(name, '"spec" should be a tuple of two objects')

            cls.names.update(cls.spec[1])
            cls.condition += ' and {0}'.format(cls.spec[0])

        # Now when a datatype condition is finally constructed and all names are gathered,
        # we need to get all attributes from the inheritance chain that are filters and do
        # some things with them to correctly prepare them for usage inside current datatype
        for item, value in it.chain(it.chain.from_iterable(base.__dict__.items() for base in bases), dct.items()):
            if isinstance(value, Filter):
                filtr = copy.copy(value)

                if (
                    filtr.datatype is not None
                    and filtr.datatype.py in filtr.accept_types
                    and filtr.datatype.py != cls.py
                ):
                    filtr.accept_types = (getattr(cls, 'accept_types', cls.py),)

                # If a datatype contains AugmentedFilters, we should
                # apply cls.augmentation on them or clean them from it
                if isinstance(filtr, AugmentedFilter):
                    try:
                        if not filtr.is_augmented:
                            filtr.condition = filtr.raw_condition.replace('{0}', cls.augmentation)
                            filtr.org_condition = filtr.raw_condition
                            filtr.raw_condition = filtr.condition
                            filtr.is_augmented = True
                        elif cls.augmentation is None:
                            filtr = Filter(filtr.org_condition, filtr.names, filtr.accept_types)
                        elif cls.augmentation != filtr.datatype.augmentation:
                            filtr.condition = filtr.org_condition.replace('{0}', cls.augmentation)
                            filtr.raw_condition = filtr.condition
                    except AttributeError:
                        raise DataTypeInitializationError(
                            name, '"augmentation" attribute is not set, while class contains augmented filters')

                filtr.datatype = cls
                setattr(cls, item, filtr)

    def __instancecheck__(cls, obj):
        """
        Allows datatype to be used in isinstance() function.
        """
        if cls.pyex is not None:
            return isinstance(obj, cls.py) and not isinstance(obj, cls.pyex)
        else:
            return isinstance(obj, cls.py)


class DataType(with_metaclass(DataTypeMeta, Filter)):
    """
    An abstract datatype implementation.

    All datatypes should inherit from this base class.
    """
    py = None    #: A type or tuple of types that this datatype will operate on.
    pyex = None  #: A type or tuple of types to exclude from this datatype.
    spec = None  #: A string of Python code that specifies additional datatype behaviour if any.

    exact = Filter('obj == {0}')


class BoolType(DataType):
    """
    Bool datatype implementation.
    """
    py = bool

    true = Filter('obj is True')
    false = Filter('obj is False')


class StringType(DataType):
    """
    String datatype implementation.
    """
    py = stringlike
    augmentation = '({0}.encode("utf-8") if isinstance(obj, (bytes, bytearray)) else {0})'

    exact = AugmentedFilter('obj == {0}', accept_types=(stringlike,))
    iexact = AugmentedFilter('obj.upper() == {0}.upper()', accept_types=(stringlike,))
    contains = AugmentedFilter('{0} in obj', accept_types=(stringlike,))
    icontains = AugmentedFilter('{0}.upper() in obj.upper()', accept_types=(stringlike,))
    startswith = AugmentedFilter('obj.startswith({0}, **{kwargs})', accept_types=(stringlike,))
    istartswith = AugmentedFilter('obj.upper().startswith({0}.upper(), **{kwargs})', accept_types=(stringlike,))
    endswith = AugmentedFilter('obj.endswith({0}, **{kwargs})', accept_types=(stringlike,))
    iendswith = AugmentedFilter('obj.upper().endswith({0}.upper(), **{kwargs})', accept_types=(stringlike,))
    regex = None
    iregex = None
    len = Filter('len(obj) == {0}', accept_types=(int,))
    lenlt = Filter('len(obj) < {0}', accept_types=(int,))
    lenlte = Filter('len(obj) <= {0}', accept_types=(int,))
    lengt = Filter('len(obj) > {0}', accept_types=(int,))
    lengte = Filter('len(obj) >= {0}', accept_types=(int,))
    isalnum = Filter('obj.isalnum()')
    isalnums = Filter('obj.replace(" ", "").isalnum()')
    isalpha = Filter('obj.isalpha()')
    isalphas = Filter('obj.replace(" ", "").isalpha()')
    isdigit = Filter('obj.isdigit()')
    islower = Filter('obj.islower()')
    isupper = Filter('obj.isupper()')
    isspace = Filter('obj.isspace()')
    istitle = Filter('obj.istitle()')


class UnicodeType(StringType):
    """
    Unicode datatype implementation.
    """
    py = unicode
    augmentation = None
    accept_types = (string,)

    isnumeric = Filter('obj.isnumeric()')
    isdecimal = Filter('obj.isdecimal()')


class BytesType(StringType):
    """
    Bytes datatype implementation.
    """
    py = bytes
    augmentation = None
    accept_types = (bytes, bytearray)

    isalnums = Filter('obj.replace(b" ", b"").isalnum()')
    isalphas = Filter('obj.replace(b" ", b"").isalpha()')


class BytearrayType(BytesType):
    """
    Bytearray datatype implementation.
    """
    py = bytearray


class NumericType(DataType):
    """
    Numeric datatype implementation.
    """
    py = numeric
    pyex = bool
    accept_types = (numeric,)

    gt = Filter('obj > {0}', accept_types=(numeric,))
    gte = Filter('obj >= {0}', accept_types=(numeric,))
    lt = Filter('obj < {0}', accept_types=(numeric,))
    lte = Filter('obj <= {0}', accept_types=(numeric,))
    between = Filter('{0} <= obj <= {1}', accept_types=(numeric,))
    ebetween = Filter('{0} < obj < {1}', accept_types=(numeric,))
    isodd = Filter('int(obj) % 2 != 0')
    iseven = Filter('int(obj) % 2 == 0')
    divisibleby = Filter('int(obj) % {0} == 0', accept_types=(numeric,))


class IntType(NumericType):
    """
    Int datatype implementation.
    """
    py = int


class FloatType(NumericType):
    """
    Float datatype implementation.
    """
    py = float
    pyex = None

    isinteger = Filter('obj.is_integer()')


class LongType(NumericType):
    """
    Long datatype implementation.
    """
    py = long
    spec = ('obj > MAXSIZE', {'MAXSIZE': MAXSIZE})


class ComplexType(DataType):
    """
    Complex datatype implementation.
    """
    py = complex


class IterableType(DataType):
    """
    Iterable datatype implementation.
    """
    py = collections.Iterable
    pyex = stringlike

    len = Filter('len(obj) == {0}', accept_types=(int,))
    lenlt = Filter('len(obj) < {0}', accept_types=(int,))
    lenlte = Filter('len(obj) <= {0}', accept_types=(int,))
    lengt = Filter('len(obj) > {0}', accept_types=(int,))
    lengte = Filter('len(obj) >= {0}', accept_types=(int,))
    contains = Filter('{0} in obj')
    contains_all = Filter('all(item in obj for item in {0})', accept_types=((list, tuple, set),))
    contains_any = Filter('any(item in obj for item in {0})', accept_types=((list, tuple, set),))
    str_contains_str = Filter('any({0} in i for i in obj if isinstance(i, string))', {'string': string}, (string,))


class ListType(IterableType):
    """
    List datatype implementation.
    """
    py = list


class TupleType(IterableType):
    """
    Tuple datatype implementation.
    """
    py = tuple


class SetType(IterableType):
    """
    Set datatype implementation.
    """
    py = set

    isdisjoint = Filter('obj.isdisjoint({0})')
    issubset = Filter('obj <= {0}', accept_types=((set, frozenset),))
    eissubset = Filter('obj < {0}', accept_types=((set, frozenset),))
    issuperset = Filter('obj >= {0}', accept_types=((set, frozenset),))
    eissuperset = Filter('obj > {0}', accept_types=((set, frozenset),))


class FrozensetType(SetType):
    """
    Frozenset datatype implementation.
    """
    py = frozenset


class DictType(DataType):
    """
    Dict datatype implementation.
    """
    py = dict
    pyex = stringlike

    len = Filter('len(obj) == {0}', accept_types=(int,))
    lenlt = Filter('len(obj) < {0}', accept_types=(int,))
    lenlte = Filter('len(obj) <= {0}', accept_types=(int,))
    lengt = Filter('len(obj) > {0}', accept_types=(int,))
    lengte = Filter('len(obj) >= {0}', accept_types=(int,))
    contains_key = Filter('{0} in obj', accept_types=(collections.Hashable,))
    contains_all_keys = Filter('all(item in obj for item in {0})', accept_types=((list, tuple, set),))
    contains_any_keys = Filter('any(item in obj for item in {0})', accept_types=((list, tuple, set),))
    key_contains_str = Filter('any({0} in i for i in obj if isinstance(i, string))', {'string': string}, (string,))
    contains_value = Filter('{0} in itervalues(obj)', {'itervalues': itervalues})
    contains_all_values = Filter('all(item in itervalues(obj) for item in {0})', {'itervalues': itervalues})
    contains_any_values = Filter('any(item in itervalues(obj) for item in {0})', {'itervalues': itervalues})
    value_contains_str = Filter('any({0} in i for i in itervalues(obj) if isinstance(i, string))',
                                {'string': string, 'itervalues': itervalues}, (string,))
