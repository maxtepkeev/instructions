from . import unittest
from instructions import compat, datatypes, filters, exceptions


class DatatypesTestCase(unittest.TestCase):
    def test_api(self):
        self.assertTrue(hasattr(datatypes, 'DataType'))
        self.assertTrue(hasattr(datatypes, 'bool'))
        self.assertTrue(hasattr(datatypes, 'string'))
        self.assertTrue(hasattr(datatypes, 'unicode'))
        self.assertTrue(hasattr(datatypes, 'bytes'))
        self.assertTrue(hasattr(datatypes, 'bytearray'))
        self.assertTrue(hasattr(datatypes, 'numeric'))
        self.assertTrue(hasattr(datatypes, 'int'))
        self.assertTrue(hasattr(datatypes, 'float'))
        self.assertTrue(hasattr(datatypes, 'long'))
        self.assertTrue(hasattr(datatypes, 'complex'))
        self.assertTrue(hasattr(datatypes, 'iterable'))
        self.assertTrue(hasattr(datatypes, 'list'))
        self.assertTrue(hasattr(datatypes, 'tuple'))
        self.assertTrue(hasattr(datatypes, 'set'))
        self.assertTrue(hasattr(datatypes, 'frozenset'))
        self.assertTrue(hasattr(datatypes, 'dict'))

    def test_initialization_errors(self):
        self.assertRaises(exceptions.DataTypeInitializationError, lambda: type('Foo', (datatypes.DataType,), {}))
        self.assertRaises(exceptions.DataTypeInitializationError, lambda: type('Foo', (datatypes.DataType,), {
            'py': int, 'pyex': (bool,), 'spec': 'foo'}))
        self.assertRaises(exceptions.DataTypeInitializationError, lambda: type('Foo', (datatypes.DataType,), {
            'py': int, 'foo': filters.AugmentedFilter('')}))

    def test_base(self):
        self.assertIsNone(datatypes.DataType.py)
        self.assertIsNone(datatypes.DataType.pyex)
        self.assertIsNone(datatypes.DataType.spec)
        self.assertTrue(issubclass(datatypes.DataType, filters.Filter))
        self.assertIsInstance(datatypes.DataType.exact, filters.Filter)

    def test_bool(self):
        self.assertEqual(datatypes.bool.py, bool)
        self.assertEqual(datatypes.bool.datatype, datatypes.bool)
        self.assertTrue(isinstance(True, datatypes.bool))
        self.assertIsInstance(datatypes.bool.true, filters.Filter)
        self.assertEqual(datatypes.bool.true.datatype, datatypes.bool)
        self.assertIsInstance(datatypes.bool.false, filters.Filter)
        self.assertEqual(datatypes.bool.false.datatype, datatypes.bool)

    def test_string(self):
        self.assertEqual(datatypes.string.py, compat.stringlike)
        self.assertEqual(datatypes.string.datatype, datatypes.string)
        self.assertTrue(isinstance('foo', datatypes.string))
        self.assertTrue(isinstance(b'foo'.decode(), datatypes.string))
        self.assertTrue(isinstance(b'foo', datatypes.string))
        self.assertTrue(isinstance(bytearray(b'foo'), datatypes.string))
        self.assertIsInstance(datatypes.string.exact, filters.AugmentedFilter)
        self.assertEqual(datatypes.string.exact.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.iexact, filters.AugmentedFilter)
        self.assertEqual(datatypes.string.iexact.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.contains, filters.AugmentedFilter)
        self.assertEqual(datatypes.string.contains.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.icontains, filters.AugmentedFilter)
        self.assertEqual(datatypes.string.icontains.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.startswith, filters.AugmentedFilter)
        self.assertEqual(datatypes.string.startswith.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.istartswith, filters.AugmentedFilter)
        self.assertEqual(datatypes.string.istartswith.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.endswith, filters.AugmentedFilter)
        self.assertEqual(datatypes.string.endswith.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.iendswith, filters.AugmentedFilter)
        self.assertEqual(datatypes.string.iendswith.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.len, filters.Filter)
        self.assertEqual(datatypes.string.len.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.lenlt, filters.Filter)
        self.assertEqual(datatypes.string.lenlt.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.lenlte, filters.Filter)
        self.assertEqual(datatypes.string.lenlte.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.lengt, filters.Filter)
        self.assertEqual(datatypes.string.lengt.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.lengte, filters.Filter)
        self.assertEqual(datatypes.string.lengte.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.isalnum, filters.Filter)
        self.assertEqual(datatypes.string.isalnum.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.isalnums, filters.Filter)
        self.assertEqual(datatypes.string.isalnums.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.isalpha, filters.Filter)
        self.assertEqual(datatypes.string.isalpha.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.isalphas, filters.Filter)
        self.assertEqual(datatypes.string.isalphas.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.isdigit, filters.Filter)
        self.assertEqual(datatypes.string.isdigit.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.islower, filters.Filter)
        self.assertEqual(datatypes.string.islower.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.isupper, filters.Filter)
        self.assertEqual(datatypes.string.isupper.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.isspace, filters.Filter)
        self.assertEqual(datatypes.string.isspace.datatype, datatypes.string)
        self.assertIsInstance(datatypes.string.istitle, filters.Filter)
        self.assertEqual(datatypes.string.istitle.datatype, datatypes.string)

    def test_unicode(self):
        self.assertEqual(datatypes.unicode.py, compat.unicode)
        self.assertEqual(datatypes.unicode.datatype, datatypes.unicode)
        self.assertTrue(isinstance(b'foo'.decode(), datatypes.unicode))
        self.assertIsInstance(datatypes.unicode.exact, filters.Filter)
        self.assertEqual(datatypes.unicode.exact.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.iexact, filters.Filter)
        self.assertEqual(datatypes.unicode.iexact.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.contains, filters.Filter)
        self.assertEqual(datatypes.unicode.contains.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.icontains, filters.Filter)
        self.assertEqual(datatypes.unicode.icontains.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.startswith, filters.Filter)
        self.assertEqual(datatypes.unicode.startswith.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.istartswith, filters.Filter)
        self.assertEqual(datatypes.unicode.istartswith.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.endswith, filters.Filter)
        self.assertEqual(datatypes.unicode.endswith.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.iendswith, filters.Filter)
        self.assertEqual(datatypes.unicode.iendswith.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.len, filters.Filter)
        self.assertEqual(datatypes.unicode.len.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.lenlt, filters.Filter)
        self.assertEqual(datatypes.unicode.lenlt.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.lenlte, filters.Filter)
        self.assertEqual(datatypes.unicode.lenlte.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.lengt, filters.Filter)
        self.assertEqual(datatypes.unicode.lengt.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.lengte, filters.Filter)
        self.assertEqual(datatypes.unicode.lengte.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isalnum, filters.Filter)
        self.assertEqual(datatypes.unicode.isalnum.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isalnums, filters.Filter)
        self.assertEqual(datatypes.unicode.isalnums.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isalpha, filters.Filter)
        self.assertEqual(datatypes.unicode.isalpha.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isalphas, filters.Filter)
        self.assertEqual(datatypes.unicode.isalphas.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isdecimal, filters.Filter)
        self.assertEqual(datatypes.unicode.isdecimal.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isdigit, filters.Filter)
        self.assertEqual(datatypes.unicode.isdigit.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.islower, filters.Filter)
        self.assertEqual(datatypes.unicode.islower.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isupper, filters.Filter)
        self.assertEqual(datatypes.unicode.isupper.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isnumeric, filters.Filter)
        self.assertEqual(datatypes.unicode.isnumeric.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.isspace, filters.Filter)
        self.assertEqual(datatypes.unicode.isspace.datatype, datatypes.unicode)
        self.assertIsInstance(datatypes.unicode.istitle, filters.Filter)
        self.assertEqual(datatypes.unicode.istitle.datatype, datatypes.unicode)

    def test_bytes(self):
        self.assertEqual(datatypes.bytes.py, bytes)
        self.assertEqual(datatypes.bytes.datatype, datatypes.bytes)
        self.assertTrue(isinstance(b'foo', datatypes.bytes))
        self.assertIsInstance(datatypes.bytes.exact, filters.Filter)
        self.assertEqual(datatypes.bytes.exact.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.iexact, filters.Filter)
        self.assertEqual(datatypes.bytes.iexact.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.contains, filters.Filter)
        self.assertEqual(datatypes.bytes.contains.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.icontains, filters.Filter)
        self.assertEqual(datatypes.bytes.icontains.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.startswith, filters.Filter)
        self.assertEqual(datatypes.bytes.startswith.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.istartswith, filters.Filter)
        self.assertEqual(datatypes.bytes.istartswith.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.endswith, filters.Filter)
        self.assertEqual(datatypes.bytes.endswith.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.iendswith, filters.Filter)
        self.assertEqual(datatypes.bytes.iendswith.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.len, filters.Filter)
        self.assertEqual(datatypes.bytes.len.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.lenlt, filters.Filter)
        self.assertEqual(datatypes.bytes.lenlt.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.lenlte, filters.Filter)
        self.assertEqual(datatypes.bytes.lenlte.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.lengt, filters.Filter)
        self.assertEqual(datatypes.bytes.lengt.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.lengte, filters.Filter)
        self.assertEqual(datatypes.bytes.lengte.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.isalnum, filters.Filter)
        self.assertEqual(datatypes.bytes.isalnum.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.isalnums, filters.Filter)
        self.assertEqual(datatypes.bytes.isalnums.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.isalpha, filters.Filter)
        self.assertEqual(datatypes.bytes.isalpha.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.isalphas, filters.Filter)
        self.assertEqual(datatypes.bytes.isalphas.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.isdigit, filters.Filter)
        self.assertEqual(datatypes.bytes.isdigit.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.islower, filters.Filter)
        self.assertEqual(datatypes.bytes.islower.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.isupper, filters.Filter)
        self.assertEqual(datatypes.bytes.isupper.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.isspace, filters.Filter)
        self.assertEqual(datatypes.bytes.isspace.datatype, datatypes.bytes)
        self.assertIsInstance(datatypes.bytes.istitle, filters.Filter)
        self.assertEqual(datatypes.bytes.istitle.datatype, datatypes.bytes)

    def test_bytearray(self):
        self.assertEqual(datatypes.bytearray.py, bytearray)
        self.assertEqual(datatypes.bytearray.datatype, datatypes.bytearray)
        self.assertTrue(isinstance(bytearray(b'foo'), datatypes.bytearray))
        self.assertIsInstance(datatypes.bytearray.exact, filters.Filter)
        self.assertEqual(datatypes.bytearray.exact.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.iexact, filters.Filter)
        self.assertEqual(datatypes.bytearray.iexact.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.contains, filters.Filter)
        self.assertEqual(datatypes.bytearray.contains.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.icontains, filters.Filter)
        self.assertEqual(datatypes.bytearray.icontains.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.startswith, filters.Filter)
        self.assertEqual(datatypes.bytearray.startswith.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.istartswith, filters.Filter)
        self.assertEqual(datatypes.bytearray.istartswith.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.endswith, filters.Filter)
        self.assertEqual(datatypes.bytearray.endswith.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.iendswith, filters.Filter)
        self.assertEqual(datatypes.bytearray.iendswith.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.len, filters.Filter)
        self.assertEqual(datatypes.bytearray.len.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.lenlt, filters.Filter)
        self.assertEqual(datatypes.bytearray.lenlt.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.lenlte, filters.Filter)
        self.assertEqual(datatypes.bytearray.lenlte.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.lengt, filters.Filter)
        self.assertEqual(datatypes.bytearray.lengt.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.lengte, filters.Filter)
        self.assertEqual(datatypes.bytearray.lengte.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.isalnum, filters.Filter)
        self.assertEqual(datatypes.bytearray.isalnum.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.isalnums, filters.Filter)
        self.assertEqual(datatypes.bytearray.isalnums.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.isalpha, filters.Filter)
        self.assertEqual(datatypes.bytearray.isalpha.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.isalphas, filters.Filter)
        self.assertEqual(datatypes.bytearray.isalphas.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.isdigit, filters.Filter)
        self.assertEqual(datatypes.bytearray.isdigit.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.islower, filters.Filter)
        self.assertEqual(datatypes.bytearray.islower.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.isupper, filters.Filter)
        self.assertEqual(datatypes.bytearray.isupper.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.isspace, filters.Filter)
        self.assertEqual(datatypes.bytearray.isspace.datatype, datatypes.bytearray)
        self.assertIsInstance(datatypes.bytearray.istitle, filters.Filter)
        self.assertEqual(datatypes.bytearray.istitle.datatype, datatypes.bytearray)

    def test_numeric(self):
        self.assertEqual(datatypes.numeric.py, compat.numeric)
        self.assertEqual(datatypes.numeric.pyex, bool)
        self.assertEqual(datatypes.numeric.datatype, datatypes.numeric)
        self.assertTrue(isinstance(1, datatypes.numeric))
        self.assertTrue(isinstance(1.1, datatypes.numeric))
        self.assertTrue(isinstance(2 ** 64, datatypes.numeric))
        self.assertIsInstance(datatypes.numeric.exact, filters.Filter)
        self.assertEqual(datatypes.numeric.exact.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.gt, filters.Filter)
        self.assertEqual(datatypes.numeric.gt.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.gte, filters.Filter)
        self.assertEqual(datatypes.numeric.gte.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.lt, filters.Filter)
        self.assertEqual(datatypes.numeric.lt.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.lte, filters.Filter)
        self.assertEqual(datatypes.numeric.lte.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.between, filters.Filter)
        self.assertEqual(datatypes.numeric.between.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.ebetween, filters.Filter)
        self.assertEqual(datatypes.numeric.ebetween.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.isodd, filters.Filter)
        self.assertEqual(datatypes.numeric.isodd.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.iseven, filters.Filter)
        self.assertEqual(datatypes.numeric.iseven.datatype, datatypes.numeric)
        self.assertIsInstance(datatypes.numeric.divisibleby, filters.Filter)
        self.assertEqual(datatypes.numeric.divisibleby.datatype, datatypes.numeric)

    def test_int(self):
        self.assertEqual(datatypes.int.py, int)
        self.assertEqual(datatypes.int.pyex, bool)
        self.assertEqual(datatypes.int.datatype, datatypes.int)
        self.assertTrue(isinstance(1, datatypes.int))
        self.assertIsInstance(datatypes.int.exact, filters.Filter)
        self.assertEqual(datatypes.int.exact.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.gt, filters.Filter)
        self.assertEqual(datatypes.int.gt.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.gte, filters.Filter)
        self.assertEqual(datatypes.int.gte.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.lt, filters.Filter)
        self.assertEqual(datatypes.int.lt.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.lte, filters.Filter)
        self.assertEqual(datatypes.int.lte.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.between, filters.Filter)
        self.assertEqual(datatypes.int.between.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.ebetween, filters.Filter)
        self.assertEqual(datatypes.int.ebetween.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.isodd, filters.Filter)
        self.assertEqual(datatypes.int.isodd.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.iseven, filters.Filter)
        self.assertEqual(datatypes.int.iseven.datatype, datatypes.int)
        self.assertIsInstance(datatypes.int.divisibleby, filters.Filter)
        self.assertEqual(datatypes.int.divisibleby.datatype, datatypes.int)

    def test_float(self):
        self.assertEqual(datatypes.float.py, float)
        self.assertEqual(datatypes.float.pyex, None)
        self.assertEqual(datatypes.float.datatype, datatypes.float)
        self.assertTrue(isinstance(1.0, datatypes.float))
        self.assertIsInstance(datatypes.float.exact, filters.Filter)
        self.assertEqual(datatypes.float.exact.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.gt, filters.Filter)
        self.assertEqual(datatypes.float.gt.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.gte, filters.Filter)
        self.assertEqual(datatypes.float.gte.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.lt, filters.Filter)
        self.assertEqual(datatypes.float.lt.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.lte, filters.Filter)
        self.assertEqual(datatypes.float.lte.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.between, filters.Filter)
        self.assertEqual(datatypes.float.between.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.ebetween, filters.Filter)
        self.assertEqual(datatypes.float.ebetween.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.isinteger, filters.Filter)
        self.assertEqual(datatypes.float.isinteger.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.isodd, filters.Filter)
        self.assertEqual(datatypes.float.isodd.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.iseven, filters.Filter)
        self.assertEqual(datatypes.float.iseven.datatype, datatypes.float)
        self.assertIsInstance(datatypes.float.divisibleby, filters.Filter)
        self.assertEqual(datatypes.float.divisibleby.datatype, datatypes.float)

    def test_long(self):
        self.assertEqual(datatypes.long.py, compat.long)
        self.assertEqual(datatypes.long.pyex, bool)
        self.assertEqual(datatypes.long.datatype, datatypes.long)
        self.assertTrue(isinstance(2 ** 64, datatypes.long))
        self.assertIsInstance(datatypes.long.exact, filters.Filter)
        self.assertEqual(datatypes.long.exact.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.gt, filters.Filter)
        self.assertEqual(datatypes.long.gt.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.gte, filters.Filter)
        self.assertEqual(datatypes.long.gte.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.lt, filters.Filter)
        self.assertEqual(datatypes.long.lt.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.lte, filters.Filter)
        self.assertEqual(datatypes.long.lte.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.between, filters.Filter)
        self.assertEqual(datatypes.long.between.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.ebetween, filters.Filter)
        self.assertEqual(datatypes.long.ebetween.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.isodd, filters.Filter)
        self.assertEqual(datatypes.long.isodd.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.iseven, filters.Filter)
        self.assertEqual(datatypes.long.iseven.datatype, datatypes.long)
        self.assertIsInstance(datatypes.long.divisibleby, filters.Filter)
        self.assertEqual(datatypes.long.divisibleby.datatype, datatypes.long)

    def test_complex(self):
        self.assertEqual(datatypes.complex.py, complex)
        self.assertEqual(datatypes.complex.datatype, datatypes.complex)
        self.assertTrue(isinstance(1j, datatypes.complex))
        self.assertIsInstance(datatypes.complex.exact, filters.Filter)
        self.assertEqual(datatypes.complex.exact.datatype, datatypes.complex)

    def test_iterable(self):
        from collections import Iterable
        self.assertEqual(datatypes.iterable.py, Iterable)
        self.assertEqual(datatypes.iterable.pyex, compat.stringlike)
        self.assertEqual(datatypes.iterable.datatype, datatypes.iterable)
        self.assertTrue(isinstance([], datatypes.iterable))
        self.assertTrue(isinstance((), datatypes.iterable))
        self.assertTrue(isinstance(set(), datatypes.iterable))
        self.assertTrue(isinstance({}, datatypes.iterable))
        self.assertIsInstance(datatypes.iterable.exact, filters.Filter)
        self.assertEqual(datatypes.iterable.exact.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.len, filters.Filter)
        self.assertEqual(datatypes.iterable.len.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.lenlt, filters.Filter)
        self.assertEqual(datatypes.iterable.lenlt.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.lenlte, filters.Filter)
        self.assertEqual(datatypes.iterable.lenlte.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.lengt, filters.Filter)
        self.assertEqual(datatypes.iterable.lengt.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.lengte, filters.Filter)
        self.assertEqual(datatypes.iterable.lengte.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.contains, filters.Filter)
        self.assertEqual(datatypes.iterable.contains.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.contains_all, filters.Filter)
        self.assertEqual(datatypes.iterable.contains_all.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.contains_any, filters.Filter)
        self.assertEqual(datatypes.iterable.contains_any.datatype, datatypes.iterable)
        self.assertIsInstance(datatypes.iterable.str_contains_str, filters.Filter)
        self.assertEqual(datatypes.iterable.str_contains_str.datatype, datatypes.iterable)

    def test_list(self):
        self.assertEqual(datatypes.list.py, list)
        self.assertEqual(datatypes.list.pyex, compat.stringlike)
        self.assertEqual(datatypes.list.datatype, datatypes.list)
        self.assertTrue(isinstance([], datatypes.list))
        self.assertIsInstance(datatypes.list.exact, filters.Filter)
        self.assertEqual(datatypes.list.exact.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.len, filters.Filter)
        self.assertEqual(datatypes.list.len.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.lenlt, filters.Filter)
        self.assertEqual(datatypes.list.lenlt.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.lenlte, filters.Filter)
        self.assertEqual(datatypes.list.lenlte.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.lengt, filters.Filter)
        self.assertEqual(datatypes.list.lengt.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.lengte, filters.Filter)
        self.assertEqual(datatypes.list.lengte.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.contains, filters.Filter)
        self.assertEqual(datatypes.list.contains.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.contains_all, filters.Filter)
        self.assertEqual(datatypes.list.contains_all.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.contains_any, filters.Filter)
        self.assertEqual(datatypes.list.contains_any.datatype, datatypes.list)
        self.assertIsInstance(datatypes.list.str_contains_str, filters.Filter)
        self.assertEqual(datatypes.list.str_contains_str.datatype, datatypes.list)

    def test_tuple(self):
        self.assertEqual(datatypes.tuple.py, tuple)
        self.assertEqual(datatypes.tuple.pyex, compat.stringlike)
        self.assertEqual(datatypes.tuple.datatype, datatypes.tuple)
        self.assertTrue(isinstance((), datatypes.tuple))
        self.assertIsInstance(datatypes.tuple.exact, filters.Filter)
        self.assertEqual(datatypes.tuple.exact.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.len, filters.Filter)
        self.assertEqual(datatypes.tuple.len.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.lenlt, filters.Filter)
        self.assertEqual(datatypes.tuple.lenlt.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.lenlte, filters.Filter)
        self.assertEqual(datatypes.tuple.lenlte.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.lengt, filters.Filter)
        self.assertEqual(datatypes.tuple.lengt.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.lengte, filters.Filter)
        self.assertEqual(datatypes.tuple.lengte.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.contains, filters.Filter)
        self.assertEqual(datatypes.tuple.contains.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.contains_all, filters.Filter)
        self.assertEqual(datatypes.tuple.contains_all.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.contains_any, filters.Filter)
        self.assertEqual(datatypes.tuple.contains_any.datatype, datatypes.tuple)
        self.assertIsInstance(datatypes.tuple.str_contains_str, filters.Filter)
        self.assertEqual(datatypes.tuple.str_contains_str.datatype, datatypes.tuple)

    def test_set(self):
        self.assertEqual(datatypes.set.py, set)
        self.assertEqual(datatypes.set.pyex, compat.stringlike)
        self.assertEqual(datatypes.set.datatype, datatypes.set)
        self.assertTrue(isinstance(set(), datatypes.set))
        self.assertIsInstance(datatypes.set.exact, filters.Filter)
        self.assertEqual(datatypes.set.exact.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.len, filters.Filter)
        self.assertEqual(datatypes.set.len.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.lenlt, filters.Filter)
        self.assertEqual(datatypes.set.lenlt.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.lenlte, filters.Filter)
        self.assertEqual(datatypes.set.lenlte.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.lengt, filters.Filter)
        self.assertEqual(datatypes.set.lengt.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.lengte, filters.Filter)
        self.assertEqual(datatypes.set.lengte.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.contains, filters.Filter)
        self.assertEqual(datatypes.set.contains.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.contains_all, filters.Filter)
        self.assertEqual(datatypes.set.contains_all.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.contains_any, filters.Filter)
        self.assertEqual(datatypes.set.contains_any.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.str_contains_str, filters.Filter)
        self.assertEqual(datatypes.set.str_contains_str.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.isdisjoint, filters.Filter)
        self.assertEqual(datatypes.set.isdisjoint.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.issubset, filters.Filter)
        self.assertEqual(datatypes.set.issubset.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.eissubset, filters.Filter)
        self.assertEqual(datatypes.set.eissubset.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.issuperset, filters.Filter)
        self.assertEqual(datatypes.set.issuperset.datatype, datatypes.set)
        self.assertIsInstance(datatypes.set.eissuperset, filters.Filter)
        self.assertEqual(datatypes.set.eissuperset.datatype, datatypes.set)

    def test_frozenset(self):
        self.assertEqual(datatypes.frozenset.py, frozenset)
        self.assertEqual(datatypes.frozenset.pyex, compat.stringlike)
        self.assertEqual(datatypes.frozenset.datatype, datatypes.frozenset)
        self.assertTrue(isinstance(frozenset(), datatypes.frozenset))
        self.assertIsInstance(datatypes.frozenset.exact, filters.Filter)
        self.assertEqual(datatypes.frozenset.exact.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.len, filters.Filter)
        self.assertEqual(datatypes.frozenset.len.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.lenlt, filters.Filter)
        self.assertEqual(datatypes.frozenset.lenlt.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.lenlte, filters.Filter)
        self.assertEqual(datatypes.frozenset.lenlte.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.lengt, filters.Filter)
        self.assertEqual(datatypes.frozenset.lengt.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.lengte, filters.Filter)
        self.assertEqual(datatypes.frozenset.lengte.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.contains, filters.Filter)
        self.assertEqual(datatypes.frozenset.contains.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.contains_all, filters.Filter)
        self.assertEqual(datatypes.frozenset.contains_all.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.contains_any, filters.Filter)
        self.assertEqual(datatypes.frozenset.contains_any.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.str_contains_str, filters.Filter)
        self.assertEqual(datatypes.frozenset.str_contains_str.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.isdisjoint, filters.Filter)
        self.assertEqual(datatypes.frozenset.isdisjoint.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.issubset, filters.Filter)
        self.assertEqual(datatypes.frozenset.issubset.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.eissubset, filters.Filter)
        self.assertEqual(datatypes.frozenset.eissubset.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.issuperset, filters.Filter)
        self.assertEqual(datatypes.frozenset.issuperset.datatype, datatypes.frozenset)
        self.assertIsInstance(datatypes.frozenset.eissuperset, filters.Filter)
        self.assertEqual(datatypes.frozenset.eissuperset.datatype, datatypes.frozenset)

    def test_dict(self):
        self.assertEqual(datatypes.dict.py, dict)
        self.assertEqual(datatypes.dict.pyex, compat.stringlike)
        self.assertEqual(datatypes.dict.datatype, datatypes.dict)
        self.assertTrue(isinstance({}, datatypes.dict))
        self.assertIsInstance(datatypes.dict.exact, filters.Filter)
        self.assertEqual(datatypes.dict.exact.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.len, filters.Filter)
        self.assertEqual(datatypes.dict.len.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.lenlt, filters.Filter)
        self.assertEqual(datatypes.dict.lenlt.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.lenlte, filters.Filter)
        self.assertEqual(datatypes.dict.lenlte.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.lengt, filters.Filter)
        self.assertEqual(datatypes.dict.lengt.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.lengte, filters.Filter)
        self.assertEqual(datatypes.dict.lengte.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.contains_key, filters.Filter)
        self.assertEqual(datatypes.dict.contains_key.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.contains_all_keys, filters.Filter)
        self.assertEqual(datatypes.dict.contains_all_keys.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.contains_any_keys, filters.Filter)
        self.assertEqual(datatypes.dict.contains_any_keys.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.key_contains_str, filters.Filter)
        self.assertEqual(datatypes.dict.key_contains_str.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.contains_value, filters.Filter)
        self.assertEqual(datatypes.dict.contains_value.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.contains_all_values, filters.Filter)
        self.assertEqual(datatypes.dict.contains_all_values.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.contains_any_values, filters.Filter)
        self.assertEqual(datatypes.dict.contains_any_values.datatype, datatypes.dict)
        self.assertIsInstance(datatypes.dict.value_contains_str, filters.Filter)
        self.assertEqual(datatypes.dict.value_contains_str.datatype, datatypes.dict)