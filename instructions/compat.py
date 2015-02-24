"""
Python 2 and 3 compatibility layer.
"""

import sys
import itertools

py2 = sys.version_info[0] == 2
py3 = sys.version_info[0] == 3

if py3:
    long = int
    string = str
    unicode = str
    numeric = (int, float)
    stringlike = (str, bytes, bytearray)

    MAXSIZE = sys.maxsize
    zip_longest = itertools.zip_longest

    def iterkeys(d, **kwargs):
        """Return an iterator over the keys of a dictionary."""
        return iter(d.keys(**kwargs))

    def itervalues(d, **kwargs):
        """Return an iterator over the values of a dictionary."""
        return iter(d.values(**kwargs))

elif py2:
    long = long
    string = basestring
    unicode = unicode
    numeric = (int, float, long)
    stringlike = (unicode, bytes, bytearray)

    class X(object):
        def __len__(self):
            return 1 << 31

    try:
        len(X())
    except OverflowError:
        MAXSIZE = int((1 << 31) - 1)  # 32-bit
    else:
        MAXSIZE = int((1 << 63) - 1)  # 64-bit
    del X

    zip_longest = itertools.izip_longest

    def iterkeys(d, **kwargs):
        """Return an iterator over the keys of a dictionary."""
        return iter(d.iterkeys(**kwargs))

    def itervalues(d, **kwargs):
        """Return an iterator over the values of a dictionary."""
        return iter(d.itervalues(**kwargs))


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    class MetaClass(meta):
        def __new__(cls, name, this_bases, dct):
            return meta(name, bases, dct)
    return type.__new__(MetaClass, 'temporary_class', (), {})
