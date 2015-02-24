from . import unittest
from instructions import filters, datatypes, exceptions


class FilterTestCase(unittest.TestCase):
    def setUp(self):
        self.filter1 = filters.Filter('{0} == 1')(1)
        self.filter2 = filters.Filter('{0} == 1')(2)

    def test_initialization_errors(self):
        self.assertRaises(exceptions.FilterImplementationError, lambda: filters.Filter())
        self.assertRaises(exceptions.FilterImplementationError, lambda: filters.Filter(names=[1, 2, 3]))
        self.assertRaises(exceptions.FilterImplementationError, lambda: filters.Filter(accept_types=int))

    def test_usage_errors(self):
        self.assertRaises(exceptions.FilterUsageError, lambda: filters.Filter('{0} == foo')('foo', 'bar'))
        self.assertRaises(exceptions.FilterUsageError, lambda: filters.Filter('{0}', accept_types=(int,))('foo'))

    def test_call(self):
        self.assertEqual(self.filter1.condition, '1 == 1')

    def test_or(self):
        self.assertEqual((self.filter1 | self.filter2).condition, '1 == 1 or 2 == 1')

    def test_and(self):
        self.assertEqual((self.filter1 & self.filter2).condition, '1 == 1 and 2 == 1')

    def test_not(self):
        self.assertEqual((~self.filter1).condition, 'not 1 == 1')

    def test_str(self):
        self.assertEqual(str(self.filter1), '1 == 1')

    def test_repr(self):
        self.assertEqual(repr(self.filter1), '<instructions.filters.Filter "1 == 1">')


class AugmentedFilterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.footype = type('Foo', (datatypes.DataType,), {
            'py': str,
            'augmentation': 'foo',
            'filter': filters.AugmentedFilter('{0} == foo')
        })
        cls.bartype = type('Bar', (cls.footype,), {'augmentation': 'bar'})
        cls.baztype = type('Baz', (cls.footype,), {'augmentation': None})

    def test_attributes(self):
        self.assertTrue(hasattr(filters.AugmentedFilter, 'is_augmented'))
        self.assertTrue(hasattr(filters.AugmentedFilter, 'org_condition'))

    def test_augmentation(self):
        self.assertEqual(self.footype.filter.condition, 'foo == foo')

    def test_augmentation_changed(self):
        self.assertEqual(self.bartype.filter.condition, 'bar == foo')

    def test_augmentation_disabled(self):
        self.assertEqual(self.baztype.filter.condition, '{0} == foo')
