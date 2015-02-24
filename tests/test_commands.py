import types

from . import unittest
from instructions import commands, datatypes, filters, exceptions


class AssertsCollection(object):
    def find_prototype_asserts(self, filtr, iterator, value):
        keys = ('nolimit', 'limit1', 'limit2', 'level1', 'level2', 'ignore')
        ignore = tuple if not isinstance(value, tuple) else list

        if not isinstance(value, dict) or not all(key in value for key in keys):
            value = {
                'nolimit': [value, value, value],
                'limit1': value,
                'limit2': [value, value],
                'level1': [value, value],
                'level2': [value, value, value],
                'ignore': [value, value]
            }

        self.assertEqual(list(commands.find(filtr).inside(iterator)), value['nolimit'])
        self.assertEqual(commands.find(filtr, limit=1).inside(iterator), value['limit1'])
        self.assertEqual(list(commands.find(filtr, limit=2).inside(iterator)), value['limit2'])
        self.assertEqual(list(commands.find(filtr, level=1).inside(iterator)), value['level1'])
        self.assertEqual(list(commands.find(filtr, level=2).inside(iterator)), value['level2'])
        self.assertEqual(list(commands.find(filtr, ignore=(ignore,)).inside(iterator)), value['ignore'])

    def find_compound_asserts(self, filtr, args, iterator, value):
        command = getattr(commands, 'find{0}'.format(filtr))
        keys = ('nolimit', 'limit1', 'limit2', 'level1', 'level2', 'ignore')
        ignore = tuple if not isinstance(value, tuple) else list

        if not isinstance(value, dict) or not all(key in value for key in keys):
            value = {
                'nolimit': [value, value, value],
                'limit1': value,
                'limit2': [value, value],
                'level1': [value, value],
                'level2': [value, value, value],
                'ignore': [value, value]
            }

        self.assertEqual(list(command(*args).inside(iterator)), value['nolimit'])
        self.assertEqual(command(*args, limit=1).inside(iterator), value['limit1'])
        self.assertEqual(list(command(*args, limit=2).inside(iterator)), value['limit2'])
        self.assertEqual(list(command(*args, level=1).inside(iterator)), value['level1'])
        self.assertEqual(list(command(*args, level=2).inside(iterator)), value['level2'])
        self.assertEqual(list(command(*args, ignore=(ignore,)).inside(iterator)), value['ignore'])

    def first_prototype_asserts(self, filtr, iterator, value):
        self.assertEqual(commands.first(filtr).inside(iterator), value)

    def first_compound_asserts(self, filtr, args, iterator, value):
        self.assertEqual(getattr(commands, 'first{0}'.format(filtr))(*args).inside(iterator), value)

    def last_prototype_asserts(self, filtr, iterator, value):
        self.assertEqual(commands.last(filtr).inside(iterator), value)

    def last_compound_asserts(self, filtr, args, iterator, value):
        self.assertEqual(getattr(commands, 'last{0}'.format(filtr))(*args).inside(iterator), value)

    def exists_prototype_asserts(self, filtr, iterator, value):
        self.assertEqual(commands.exists(filtr).inside(iterator), value)

    def exists_compound_asserts(self, filtr, args, iterator, value):
        self.assertEqual(getattr(commands, 'exists{0}'.format(filtr))(*args).inside(iterator), value)

    def count_prototype_asserts(self, filtr, iterator, value):
        self.assertEqual(commands.count(filtr).inside(iterator), value)
        self.assertEqual(commands.count(filtr, limit=1).inside(iterator), 1)

    def count_compound_asserts(self, filtr, args, iterator, value):
        self.assertEqual(getattr(commands, 'count{0}'.format(filtr))(*args).inside(iterator), value)


class BaseCommandTestCase(unittest.TestCase):
    def test_filter_type_error(self):
        self.assertRaises(exceptions.FilterTypeError, lambda: commands.find('foo'))

    def test_filter_without_datatype(self):
        self.assertEqual(commands.find(filters.Filter('True')).raw_condition, 'True')

    def test_command_indict_option(self):
        searchable = [{'fo': 'ba'}]
        self.assertEqual(list(commands.find(datatypes.string.exact('fo'), indict='keys').inside(searchable)), ['fo'])
        self.assertEqual(list(commands.find(datatypes.string.exact('ba'), indict='values').inside(searchable)), ['ba'])

    def test_command_option_errors(self):
        self.assertRaises(exceptions.CommandOptionTypeError, lambda: commands.find(datatypes.bool, limit='foo'))
        self.assertRaises(exceptions.CommandOptionTypeError, lambda: commands.find(datatypes.bool, level='foo'))
        self.assertRaises(exceptions.CommandOptionTypeError, lambda: commands.find(datatypes.bool, ignore='foo'))
        self.assertRaises(exceptions.CommandOptionError, lambda: commands.find(datatypes.bool, indict='foo'))

    def test_command_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            class BadCommand(commands.Command):
                pass
            BadCommand(datatypes.bool).inside([])


class FindCommandTestCase(unittest.TestCase):
    def test_prototype(self):
        self.assertIsInstance(commands.find(datatypes.bool), commands.Command)
        self.assertIsInstance(commands.find(datatypes.bool).inside([]), types.GeneratorType)


class FindCommandBoolDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.bool.exact(True), (True, True, (True,)), True)

    def test_compound_exact(self):
        self.find_compound_asserts('bool__exact', [True], (True, True, (True,)), True)

    def test_prototype_true(self):
        self.find_prototype_asserts(datatypes.bool.true, (True, True, (True,)), True)

    def test_compound_true(self):
        self.find_compound_asserts('bool__true', [], (True, True, (True,)), True)

    def test_prototype_false(self):
        self.find_prototype_asserts(datatypes.bool.false, (False, False, (False,)), False)

    def test_compound_false(self):
        self.find_compound_asserts('bool__false', [], (False, False, (False,)), False)


class FindCommandStringDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = 'foo'

    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.string.exact(self.foo), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_exact(self):
        self.find_compound_asserts('string__exact', [self.foo], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_iexact(self):
        self.find_prototype_asserts(datatypes.string.iexact('FOO'), (self.foo, 'fOo', ('Foo',)), {
            'nolimit': [self.foo, 'fOo', 'Foo'],
            'limit1': self.foo,
            'limit2': [self.foo, 'fOo'],
            'level1': [self.foo, 'fOo'],
            'level2': [self.foo, 'fOo', 'Foo'],
            'ignore': [self.foo, 'fOo']
        })

    def test_compound_iexact(self):
        self.find_compound_asserts('string__iexact', ['FOO'], (self.foo, 'fOo', ('Foo',)), {
            'nolimit': [self.foo, 'fOo', 'Foo'],
            'limit1': self.foo,
            'limit2': [self.foo, 'fOo'],
            'level1': [self.foo, 'fOo'],
            'level2': [self.foo, 'fOo', 'Foo'],
            'ignore': [self.foo, 'fOo']
        })

    def test_prototype_contains(self):
        self.find_prototype_asserts(datatypes.string.contains('o'), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_contains(self):
        self.find_compound_asserts('string__contains', ['o'], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_icontains(self):
        self.find_prototype_asserts(datatypes.string.icontains('O'), (self.foo, 'fOo', ('Foo',)), {
            'nolimit': [self.foo, 'fOo', 'Foo'],
            'limit1': self.foo,
            'limit2': [self.foo, 'fOo'],
            'level1': [self.foo, 'fOo'],
            'level2': [self.foo, 'fOo', 'Foo'],
            'ignore': [self.foo, 'fOo']
        })

    def test_compound_icontains(self):
        self.find_compound_asserts('string__icontains', ['O'], (self.foo, 'fOo', ('Foo',)), {
            'nolimit': [self.foo, 'fOo', 'Foo'],
            'limit1': self.foo,
            'limit2': [self.foo, 'fOo'],
            'level1': [self.foo, 'fOo'],
            'level2': [self.foo, 'fOo', 'Foo'],
            'ignore': [self.foo, 'fOo']
        })

    def test_prototype_startswith(self):
        self.find_prototype_asserts(datatypes.string.startswith('f'), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_startswith(self):
        self.find_compound_asserts('string__startswith', ['f'], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_istartswith(self):
        self.find_prototype_asserts(datatypes.string.istartswith('F'), (self.foo, 'fOo', ('Foo',)), {
            'nolimit': [self.foo, 'fOo', 'Foo'],
            'limit1': self.foo,
            'limit2': [self.foo, 'fOo'],
            'level1': [self.foo, 'fOo'],
            'level2': [self.foo, 'fOo', 'Foo'],
            'ignore': [self.foo, 'fOo']
        })

    def test_compound_istartswith(self):
        self.find_compound_asserts('string__istartswith', ['F'], (self.foo, 'fOo', ('Foo',)), {
            'nolimit': [self.foo, 'fOo', 'Foo'],
            'limit1': self.foo,
            'limit2': [self.foo, 'fOo'],
            'level1': [self.foo, 'fOo'],
            'level2': [self.foo, 'fOo', 'Foo'],
            'ignore': [self.foo, 'fOo']
        })

    def test_prototype_endswith(self):
        self.find_prototype_asserts(datatypes.string.endswith('oo'), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_endswith(self):
        self.find_compound_asserts('string__endswith', ['oo'], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_iendswith(self):
        self.find_prototype_asserts(datatypes.string.iendswith('OO'), (self.foo, 'fOo', ('Foo',)), {
            'nolimit': [self.foo, 'fOo', 'Foo'],
            'limit1': self.foo,
            'limit2': [self.foo, 'fOo'],
            'level1': [self.foo, 'fOo'],
            'level2': [self.foo, 'fOo', 'Foo'],
            'ignore': [self.foo, 'fOo']
        })

    def test_compound_iendswith(self):
        self.find_compound_asserts('string__iendswith', ['OO'], (self.foo, 'fOo', ('Foo',)), {
            'nolimit': [self.foo, 'fOo', 'Foo'],
            'limit1': self.foo,
            'limit2': [self.foo, 'fOo'],
            'level1': [self.foo, 'fOo'],
            'level2': [self.foo, 'fOo', 'Foo'],
            'ignore': [self.foo, 'fOo']
        })

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.string.len(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_len(self):
        self.find_compound_asserts('string__len', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.string.lenlt(4), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lenlt(self):
        self.find_compound_asserts('string__lenlt', [4], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.string.lenlte(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lenlte(self):
        self.find_compound_asserts('string__lenlte', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lengt(self):
        self.find_prototype_asserts(datatypes.string.lengt(2), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lengt(self):
        self.find_compound_asserts('string__lengt', [2], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lengte(self):
        self.find_prototype_asserts(datatypes.string.lengte(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lengte(self):
        self.find_compound_asserts('string__lengte', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalnum(self):
        self.find_prototype_asserts(datatypes.string.isalnum(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_isalnum(self):
        self.find_compound_asserts('string__isalnum', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalnums(self):
        self.find_prototype_asserts(datatypes.string.isalnums(), ('fo o', 'f Oo', ('Fo o',)), {
            'nolimit': ['fo o', 'f Oo', 'Fo o'],
            'limit1': 'fo o',
            'limit2': ['fo o', 'f Oo'],
            'level1': ['fo o', 'f Oo'],
            'level2': ['fo o', 'f Oo', 'Fo o'],
            'ignore': ['fo o', 'f Oo']
        })

    def test_compound_isalnums(self):
        self.find_compound_asserts('string__isalnums', [], ('fo o', 'f Oo', ('Fo o',)), {
            'nolimit': ['fo o', 'f Oo', 'Fo o'],
            'limit1': 'fo o',
            'limit2': ['fo o', 'f Oo'],
            'level1': ['fo o', 'f Oo'],
            'level2': ['fo o', 'f Oo', 'Fo o'],
            'ignore': ['fo o', 'f Oo']
        })

    def test_prototype_isalpha(self):
        self.find_prototype_asserts(datatypes.string.isalpha(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_isalpha(self):
        self.find_compound_asserts('string__isalpha', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalphas(self):
        self.find_prototype_asserts(datatypes.string.isalphas(), ('fo o', 'f Oo', ('Fo o',)), {
            'nolimit': ['fo o', 'f Oo', 'Fo o'],
            'limit1': 'fo o',
            'limit2': ['fo o', 'f Oo'],
            'level1': ['fo o', 'f Oo'],
            'level2': ['fo o', 'f Oo', 'Fo o'],
            'ignore': ['fo o', 'f Oo']
        })

    def test_compound_isalphas(self):
        self.find_compound_asserts('string__isalphas', [], ('fo o', 'f Oo', ('Fo o',)), {
            'nolimit': ['fo o', 'f Oo', 'Fo o'],
            'limit1': 'fo o',
            'limit2': ['fo o', 'f Oo'],
            'level1': ['fo o', 'f Oo'],
            'level2': ['fo o', 'f Oo', 'Fo o'],
            'ignore': ['fo o', 'f Oo']
        })

    def test_prototype_isdigit(self):
        self.find_prototype_asserts(datatypes.string.isdigit(), ('1', '1', ('1',)), '1')

    def test_compound_isdigit(self):
        self.find_compound_asserts('string__isdigit', [], ('1', '1', ('1',)), '1')

    def test_prototype_islower(self):
        self.find_prototype_asserts(datatypes.string.islower(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_islower(self):
        self.find_compound_asserts('string__islower', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isupper(self):
        self.find_prototype_asserts(datatypes.string.isupper(), ('FOO', 'FOO', ('FOO',)), 'FOO')

    def test_compound_isupper(self):
        self.find_compound_asserts('string__isupper', [], ('FOO', 'FOO', ('FOO',)), 'FOO')

    def test_prototype_isspace(self):
        self.find_prototype_asserts(datatypes.string.isspace(), ('    ', '    ', ('    ',)), '    ')

    def test_compound_isspace(self):
        self.find_compound_asserts('string__isspace', [], ('    ', '    ', ('    ',)), '    ')

    def test_prototype_istitle(self):
        self.find_prototype_asserts(datatypes.string.istitle(), ('Foo', 'Foo', ('Foo',)), 'Foo')

    def test_compound_istitle(self):
        self.find_compound_asserts('string__istitle', [], ('Foo', 'Foo', ('Foo',)), 'Foo')


class FindCommandUnicodeDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'.decode()

    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.unicode.exact(self.foo), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_exact(self):
        self.find_compound_asserts('unicode__exact', [self.foo], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_iexact(self):
        self.find_prototype_asserts(datatypes.unicode.iexact(self.foo), (self.foo, self.foo, (self.foo,)), {
            'nolimit': [self.foo, self.foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, self.foo],
            'level1': [self.foo, self.foo],
            'level2': [self.foo, self.foo, self.foo],
            'ignore': [self.foo, self.foo]
        })

    def test_compound_iexact(self):
        self.find_compound_asserts('unicode__iexact', [self.foo], (self.foo, self.foo, (self.foo,)), {
            'nolimit': [self.foo, self.foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, self.foo],
            'level1': [self.foo, self.foo],
            'level2': [self.foo, self.foo, self.foo],
            'ignore': [self.foo, self.foo]
        })

    def test_prototype_contains(self):
        self.find_prototype_asserts(datatypes.unicode.contains('o'), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_contains(self):
        self.find_compound_asserts('unicode__contains', ['o'], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_icontains(self):
        self.find_prototype_asserts(datatypes.unicode.icontains('O'), (self.foo, self.foo, (self.foo,)), {
            'nolimit': [self.foo, self.foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, self.foo],
            'level1': [self.foo, self.foo],
            'level2': [self.foo, self.foo, self.foo],
            'ignore': [self.foo, self.foo]
        })

    def test_compound_icontains(self):
        self.find_compound_asserts('unicode__icontains', ['O'], (self.foo, self.foo, (self.foo,)), {
            'nolimit': [self.foo, self.foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, self.foo],
            'level1': [self.foo, self.foo],
            'level2': [self.foo, self.foo, self.foo],
            'ignore': [self.foo, self.foo]
        })

    def test_prototype_startswith(self):
        self.find_prototype_asserts(
            datatypes.unicode.startswith(b'f'.decode()),
            (self.foo, self.foo, (self.foo,)), self.foo
        )

    def test_compound_startswith(self):
        self.find_compound_asserts('unicode__startswith', [b'f'.decode()], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_istartswith(self):
        self.find_prototype_asserts(datatypes.unicode.istartswith(b'f'.decode()), (self.foo, self.foo, (self.foo,)), {
            'nolimit': [self.foo, self.foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, self.foo],
            'level1': [self.foo, self.foo],
            'level2': [self.foo, self.foo, self.foo],
            'ignore': [self.foo, self.foo]
        })

    def test_compound_istartswith(self):
        self.find_compound_asserts('unicode__istartswith', [b'f'.decode()], (self.foo, self.foo, (self.foo,)), {
            'nolimit': [self.foo, self.foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, self.foo],
            'level1': [self.foo, self.foo],
            'level2': [self.foo, self.foo, self.foo],
            'ignore': [self.foo, self.foo]
        })

    def test_prototype_endswith(self):
        self.find_prototype_asserts(
            datatypes.unicode.endswith(b'oo'.decode()),
            (self.foo, self.foo, (self.foo,)), self.foo
        )

    def test_compound_endswith(self):
        self.find_compound_asserts('unicode__endswith', [b'oo'.decode()], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_iendswith(self):
        self.find_prototype_asserts(datatypes.unicode.iendswith(b'oo'.decode()), (self.foo, self.foo, (self.foo,)), {
            'nolimit': [self.foo, self.foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, self.foo],
            'level1': [self.foo, self.foo],
            'level2': [self.foo, self.foo, self.foo],
            'ignore': [self.foo, self.foo]
        })

    def test_compound_iendswith(self):
        self.find_compound_asserts('unicode__iendswith', [b'oo'.decode()], (self.foo, self.foo, (self.foo,)), {
            'nolimit': [self.foo, self.foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, self.foo],
            'level1': [self.foo, self.foo],
            'level2': [self.foo, self.foo, self.foo],
            'ignore': [self.foo, self.foo]
        })

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.unicode.len(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_len(self):
        self.find_compound_asserts('unicode__len', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.unicode.lenlt(4), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lenlt(self):
        self.find_compound_asserts('unicode__lenlt', [4], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.unicode.lenlte(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lenlte(self):
        self.find_compound_asserts('unicode__lenlte', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lengt(self):
        self.find_prototype_asserts(datatypes.unicode.lengt(2), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lengt(self):
        self.find_compound_asserts('unicode__lengt', [2], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lengte(self):
        self.find_prototype_asserts(datatypes.unicode.lengte(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lengte(self):
        self.find_compound_asserts('unicode__lengte', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalnum(self):
        self.find_prototype_asserts(datatypes.unicode.isalnum(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_isalnum(self):
        self.find_compound_asserts('unicode__isalnum', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalnums(self):
        foo = b'f oo'.decode()
        self.find_prototype_asserts(datatypes.unicode.isalnums(), (foo, foo, (foo,)), foo)

    def test_compound_isalnums(self):
        foo = b'f oo'.decode()
        self.find_compound_asserts('unicode__isalnums', [], (foo, foo, (foo,)), foo)

    def test_prototype_isalpha(self):
        self.find_prototype_asserts(datatypes.unicode.isalpha(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_isalpha(self):
        self.find_compound_asserts('unicode__isalpha', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalphas(self):
        foo = b'f oo'.decode()
        self.find_prototype_asserts(datatypes.unicode.isalphas(), (foo, foo, (foo,)), foo)

    def test_compound_isalphas(self):
        foo = b'f oo'.decode()
        self.find_compound_asserts('unicode__isalphas', [], (foo, foo, (foo,)), foo)

    def test_prototype_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.find_prototype_asserts(datatypes.unicode.isdecimal(), (decimal, decimal, (decimal,)), decimal)

    def test_compound_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.find_compound_asserts('unicode__isdecimal', [], (decimal, decimal, (decimal,)), decimal)

    def test_prototype_isdigit(self):
        one = b'1'.decode()
        self.find_prototype_asserts(datatypes.unicode.isdigit(), (one, one, (one,)), one)

    def test_compound_isdigit(self):
        one = b'1'.decode()
        self.find_compound_asserts('unicode__isdigit', [], (one, one, (one,)), one)

    def test_prototype_islower(self):
        self.find_prototype_asserts(datatypes.unicode.islower(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_islower(self):
        self.find_compound_asserts('unicode__islower', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isupper(self):
        upper = b'FOO'.decode()
        self.find_prototype_asserts(datatypes.unicode.isupper(), (upper, upper, (upper,)), upper)

    def test_compound_isupper(self):
        upper = b'FOO'.decode()
        self.find_compound_asserts('unicode__isupper', [], (upper, upper, (upper,)), upper)

    def test_prototype_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.find_prototype_asserts(datatypes.unicode.isnumeric(), (numeric, numeric, (numeric,)), numeric)

    def test_compound_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.find_compound_asserts('unicode__isnumeric', [], (numeric, numeric, (numeric,)), numeric)

    def test_prototype_isspace(self):
        space = b'    '.decode()
        self.find_prototype_asserts(datatypes.unicode.isspace(), (space, space, (space,)), space)

    def test_compound_isspace(self):
        space = b'    '.decode()
        self.find_compound_asserts('unicode__isspace', [], (space, space, (space,)), space)

    def test_prototype_istitle(self):
        foo = b'Foo'.decode()
        self.find_prototype_asserts(datatypes.unicode.istitle(), (foo, foo, (foo,)), foo)

    def test_compound_istitle(self):
        foo = b'Foo'.decode()
        self.find_compound_asserts('unicode__istitle', [], (foo, foo, (foo,)), foo)


class FindCommandBytesDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.bytes.exact(b'foo'), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_exact(self):
        self.find_compound_asserts('bytes__exact', [b'foo'], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_iexact(self):
        self.find_prototype_asserts(datatypes.bytes.iexact(b'fOO'), (b'foo', b'fOo', (b'foo',)), {
            'nolimit': [b'foo', b'fOo', b'foo'],
            'limit1': b'foo',
            'limit2': [b'foo', b'fOo'],
            'level1': [b'foo', b'fOo'],
            'level2': [b'foo', b'fOo', b'foo'],
            'ignore': [b'foo', b'fOo']
        })

    def test_compound_iexact(self):
        self.find_compound_asserts('bytes__iexact', [b'fOO'], (b'foo', b'fOo', (b'foo',)), {
            'nolimit': [b'foo', b'fOo', b'foo'],
            'limit1': b'foo',
            'limit2': [b'foo', b'fOo'],
            'level1': [b'foo', b'fOo'],
            'level2': [b'foo', b'fOo', b'foo'],
            'ignore': [b'foo', b'fOo']
        })

    def test_prototype_contains(self):
        self.find_prototype_asserts(datatypes.bytes.contains(b'o'), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_contains(self):
        self.find_compound_asserts('bytes__contains', [b'o'], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_icontains(self):
        self.find_prototype_asserts(datatypes.bytes.icontains(b'O'), (b'foo', b'fOo', (b'foo',)), {
            'nolimit': [b'foo', b'fOo', b'foo'],
            'limit1': b'foo',
            'limit2': [b'foo', b'fOo'],
            'level1': [b'foo', b'fOo'],
            'level2': [b'foo', b'fOo', b'foo'],
            'ignore': [b'foo', b'fOo']
        })

    def test_compound_icontains(self):
        self.find_compound_asserts('bytes__icontains', [b'O'], (b'foo', b'fOo', (b'foo',)), {
            'nolimit': [b'foo', b'fOo', b'foo'],
            'limit1': b'foo',
            'limit2': [b'foo', b'fOo'],
            'level1': [b'foo', b'fOo'],
            'level2': [b'foo', b'fOo', b'foo'],
            'ignore': [b'foo', b'fOo']
        })

    def test_prototype_startswith(self):
        self.find_prototype_asserts(datatypes.bytes.startswith(b'f'), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_startswith(self):
        self.find_compound_asserts('bytes__startswith', [b'f'], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_istartswith(self):
        self.find_prototype_asserts(datatypes.bytes.istartswith(b'f'), (b'foo', b'fOo', (b'foo',)), {
            'nolimit': [b'foo', b'fOo', b'foo'],
            'limit1': b'foo',
            'limit2': [b'foo', b'fOo'],
            'level1': [b'foo', b'fOo'],
            'level2': [b'foo', b'fOo', b'foo'],
            'ignore': [b'foo', b'fOo']
        })

    def test_compound_istartswith(self):
        self.find_compound_asserts('bytes__istartswith', [b'f'], (b'foo', b'fOo', (b'foo',)), {
            'nolimit': [b'foo', b'fOo', b'foo'],
            'limit1': b'foo',
            'limit2': [b'foo', b'fOo'],
            'level1': [b'foo', b'fOo'],
            'level2': [b'foo', b'fOo', b'foo'],
            'ignore': [b'foo', b'fOo']
        })

    def test_prototype_endswith(self):
        self.find_prototype_asserts(datatypes.bytes.endswith(b'oo'), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_endswith(self):
        self.find_compound_asserts('bytes__endswith', [b'oo'], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_iendswith(self):
        self.find_prototype_asserts(datatypes.bytes.iendswith(b'OO'), (b'foo', b'fOo', (b'foo',)), {
            'nolimit': [b'foo', b'fOo', b'foo'],
            'limit1': b'foo',
            'limit2': [b'foo', b'fOo'],
            'level1': [b'foo', b'fOo'],
            'level2': [b'foo', b'fOo', b'foo'],
            'ignore': [b'foo', b'fOo']
        })

    def test_compound_iendswith(self):
        self.find_compound_asserts('bytes__iendswith', [b'OO'], (b'foo', b'fOo', (b'foo',)), {
            'nolimit': [b'foo', b'fOo', b'foo'],
            'limit1': b'foo',
            'limit2': [b'foo', b'fOo'],
            'level1': [b'foo', b'fOo'],
            'level2': [b'foo', b'fOo', b'foo'],
            'ignore': [b'foo', b'fOo']
        })

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.bytes.len(3), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_len(self):
        self.find_compound_asserts('bytes__len', [3], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.bytes.lenlt(4), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_lenlt(self):
        self.find_compound_asserts('bytes__lenlt', [4], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.bytes.lenlte(3), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_lenlte(self):
        self.find_compound_asserts('bytes__lenlte', [3], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_lengt(self):
        self.find_prototype_asserts(datatypes.bytes.lengt(2), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_lengt(self):
        self.find_compound_asserts('bytes__lengt', [2], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_lengte(self):
        self.find_prototype_asserts(datatypes.bytes.lengte(3), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_lengte(self):
        self.find_compound_asserts('bytes__lengte', [3], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_isalnum(self):
        self.find_prototype_asserts(datatypes.bytes.isalnum(), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_isalnum(self):
        self.find_compound_asserts('bytes__isalnum', [], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_isalnums(self):
        self.find_prototype_asserts(datatypes.bytes.isalnums(), (b'fo o', b'f Oo', (b'fo o',)), {
            'nolimit': [b'fo o', b'f Oo', b'fo o'],
            'limit1': b'fo o',
            'limit2': [b'fo o', b'f Oo'],
            'level1': [b'fo o', b'f Oo'],
            'level2': [b'fo o', b'f Oo', b'fo o'],
            'ignore': [b'fo o', b'f Oo']
        })

    def test_compound_isalnums(self):
        self.find_compound_asserts('bytes__isalnums', [], (b'fo o', b'f Oo', (b'fo o',)), {
            'nolimit': [b'fo o', b'f Oo', b'fo o'],
            'limit1': b'fo o',
            'limit2': [b'fo o', b'f Oo'],
            'level1': [b'fo o', b'f Oo'],
            'level2': [b'fo o', b'f Oo', b'fo o'],
            'ignore': [b'fo o', b'f Oo']
        })

    def test_prototype_isalpha(self):
        self.find_prototype_asserts(datatypes.bytes.isalpha(), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_isalpha(self):
        self.find_compound_asserts('bytes__isalpha', [], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_isalphas(self):
        self.find_prototype_asserts(datatypes.bytes.isalphas(), (b'fo o', b'f Oo', (b'fo o',)), {
            'nolimit': [b'fo o', b'f Oo', b'fo o'],
            'limit1': b'fo o',
            'limit2': [b'fo o', b'f Oo'],
            'level1': [b'fo o', b'f Oo'],
            'level2': [b'fo o', b'f Oo', b'fo o'],
            'ignore': [b'fo o', b'f Oo']
        })

    def test_compound_isalphas(self):
        self.find_compound_asserts('bytes__isalphas', [], (b'fo o', b'f Oo', (b'fo o',)), {
            'nolimit': [b'fo o', b'f Oo', b'fo o'],
            'limit1': b'fo o',
            'limit2': [b'fo o', b'f Oo'],
            'level1': [b'fo o', b'f Oo'],
            'level2': [b'fo o', b'f Oo', b'fo o'],
            'ignore': [b'fo o', b'f Oo']
        })

    def test_prototype_isdigit(self):
        self.find_prototype_asserts(datatypes.bytes.isdigit(), (b'1', b'1', (b'1',)), b'1')

    def test_compound_isdigit(self):
        self.find_compound_asserts('bytes__isdigit', [], (b'1', b'1', (b'1',)), b'1')

    def test_prototype_islower(self):
        self.find_prototype_asserts(datatypes.bytes.islower(), (b'foo', b'foo', (b'foo',)), b'foo')

    def test_compound_islower(self):
        self.find_compound_asserts('bytes__islower', [], (b'foo', b'foo', (b'foo',)), b'foo')

    def test_prototype_isupper(self):
        self.find_prototype_asserts(datatypes.bytes.isupper(), (b'FOO', b'FOO', (b'FOO',)), b'FOO')

    def test_compound_isupper(self):
        self.find_compound_asserts('bytes__isupper', [], (b'FOO', b'FOO', (b'FOO',)), b'FOO')

    def test_prototype_isspace(self):
        self.find_prototype_asserts(datatypes.bytes.isspace(), (b'    ', b'    ', (b'    ',)), b'    ')

    def test_compound_isspace(self):
        self.find_compound_asserts('bytes__isspace', [], (b'    ', b'    ', (b'    ',)), b'    ')

    def test_prototype_istitle(self):
        self.find_prototype_asserts(datatypes.bytes.istitle(), (b'Foo', b'Foo', (b'Foo',)), b'Foo')

    def test_compound_istitle(self):
        self.find_compound_asserts('bytes__istitle', [], (b'Foo', b'Foo', (b'Foo',)), b'Foo')


class FindCommandBytearrayDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = bytearray(b'foo')

    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.bytearray.exact(self.foo), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_exact(self):
        self.find_compound_asserts('bytearray__exact', [self.foo], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_iexact(self):
        foo = bytearray(b'fOo')
        self.find_prototype_asserts(datatypes.bytearray.iexact(bytearray(b'fOO')), (self.foo, foo, (self.foo,)), {
            'nolimit': [self.foo, foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, foo],
            'level1': [self.foo, foo],
            'level2': [self.foo, foo, self.foo],
            'ignore': [self.foo, foo]
        })

    def test_compound_iexact(self):
        foo = bytearray(b'fOo')
        self.find_compound_asserts('bytearray__iexact', [bytearray(b'fOO')], (self.foo, foo, (self.foo,)), {
            'nolimit': [self.foo, foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, foo],
            'level1': [self.foo, foo],
            'level2': [self.foo, foo, self.foo],
            'ignore': [self.foo, foo]
        })

    def test_prototype_contains(self):
        self.find_prototype_asserts(
            datatypes.bytearray.contains(bytearray(b'o')),
            (self.foo, self.foo, (self.foo,)), self.foo
        )

    def test_compound_contains(self):
        self.find_compound_asserts(
            'bytearray__contains', [bytearray(b'o')],
            (self.foo, self.foo, (self.foo,)), self.foo
        )

    def test_prototype_icontains(self):
        foo = bytearray(b'fOo')
        self.find_prototype_asserts(datatypes.bytearray.icontains(bytearray(b'O')), (self.foo, foo, (self.foo,)), {
            'nolimit': [self.foo, foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, foo],
            'level1': [self.foo, foo],
            'level2': [self.foo, foo, self.foo],
            'ignore': [self.foo, foo]
        })

    def test_compound_icontains(self):
        foo = bytearray(b'fOo')
        self.find_compound_asserts('bytearray__icontains', [bytearray(b'O')], (self.foo, foo, (self.foo,)), {
            'nolimit': [self.foo, foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, foo],
            'level1': [self.foo, foo],
            'level2': [self.foo, foo, self.foo],
            'ignore': [self.foo, foo]
        })

    def test_prototype_startswith(self):
        self.find_prototype_asserts(
            datatypes.bytearray.startswith(bytearray(b'f')),
            (self.foo, self.foo, (self.foo,)), self.foo
        )

    def test_compound_startswith(self):
        self.find_compound_asserts(
            'bytearray__startswith', [bytearray(b'f')],
            (self.foo, self.foo, (self.foo,)), self.foo
        )

    def test_prototype_istartswith(self):
        foo = bytearray(b'fOo')
        self.find_prototype_asserts(datatypes.bytearray.istartswith(bytearray(b'f')), (self.foo, foo, (self.foo,)), {
            'nolimit': [self.foo, foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, foo],
            'level1': [self.foo, foo],
            'level2': [self.foo, foo, self.foo],
            'ignore': [self.foo, foo]
        })

    def test_compound_istartswith(self):
        foo = bytearray(b'fOo')
        self.find_compound_asserts('bytearray__istartswith', [bytearray(b'f')], (self.foo, foo, (self.foo,)), {
            'nolimit': [self.foo, foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, foo],
            'level1': [self.foo, foo],
            'level2': [self.foo, foo, self.foo],
            'ignore': [self.foo, foo]
        })

    def test_prototype_endswith(self):
        self.find_prototype_asserts(
            datatypes.bytearray.endswith(bytearray(b'oo')),
            (self.foo, self.foo, (self.foo,)), self.foo
        )

    def test_compound_endswith(self):
        self.find_compound_asserts(
            'bytearray__endswith', [bytearray(b'oo')],
            (self.foo, self.foo, (self.foo,)), self.foo
        )

    def test_prototype_iendswith(self):
        foo = bytearray(b'fOo')
        self.find_prototype_asserts(datatypes.bytearray.iendswith(bytearray(b'OO')), (self.foo, foo, (self.foo,)), {
            'nolimit': [self.foo, foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, foo],
            'level1': [self.foo, foo],
            'level2': [self.foo, foo, self.foo],
            'ignore': [self.foo, foo]
        })

    def test_compound_iendswith(self):
        foo = bytearray(b'fOo')
        self.find_compound_asserts('bytearray__iendswith', [bytearray(b'OO')], (self.foo, foo, (self.foo,)), {
            'nolimit': [self.foo, foo, self.foo],
            'limit1': self.foo,
            'limit2': [self.foo, foo],
            'level1': [self.foo, foo],
            'level2': [self.foo, foo, self.foo],
            'ignore': [self.foo, foo]
        })

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.bytearray.len(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_len(self):
        self.find_compound_asserts('bytearray__len', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.bytearray.lenlt(4), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lenlt(self):
        self.find_compound_asserts('bytearray__lenlt', [4], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.bytearray.lenlte(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lenlte(self):
        self.find_compound_asserts('bytearray__lenlte', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lengt(self):
        self.find_prototype_asserts(datatypes.bytearray.lengt(2), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lengt(self):
        self.find_compound_asserts('bytearray__lengt', [2], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_lengte(self):
        self.find_prototype_asserts(datatypes.bytearray.lengte(3), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_lengte(self):
        self.find_compound_asserts('bytearray__lengte', [3], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalnum(self):
        self.find_prototype_asserts(datatypes.bytearray.isalnum(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_isalnum(self):
        self.find_compound_asserts('bytearray__isalnum', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalnums(self):
        foo1, foo2, foo3 = bytearray(b'fo o'), bytearray(b'f Oo'), bytearray(b'f O o')
        self.find_prototype_asserts(datatypes.bytearray.isalnums(), (foo1, foo2, (foo3,)), {
            'nolimit': [foo1, foo2, foo3],
            'limit1': foo1,
            'limit2': [foo1, foo2],
            'level1': [foo1, foo2],
            'level2': [foo1, foo2, foo3],
            'ignore': [foo1, foo2]
        })

    def test_compound_isalnums(self):
        foo1, foo2, foo3 = bytearray(b'fo o'), bytearray(b'f Oo'), bytearray(b'f O o')
        self.find_compound_asserts('bytearray__isalnums', [], (foo1, foo2, (foo3,)), {
            'nolimit': [foo1, foo2, foo3],
            'limit1': foo1,
            'limit2': [foo1, foo2],
            'level1': [foo1, foo2],
            'level2': [foo1, foo2, foo3],
            'ignore': [foo1, foo2]
        })

    def test_prototype_isalpha(self):
        self.find_prototype_asserts(datatypes.bytearray.isalpha(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_isalpha(self):
        self.find_compound_asserts('bytearray__isalpha', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isalphas(self):
        foo1, foo2, foo3 = bytearray(b'fo o'), bytearray(b'f Oo'), bytearray(b'fo o')
        self.find_prototype_asserts(datatypes.bytearray.isalphas(), (foo1, foo2, (foo3,)), {
            'nolimit': [foo1, foo2, foo3],
            'limit1': foo1,
            'limit2': [foo1, foo2],
            'level1': [foo1, foo2],
            'level2': [foo1, foo2, foo3],
            'ignore': [foo1, foo2]
        })

    def test_compound_isalphas(self):
        foo1, foo2, foo3 = bytearray(b'fo o'), bytearray(b'f Oo'), bytearray(b'fo o')
        self.find_compound_asserts('bytearray__isalphas', [], (foo1, foo2, (foo3,)), {
            'nolimit': [foo1, foo2, foo3],
            'limit1': foo1,
            'limit2': [foo1, foo2],
            'level1': [foo1, foo2],
            'level2': [foo1, foo2, foo3],
            'ignore': [foo1, foo2]
        })

    def test_prototype_isdigit(self):
        one = bytearray(b'1')
        self.find_prototype_asserts(datatypes.bytearray.isdigit(), (one, one, (one,)), one)

    def test_compound_isdigit(self):
        one = bytearray(b'1')
        self.find_compound_asserts('bytearray__isdigit', [], (one, one, (one,)), one)

    def test_prototype_islower(self):
        self.find_prototype_asserts(datatypes.bytearray.islower(), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_islower(self):
        self.find_compound_asserts('bytearray__islower', [], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_isupper(self):
        upper = bytearray(b'FOO')
        self.find_prototype_asserts(datatypes.bytearray.isupper(), (upper, upper, (upper,)), upper)

    def test_compound_isupper(self):
        upper = bytearray(b'FOO')
        self.find_compound_asserts('bytearray__isupper', [], (upper, upper, (upper,)), upper)

    def test_prototype_isspace(self):
        space = bytearray(b'    ')
        self.find_prototype_asserts(datatypes.bytearray.isspace(), (space, space, (space,)), space)

    def test_compound_isspace(self):
        space = bytearray(b'    ')
        self.find_compound_asserts('bytearray__isspace', [], (space, space, (space,)), space)

    def test_prototype_istitle(self):
        title = bytearray(b'Foo')
        self.find_prototype_asserts(datatypes.bytearray.istitle(), (title, title, (title,)), title)

    def test_compound_istitle(self):
        title = bytearray(b'Foo')
        self.find_compound_asserts('bytearray__istitle', [], (title, title, (title,)), title)


class FindCommandNumericDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.numeric.exact(5.5), (5.5, 5.5, (5.5,)), 5.5)

    def test_compound_exact(self):
        self.find_compound_asserts('numeric__exact', [5.5], (5.5, 5.5, (5.5,)), 5.5)

    def test_prototype_gt(self):
        self.find_prototype_asserts(datatypes.numeric.gt(3), (4, 4, (4,)), 4)

    def test_compound_gt(self):
        self.find_compound_asserts('numeric__gt', [3], (4, 4, (4,)), 4)

    def test_prototype_gte(self):
        self.find_prototype_asserts(datatypes.numeric.gte(5), (5, 5, (5,)), 5)

    def test_compound_gte(self):
        self.find_compound_asserts('numeric__gte', [5], (5, 5, (5,)), 5)

    def test_prototype_lt(self):
        self.find_prototype_asserts(datatypes.numeric.lt(2), (1, 1, (1,)), 1)

    def test_compound_lt(self):
        self.find_compound_asserts('numeric__lt', [2], (1, 1, (1,)), 1)

    def test_prototype_lte(self):
        self.find_prototype_asserts(datatypes.numeric.lte(2), (2, 2, (2,)), 2)

    def test_compound_lte(self):
        self.find_compound_asserts('numeric__lte', [2], (2, 2, (2,)), 2)

    def test_prototype_between(self):
        self.find_prototype_asserts(datatypes.numeric.between(1, 2), (1, 1, (1,)), 1)

    def test_compound_between(self):
        self.find_compound_asserts('numeric__between', [1, 2], (1, 1, (1,)), 1)

    def test_prototype_ebetween(self):
        self.find_prototype_asserts(datatypes.numeric.ebetween(0, 2), (1, 1, (1,)), 1)

    def test_compound_ebetween(self):
        self.find_compound_asserts('numeric__ebetween', [0, 2], (1, 1, (1,)), 1)

    def test_prototype_isodd(self):
        self.find_prototype_asserts(datatypes.numeric.isodd(), (5, 5, (5,)), 5)

    def test_compound_isodd(self):
        self.find_compound_asserts('numeric__isodd', [], (5, 5, (5,)), 5)

    def test_prototype_iseven(self):
        self.find_prototype_asserts(datatypes.numeric.iseven(), (4, 4, (4,)), 4)

    def test_compound_iseven(self):
        self.find_compound_asserts('numeric__iseven', [], (4, 4, (4,)), 4)

    def test_prototype_divisibleby(self):
        self.find_prototype_asserts(datatypes.numeric.divisibleby(2), (4, 4, (4,)), 4)

    def test_compound_divisibleby(self):
        self.find_compound_asserts('numeric__divisibleby', [2], (4, 4, (4,)), 4)


class FindCommandIntDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.int.exact(5), (5, 5, (5,)), 5)

    def test_compound_exact(self):
        self.find_compound_asserts('int__exact', [5], (5, 5, (5,)), 5)

    def test_prototype_gt(self):
        self.find_prototype_asserts(datatypes.int.gt(3), (4, 4, (4,)), 4)

    def test_compound_gt(self):
        self.find_compound_asserts('int__gt', [3], (4, 4, (4,)), 4)

    def test_prototype_gte(self):
        self.find_prototype_asserts(datatypes.int.gte(5), (5, 5, (5,)), 5)

    def test_compound_gte(self):
        self.find_compound_asserts('int__gte', [5], (5, 5, (5,)), 5)

    def test_prototype_lt(self):
        self.find_prototype_asserts(datatypes.int.lt(2), (1, 1, (1,)), 1)

    def test_compound_lt(self):
        self.find_compound_asserts('int__lt', [2], (1, 1, (1,)), 1)

    def test_prototype_lte(self):
        self.find_prototype_asserts(datatypes.int.lte(2), (2, 2, (2,)), 2)

    def test_compound_lte(self):
        self.find_compound_asserts('int__lte', [2], (2, 2, (2,)), 2)

    def test_prototype_between(self):
        self.find_prototype_asserts(datatypes.int.between(1, 2), (1, 1, (1,)), 1)

    def test_compound_between(self):
        self.find_compound_asserts('int__between', [1, 2], (1, 1, (1,)), 1)

    def test_prototype_ebetween(self):
        self.find_prototype_asserts(datatypes.int.ebetween(0, 2), (1, 1, (1,)), 1)

    def test_compound_ebetween(self):
        self.find_compound_asserts('int__ebetween', [0, 2], (1, 1, (1,)), 1)

    def test_prototype_isodd(self):
        self.find_prototype_asserts(datatypes.int.isodd(), (5, 5, (5,)), 5)

    def test_compound_isodd(self):
        self.find_compound_asserts('int__isodd', [], (5, 5, (5,)), 5)

    def test_prototype_iseven(self):
        self.find_prototype_asserts(datatypes.int.iseven(), (4, 4, (4,)), 4)

    def test_compound_iseven(self):
        self.find_compound_asserts('int__iseven', [], (4, 4, (4,)), 4)

    def test_prototype_divisibleby(self):
        self.find_prototype_asserts(datatypes.int.divisibleby(2), (4, 4, (4,)), 4)

    def test_compound_divisibleby(self):
        self.find_compound_asserts('int__divisibleby', [2], (4, 4, (4,)), 4)


class FindCommandFloatDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.float.exact(5.5), (5.5, 5.5, (5.5,)), 5.5)

    def test_compound_exact(self):
        self.find_compound_asserts('float__exact', [5.5], (5.5, 5.5, (5.5,)), 5.5)

    def test_prototype_gt(self):
        self.find_prototype_asserts(datatypes.float.gt(3), (4.2, 4.2, (4.2,)), 4.2)

    def test_compound_gt(self):
        self.find_compound_asserts('float__gt', [3], (4.2, 4.2, (4.2,)), 4.2)

    def test_prototype_gte(self):
        self.find_prototype_asserts(datatypes.float.gte(5), (5.5, 5.5, (5.5,)), 5.5)

    def test_compound_gte(self):
        self.find_compound_asserts('float__gte', [5], (5.5, 5.5, (5.5,)), 5.5)

    def test_prototype_lt(self):
        self.find_prototype_asserts(datatypes.float.lt(2), (1.1, 1.1, (1.1,)), 1.1)

    def test_compound_lt(self):
        self.find_compound_asserts('float__lt', [2], (1.1, 1.1, (1.1,)), 1.1)

    def test_prototype_lte(self):
        self.find_prototype_asserts(datatypes.float.lte(2), (1.8, 1.8, (1.8,)), 1.8)

    def test_compound_lte(self):
        self.find_compound_asserts('float__lte', [2], (1.8, 1.8, (1.8,)), 1.8)

    def test_prototype_between(self):
        self.find_prototype_asserts(datatypes.float.between(1, 2), (1.4, 1.4, (1.4,)), 1.4)

    def test_compound_between(self):
        self.find_compound_asserts('float__between', [1, 2], (1.4, 1.4, (1.4,)), 1.4)

    def test_prototype_ebetween(self):
        self.find_prototype_asserts(datatypes.float.ebetween(0, 2), (1.5, 1.5, (1.5,)), 1.5)

    def test_compound_ebetween(self):
        self.find_compound_asserts('float__ebetween', [0, 2], (1.5, 1.5, (1.5,)), 1.5)

    def test_prototype_isinteger(self):
        self.find_prototype_asserts(datatypes.float.isinteger(), (5.0, 5.0, (5.0,)), 5.0)

    def test_compound_isinteger(self):
        self.find_compound_asserts('float__isinteger', [], (5.0, 5.0, (5.0,)), 5.0)

    def test_prototype_isodd(self):
        self.find_prototype_asserts(datatypes.float.isodd(), (5.2, 5.2, (5.2,)), 5.2)

    def test_compound_isodd(self):
        self.find_compound_asserts('float__isodd', [], (5.2, 5.2, (5.2,)), 5.2)

    def test_prototype_iseven(self):
        self.find_prototype_asserts(datatypes.float.iseven(), (4.3, 4.3, (4.3,)), 4.3)

    def test_compound_iseven(self):
        self.find_compound_asserts('float__iseven', [], (4.3, 4.3, (4.3,)), 4.3)

    def test_prototype_divisibleby(self):
        self.find_prototype_asserts(datatypes.float.divisibleby(2), (4.7, 4.7, (4.7,)), 4.7)

    def test_compound_divisibleby(self):
        self.find_compound_asserts('float__divisibleby', [2], (4.7, 4.7, (4.7,)), 4.7)


class FindCommandLongDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.long.exact(2 ** 64), (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_compound_exact(self):
        self.find_compound_asserts('long__exact', [2 ** 64], (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_prototype_gt(self):
        self.find_prototype_asserts(datatypes.long.gt(2 ** 63), (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_compound_gt(self):
        self.find_compound_asserts('long__gt', [2 ** 63], (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_prototype_gte(self):
        self.find_prototype_asserts(datatypes.long.gte(2 ** 64), (2 ** 65, 2 ** 65, (2 ** 65,)), 2 ** 65)

    def test_compound_gte(self):
        self.find_compound_asserts('long__gte', [2 ** 64], (2 ** 65, 2 ** 65, (2 ** 65,)), 2 ** 65)

    def test_prototype_lt(self):
        self.find_prototype_asserts(datatypes.long.lt(2 ** 64), (2 ** 63, 2 ** 63, (2 ** 63,)), 2 ** 63)

    def test_compound_lt(self):
        self.find_compound_asserts('long__lt', [2 ** 64], (2 ** 63, 2 ** 63, (2 ** 63,)), 2 ** 63)

    def test_prototype_lte(self):
        self.find_prototype_asserts(datatypes.long.lte(2 ** 64), (2 ** 63, 2 ** 63, (2 ** 63,)), 2 ** 63)

    def test_compound_lte(self):
        self.find_compound_asserts('long__lte', [2 ** 64], (2 ** 63, 2 ** 63, (2 ** 63,)), 2 ** 63)

    def test_prototype_between(self):
        self.find_prototype_asserts(datatypes.long.between(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_compound_between(self):
        self.find_compound_asserts('long__between', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_prototype_ebetween(self):
        self.find_prototype_asserts(datatypes.long.ebetween(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_compound_ebetween(self):
        self.find_compound_asserts('long__ebetween', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_prototype_isodd(self):
        self.find_prototype_asserts(datatypes.long.isodd(), (3 ** 64, 3 ** 64, (3 ** 64,)), 3 ** 64)

    def test_compound_isodd(self):
        self.find_compound_asserts('long__isodd', [], (3 ** 64, 3 ** 64, (3 ** 64,)), 3 ** 64)

    def test_prototype_iseven(self):
        self.find_prototype_asserts(datatypes.long.iseven(), (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_compound_iseven(self):
        self.find_compound_asserts('long__iseven', [], (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_prototype_divisibleby(self):
        self.find_prototype_asserts(datatypes.long.divisibleby(2), (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)

    def test_compound_divisibleby(self):
        self.find_compound_asserts('long__divisibleby', [2], (2 ** 64, 2 ** 64, (2 ** 64,)), 2 ** 64)


class FindCommandComplexDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.complex.exact(1j), (1j, 1j, (1j,)), 1j)

    def test_compound_exact(self):
        self.find_compound_asserts('complex__exact', [1j], (1j, 1j, (1j,)), 1j)


class FindCommandIterableDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.iterable.exact(['foo']), (['foo'], ['foo'], (['foo'],)), ['foo'])

    def test_compound_exact(self):
        self.find_compound_asserts('iterable__exact', [['foo']], (['foo'], ['foo'], (['foo'],)), ['foo'])

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.iterable.len(1), (['foo'], ['foo'], (['foo'], [])), ['foo'])

    def test_compound_len(self):
        self.find_compound_asserts('iterable__len', [1], (['foo'], ['foo'], (['foo'], [])), ['foo'])

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.iterable.lenlt(2), (['foo'], ['foo'], (['foo'], [1, 2])), ['foo'])

    def test_compound_lenlt(self):
        self.find_compound_asserts('iterable__lenlt', [2], (['foo'], ['foo'], (['foo'], [1, 2])), ['foo'])

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.iterable.lenlte(1), (['foo'], ['foo'], (['foo'], [1, 2])), ['foo'])

    def test_compound_lenlte(self):
        self.find_compound_asserts('iterable__lenlte', [1], (['foo'], ['foo'], (['foo'], [1, 2])), ['foo'])

    def test_prototype_lengt(self):
        self.find_prototype_asserts(datatypes.iterable.lengt(1), (['foo', 1], ['foo', 1], (['foo', 1],)), ['foo', 1])

    def test_compound_lengt(self):
        self.find_compound_asserts('iterable__lengt', [1], (['foo', 1], ['foo', 1], (['foo', 1],)), ['foo', 1])

    def test_prototype_lengte(self):
        self.find_prototype_asserts(datatypes.iterable.lengte(2), (['foo', 1], ['foo', 1], (['foo', 1],)), ['foo', 1])

    def test_compound_lengte(self):
        self.find_compound_asserts('iterable__lengte', [2], (['foo', 1], ['foo', 1], (['foo', 1],)), ['foo', 1])

    def test_prototype_contains(self):
        self.find_prototype_asserts(datatypes.iterable.contains('foo'), (['foo'], ('foo',), (set(['foo']),)), {
            'nolimit': [['foo'], ('foo',), set(['foo'])],
            'limit1': ['foo'],
            'limit2': [['foo'], ('foo',)],
            'level1': [['foo'], ('foo',)],
            'level2': [['foo'], ('foo',), set(['foo'])],
            'ignore': [['foo']]
        })

    def test_compound_contains(self):
        self.find_compound_asserts('iterable__contains', ['foo'], (['foo'], ('foo',), (set(['foo']),)), {
            'nolimit': [['foo'], ('foo',), set(['foo'])],
            'limit1': ['foo'],
            'limit2': [['foo'], ('foo',)],
            'level1': [['foo'], ('foo',)],
            'level2': [['foo'], ('foo',), set(['foo'])],
            'ignore': [['foo']]
        })

    def test_prototype_contains_all(self):
        self.find_prototype_asserts(
            datatypes.iterable.contains_all(['f', 'o']),
            (['f', 'o'], ('f', 'o'), (set(['f', 'o']),)),
            {
                'nolimit': [['f', 'o'], ('f', 'o'), set(['f', 'o'])],
                'limit1': ['f', 'o'],
                'limit2': [['f', 'o'], ('f', 'o')],
                'level1': [['f', 'o'], ('f', 'o')],
                'level2': [['f', 'o'], ('f', 'o'), set(['f', 'o'])],
                'ignore': [['f', 'o']]
            }
        )

    def test_compound_contains_all(self):
        self.find_compound_asserts(
            'iterable__contains_all',
            [['f', 'o']],
            (['f', 'o'], ('f', 'o'), (set(['f', 'o']),)),
            {
                'nolimit': [['f', 'o'], ('f', 'o'), set(['f', 'o'])],
                'limit1': ['f', 'o'],
                'limit2': [['f', 'o'], ('f', 'o')],
                'level1': [['f', 'o'], ('f', 'o')],
                'level2': [['f', 'o'], ('f', 'o'), set(['f', 'o'])],
                'ignore': [['f', 'o']]
            }
        )

    def test_prototype_contains_any(self):
        self.find_prototype_asserts(
            datatypes.iterable.contains_any(['f', 'z']),
            (['f', 'o'], ('f', 'o'), (set(['f', 'o']),)),
            {
                'nolimit': [['f', 'o'], ('f', 'o'), set(['f', 'o'])],
                'limit1': ['f', 'o'],
                'limit2': [['f', 'o'], ('f', 'o')],
                'level1': [['f', 'o'], ('f', 'o')],
                'level2': [['f', 'o'], ('f', 'o'), set(['f', 'o'])],
                'ignore': [['f', 'o']]
            }
        )

    def test_compound_contains_any(self):
        self.find_compound_asserts(
            'iterable__contains_any',
            [['f', 'z']],
            (['f', 'o'], ('f', 'o'), (set(['f', 'o']),)),
            {
                'nolimit': [['f', 'o'], ('f', 'o'), set(['f', 'o'])],
                'limit1': ['f', 'o'],
                'limit2': [['f', 'o'], ('f', 'o')],
                'level1': [['f', 'o'], ('f', 'o')],
                'level2': [['f', 'o'], ('f', 'o'), set(['f', 'o'])],
                'ignore': [['f', 'o']]
            }
        )

    def test_prototype_str_contains_str(self):
        self.find_prototype_asserts(datatypes.iterable.str_contains_str('f'), (['fo'], ('fo',), (set(['fo']),)), {
            'nolimit': [['fo'], ('fo',), set(['fo'])],
            'limit1': ['fo'],
            'limit2': [['fo'], ('fo',)],
            'level1': [['fo'], ('fo',)],
            'level2': [['fo'], ('fo',), set(['fo'])],
            'ignore': [['fo']]
        })

    def test_compound_str_contains_str(self):
        self.find_compound_asserts('iterable__str_contains_str', ['f'], (['fo'], ('fo',), (set(['fo']),)), {
            'nolimit': [['fo'], ('fo',), set(['fo'])],
            'limit1': ['fo'],
            'limit2': [['fo'], ('fo',)],
            'level1': [['fo'], ('fo',)],
            'level2': [['fo'], ('fo',), set(['fo'])],
            'ignore': [['fo']]
        })


class FindCommandListDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.list.exact(['foo']), (['foo'], ['foo'], (['foo'],)), ['foo'])

    def test_compound_exact(self):
        self.find_compound_asserts('list__exact', [['foo']], (['foo'], ['foo'], (['foo'],)), ['foo'])

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.list.len(1), (['foo'], ['foo'], (['foo'], [])), ['foo'])

    def test_compound_len(self):
        self.find_compound_asserts('list__len', [1], (['foo'], ['foo'], (['foo'], [])), ['foo'])

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.list.lenlt(2), (['foo'], ['foo'], (['foo'], [1, 2])), ['foo'])

    def test_compound_lenlt(self):
        self.find_compound_asserts('list__lenlt', [2], (['foo'], ['foo'], (['foo'], [1, 2])), ['foo'])

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.list.lenlte(1), (['foo'], ['foo'], (['foo'], [1, 2])), ['foo'])

    def test_compound_lenlte(self):
        self.find_compound_asserts('list__lenlte', [1], (['foo'], ['foo'], (['foo'], [1, 2])), ['foo'])

    def test_prototype_lengt(self):
        self.find_prototype_asserts(datatypes.list.lengt(1), (['foo', 1], ['foo', 1], (['foo', 1],)), ['foo', 1])

    def test_compound_lengt(self):
        self.find_compound_asserts('list__lengt', [1], (['foo', 1], ['foo', 1], (['foo', 1],)), ['foo', 1])

    def test_prototype_lengte(self):
        self.find_prototype_asserts(datatypes.list.lengte(2), (['foo', 1], ['foo', 1], (['foo', 1],)), ['foo', 1])

    def test_compound_lengte(self):
        self.find_compound_asserts('list__lengte', [2], (['foo', 1], ['foo', 1], (['foo', 1],)), ['foo', 1])

    def test_prototype_contains(self):
        self.find_prototype_asserts(datatypes.list.contains('foo'), (['foo'], ['foo'], (['foo'],)), ['foo'])

    def test_compound_contains(self):
        self.find_compound_asserts('list__contains', ['foo'], (['foo'], ['foo'], (['foo'],)), ['foo'])

    def test_prototype_contains_all(self):
        self.find_prototype_asserts(
            datatypes.list.contains_all(['f', 'o']),
            (['f', 'o'], ['f', 'o'], (['f', 'o'],)),
            ['f', 'o']
        )

    def test_compound_contains_all(self):
        self.find_compound_asserts(
            'list__contains_all',
            [['f', 'o']],
            (['f', 'o'], ['f', 'o'], (['f', 'o'],)),
            ['f', 'o']
        )

    def test_prototype_contains_any(self):
        self.find_prototype_asserts(
            datatypes.list.contains_any(['f', 'z']),
            (['f', 'o'], ['f', 'o'], (['f', 'o'],)),
            ['f', 'o']
        )

    def test_compound_contains_any(self):
        self.find_compound_asserts(
            'list__contains_any',
            [['f', 'z']],
            (['f', 'o'], ['f', 'o'], (['f', 'o'],)),
            ['f', 'o']
        )

    def test_prototype_str_contains_str(self):
        self.find_prototype_asserts(datatypes.list.str_contains_str('f'), (['fo'], ['fo'], (['fo'],)), ['fo'])

    def test_compound_str_contains_str(self):
        self.find_compound_asserts('list__str_contains_str', ['f'], (['fo'], ['fo'], (['fo'],)), ['fo'])


class FindCommandTupleDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.tuple.exact(('foo',)), (('foo',), ('foo',), [('foo',)]), ('foo',))

    def test_compound_exact(self):
        self.find_compound_asserts('tuple__exact', [('foo',)], (('foo',), ('foo',), [('foo',)]), ('foo',))

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.tuple.len(1), (('foo',), ('foo',), [('foo',), ()]), ('foo',))

    def test_compound_len(self):
        self.find_compound_asserts('tuple__len', [1], (('foo',), ('foo',), [('foo',), ()]), ('foo',))

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.tuple.lenlt(2), (('foo',), ('foo',), [('foo',), (1, 2)]), ('foo',))

    def test_compound_lenlt(self):
        self.find_compound_asserts('tuple__lenlt', [2], (('foo',), ('foo',), [('foo',), (1, 2)]), ('foo',))

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.tuple.lenlte(1), (('foo',), ('foo',), [('foo',), (1, 2)]), ('foo',))

    def test_compound_lenlte(self):
        self.find_compound_asserts('tuple__lenlte', [1], (('foo',), ('foo',), [('foo',), (1, 2)]), ('foo',))

    def test_prototype_lengt(self):
        self.find_prototype_asserts(datatypes.tuple.lengt(1), (('foo', 1), ('foo', 1), [('foo', 1)]), ('foo', 1))

    def test_compound_lengt(self):
        self.find_compound_asserts('tuple__lengt', [1], (('foo', 1), ('foo', 1), [('foo', 1)]), ('foo', 1))

    def test_prototype_lengte(self):
        self.find_prototype_asserts(datatypes.tuple.lengte(2), (('foo', 1), ('foo', 1), [('foo', 1)]), ('foo', 1))

    def test_compound_lengte(self):
        self.find_compound_asserts('tuple__lengte', [2], (('foo', 1), ('foo', 1), [('foo', 1)]), ('foo', 1))

    def test_prototype_contains(self):
        self.find_prototype_asserts(datatypes.tuple.contains('foo'), (('foo',), ('foo',), [('foo',)]), ('foo',))

    def test_compound_contains(self):
        self.find_compound_asserts('tuple__contains', ['foo'], (('foo',), ('foo',), [('foo',)]), ('foo',))

    def test_prototype_contains_all(self):
        self.find_prototype_asserts(
            datatypes.tuple.contains_all(('f', 'o')),
            (('f', 'o'), ('f', 'o'), [('f', 'o')]),
            ('f', 'o')
        )

    def test_compound_contains_all(self):
        self.find_compound_asserts(
            'tuple__contains_all',
            [('f', 'o')],
            (('f', 'o'), ('f', 'o'), [('f', 'o')]),
            ('f', 'o')
        )

    def test_prototype_contains_any(self):
        self.find_prototype_asserts(
            datatypes.tuple.contains_any(('f', 'z')),
            (('f', 'o'), ('f', 'o'), [('f', 'o')]),
            ('f', 'o')
        )

    def test_compound_contains_any(self):
        self.find_compound_asserts(
            'tuple__contains_any',
            [('f', 'z')],
            (('f', 'o'), ('f', 'o'), [('f', 'o')]),
            ('f', 'o')
        )

    def test_prototype_str_contains_str(self):
        self.find_prototype_asserts(datatypes.tuple.str_contains_str('f'), (('fo',), ('fo',), [('fo',)]), ('fo',))

    def test_compound_str_contains_str(self):
        self.find_compound_asserts('tuple__str_contains_str', ['f'], (('fo',), ('fo',), [('fo',)]), ('fo',))


class FindCommandSetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = set(['foo'])

    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.set.exact(self.foo), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_exact(self):
        self.find_compound_asserts('set__exact', [self.foo], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.set.len(1), (self.foo, self.foo, (self.foo, [])), self.foo)

    def test_compound_len(self):
        self.find_compound_asserts('set__len', [1], (self.foo, self.foo, (self.foo, [])), self.foo)

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.set.lenlt(2), (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_compound_lenlt(self):
        self.find_compound_asserts('set__lenlt', [2], (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.set.lenlte(1), (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_compound_lenlte(self):
        self.find_compound_asserts('set__lenlte', [1], (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_prototype_lengt(self):
        foo = set(['foo', 1])
        self.find_prototype_asserts(datatypes.set.lengt(1), (foo, foo, (foo,)), foo)

    def test_compound_lengt(self):
        foo = set(['foo', 1])
        self.find_compound_asserts('set__lengt', [1], (foo, foo, (foo,)), foo)

    def test_prototype_lengte(self):
        foo = set(['foo', 1])
        self.find_prototype_asserts(datatypes.set.lengte(2), (foo, foo, (foo,)), foo)

    def test_compound_lengte(self):
        foo = set(['foo', 1])
        self.find_compound_asserts('set__lengte', [2], (foo, foo, (foo,)), foo)

    def test_prototype_contains(self):
        self.find_prototype_asserts(datatypes.set.contains('foo'), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_contains(self):
        self.find_compound_asserts('set__contains', ['foo'], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_contains_all(self):
        foo = set(['f', 'o'])
        self.find_prototype_asserts(datatypes.set.contains_all(['f', 'o']), (foo, foo, (foo,)), foo)

    def test_compound_contains_all(self):
        foo = set(['f', 'o'])
        self.find_compound_asserts('set__contains_all', [['f', 'o']], (foo, foo, (foo,)), foo)

    def test_prototype_contains_any(self):
        foo = set(['f', 'o'])
        self.find_prototype_asserts(datatypes.set.contains_any(['f', 'z']), (foo, foo, (foo,)), foo)

    def test_compound_contains_any(self):
        foo = set(['f', 'o'])
        self.find_compound_asserts('set__contains_any', [['f', 'z']], (foo, foo, (foo,)), foo)

    def test_prototype_str_contains_str(self):
        foo = set(['fo'])
        self.find_prototype_asserts(datatypes.set.str_contains_str('f'), (foo, foo, (foo,)), foo)

    def test_compound_str_contains_str(self):
        foo = set(['fo'])
        self.find_compound_asserts('set__str_contains_str', ['f'], (foo, foo, (foo,)), foo)

    def test_prototype_isdisjoint(self):
        foo = set(['foo'])
        self.find_prototype_asserts(datatypes.set.isdisjoint(set(['bar'])), (foo, foo, (foo,)), foo)

    def test_compound_isdisjoint(self):
        foo = set(['foo'])
        self.find_compound_asserts('set__isdisjoint', [set(['bar'])], (foo, foo, (foo,)), foo)

    def test_prototype_issubset(self):
        foo = set(['foo'])
        self.find_prototype_asserts(datatypes.set.issubset(set(['foo'])), (foo, foo, (foo,)), foo)

    def test_compound_issubset(self):
        foo = set(['foo'])
        self.find_compound_asserts('set__issubset', [set(['foo'])], (foo, foo, (foo,)), foo)

    def test_prototype_eissubset(self):
        foo = set(['foo'])
        self.find_prototype_asserts(datatypes.set.eissubset(set(['foo', 'bar'])), (foo, foo, (foo,)), foo)

    def test_compound_eissubset(self):
        foo = set(['foo'])
        self.find_compound_asserts('set__eissubset', [set(['foo', 'bar'])], (foo, foo, (foo,)), foo)

    def test_prototype_issuperset(self):
        foo = set(['foo', 'bar'])
        self.find_prototype_asserts(datatypes.set.issuperset(set(['foo', 'bar'])), (foo, foo, (foo,)), foo)

    def test_compound_issuperset(self):
        foo = set(['foo', 'bar'])
        self.find_compound_asserts('set__issuperset', [set(['foo', 'bar'])], (foo, foo, (foo,)), foo)

    def test_prototype_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.find_prototype_asserts(datatypes.set.eissuperset(set(['foo'])), (foo, foo, (foo,)), foo)

    def test_compound_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.find_compound_asserts('set__eissuperset', [set(['foo'])], (foo, foo, (foo,)), foo)


class FindCommandFrozensetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = frozenset(['foo'])

    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.frozenset.exact(self.foo), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_exact(self):
        self.find_compound_asserts('frozenset__exact', [self.foo], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.frozenset.len(1), (self.foo, self.foo, (self.foo, [])), self.foo)

    def test_compound_len(self):
        self.find_compound_asserts('frozenset__len', [1], (self.foo, self.foo, (self.foo, [])), self.foo)

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.frozenset.lenlt(2), (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_compound_lenlt(self):
        self.find_compound_asserts('frozenset__lenlt', [2], (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.frozenset.lenlte(1), (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_compound_lenlte(self):
        self.find_compound_asserts('frozenset__lenlte', [1], (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_prototype_lengt(self):
        foo = frozenset(['foo', 1])
        self.find_prototype_asserts(datatypes.frozenset.lengt(1), (foo, foo, (foo,)), foo)

    def test_compound_lengt(self):
        foo = frozenset(['foo', 1])
        self.find_compound_asserts('frozenset__lengt', [1], (foo, foo, (foo,)), foo)

    def test_prototype_lengte(self):
        foo = frozenset(['foo', 1])
        self.find_prototype_asserts(datatypes.frozenset.lengte(2), (foo, foo, (foo,)), foo)

    def test_compound_lengte(self):
        foo = frozenset(['foo', 1])
        self.find_compound_asserts('frozenset__lengte', [2], (foo, foo, (foo,)), foo)

    def test_prototype_contains(self):
        self.find_prototype_asserts(datatypes.frozenset.contains('foo'), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_contains(self):
        self.find_compound_asserts('frozenset__contains', ['foo'], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.find_prototype_asserts(datatypes.frozenset.contains_all(['f', 'o']), (foo, foo, (foo,)), foo)

    def test_compound_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.find_compound_asserts('frozenset__contains_all', [['f', 'o']], (foo, foo, (foo,)), foo)

    def test_prototype_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.find_prototype_asserts(datatypes.frozenset.contains_any(['f', 'z']), (foo, foo, (foo,)), foo)

    def test_compound_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.find_compound_asserts('frozenset__contains_any', [['f', 'z']], (foo, foo, (foo,)), foo)

    def test_prototype_str_contains_str(self):
        foo = frozenset(['fo'])
        self.find_prototype_asserts(datatypes.frozenset.str_contains_str('f'), (foo, foo, (foo,)), foo)

    def test_compound_str_contains_str(self):
        foo = frozenset(['fo'])
        self.find_compound_asserts('frozenset__str_contains_str', ['f'], (foo, foo, (foo,)), foo)

    def test_prototype_isdisjoint(self):
        foo = frozenset(['foo'])
        self.find_prototype_asserts(datatypes.frozenset.isdisjoint(frozenset(['bar'])), (foo, foo, (foo,)), foo)

    def test_compound_isdisjoint(self):
        foo = frozenset(['foo'])
        self.find_compound_asserts('frozenset__isdisjoint', [frozenset(['bar'])], (foo, foo, (foo,)), foo)

    def test_prototype_issubset(self):
        foo = frozenset(['foo'])
        self.find_prototype_asserts(datatypes.frozenset.issubset(frozenset(['foo'])), (foo, foo, (foo,)), foo)

    def test_compound_issubset(self):
        foo = frozenset(['foo'])
        self.find_compound_asserts('frozenset__issubset', [frozenset(['foo'])], (foo, foo, (foo,)), foo)

    def test_prototype_eissubset(self):
        foo = frozenset(['foo'])
        self.find_prototype_asserts(datatypes.frozenset.eissubset(frozenset(['foo', 'bar'])), (foo, foo, (foo,)), foo)

    def test_compound_eissubset(self):
        foo = frozenset(['foo'])
        self.find_compound_asserts('frozenset__eissubset', [frozenset(['foo', 'bar'])], (foo, foo, (foo,)), foo)

    def test_prototype_issuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.find_prototype_asserts(datatypes.frozenset.issuperset(frozenset(['foo', 'bar'])), (foo, foo, (foo,)), foo)

    def test_compound_issuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.find_compound_asserts('frozenset__issuperset', [frozenset(['foo', 'bar'])], (foo, foo, (foo,)), foo)

    def test_prototype_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.find_prototype_asserts(datatypes.frozenset.eissuperset(frozenset(['foo'])), (foo, foo, (foo,)), foo)

    def test_compound_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.find_compound_asserts('frozenset__eissuperset', [frozenset(['foo'])], (foo, foo, (foo,)), foo)


class FindCommandDictDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = {'foo': 'bar'}

    def test_prototype_exact(self):
        self.find_prototype_asserts(datatypes.dict.exact(self.foo), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_exact(self):
        self.find_compound_asserts('dict__exact', [self.foo], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_len(self):
        self.find_prototype_asserts(datatypes.dict.len(1), (self.foo, self.foo, (self.foo, [])), self.foo)

    def test_compound_len(self):
        self.find_compound_asserts('dict__len', [1], (self.foo, self.foo, (self.foo, [])), self.foo)

    def test_prototype_lenlt(self):
        self.find_prototype_asserts(datatypes.dict.lenlt(2), (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_compound_lenlt(self):
        self.find_compound_asserts('dict__lenlt', [2], (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_prototype_lenlte(self):
        self.find_prototype_asserts(datatypes.dict.lenlte(1), (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_compound_lenlte(self):
        self.find_compound_asserts('dict__lenlte', [1], (self.foo, self.foo, (self.foo, [1, 2])), self.foo)

    def test_prototype_lengt(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_prototype_asserts(datatypes.dict.lengt(1), (foo, foo, (foo,)), foo)

    def test_compound_lengt(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_compound_asserts('dict__lengt', [1], (foo, foo, (foo,)), foo)

    def test_prototype_lengte(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_prototype_asserts(datatypes.dict.lengte(2), (foo, foo, (foo,)), foo)

    def test_compound_lengte(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_compound_asserts('dict__lengte', [2], (foo, foo, (foo,)), foo)

    def test_prototype_contains_key(self):
        self.find_prototype_asserts(datatypes.dict.contains_key('foo'), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_contains_key(self):
        self.find_compound_asserts('dict__contains_key', ['foo'], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_prototype_asserts(datatypes.dict.contains_all_keys(['foo', 'bar']), (foo, foo, (foo,)), foo)

    def test_compound_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_compound_asserts('dict__contains_all_keys', [['foo', 'bar']], (foo, foo, (foo,)), foo)

    def test_prototype_contains_any_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_prototype_asserts(datatypes.dict.contains_any_keys(['foo', 'baz']), (foo, foo, (foo,)), foo)

    def test_compound_contains_any_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_compound_asserts('dict__contains_any_keys', [['foo', 'baz']], (foo, foo, (foo,)), foo)

    def test_prototype_key_contains_str(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_prototype_asserts(datatypes.dict.key_contains_str('f'), (foo, foo, (foo,)), foo)

    def test_compound_key_contains_str(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_compound_asserts('dict__key_contains_str', ['f'], (foo, foo, (foo,)), foo)

    def test_prototype_contains_value(self):
        self.find_prototype_asserts(datatypes.dict.contains_value('bar'), (self.foo, self.foo, (self.foo,)), self.foo)

    def test_compound_contains_value(self):
        self.find_compound_asserts('dict__contains_value', ['bar'], (self.foo, self.foo, (self.foo,)), self.foo)

    def test_prototype_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_prototype_asserts(datatypes.dict.contains_all_values(['baz', 'bar']), (foo, foo, (foo,)), foo)

    def test_compound_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_compound_asserts('dict__contains_all_values', [['baz', 'bar']], (foo, foo, (foo,)), foo)

    def test_prototype_contains_any_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_prototype_asserts(datatypes.dict.contains_any_values(['foo', 'baz']), (foo, foo, (foo,)), foo)

    def test_compound_contains_any_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_compound_asserts('dict__contains_any_values', [['foo', 'baz']], (foo, foo, (foo,)), foo)

    def test_prototype_value_contains_str(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_prototype_asserts(datatypes.dict.value_contains_str('b'), (foo, foo, (foo,)), foo)

    def test_compound_value_contains_str(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.find_compound_asserts('dict__value_contains_str', ['b'], (foo, foo, (foo,)), foo)


class FirstCommandTestCase(unittest.TestCase):
    def test_prototype(self):
        self.assertIsInstance(commands.first(datatypes.bool), commands.Command)
        self.assertEqual(commands.first(datatypes.bool).limit, 1)


class FirstCommandBoolDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.bool.exact(True), (True, True), True)

    def test_compound_exact(self):
        self.first_compound_asserts('bool__exact', [True], (True, True), True)

    def test_prototype_true(self):
        self.first_prototype_asserts(datatypes.bool.true, (True, True), True)

    def test_compound_true(self):
        self.first_compound_asserts('bool__true', [], (True, True), True)

    def test_prototype_false(self):
        self.first_prototype_asserts(datatypes.bool.false, (False, False), False)

    def test_compound_false(self):
        self.first_compound_asserts('bool__false', [], (False, False), False)


class FirstCommandStringDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = 'foo'

    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.string.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.first_compound_asserts('string__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_iexact(self):
        self.first_prototype_asserts(datatypes.string.iexact('FOO'), (self.foo, 'fOo',), self.foo)

    def test_compound_iexact(self):
        self.first_compound_asserts('string__iexact', ['FOO'], (self.foo, self.foo), self.foo)

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.string.contains('o'), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.first_compound_asserts('string__contains', ['o'], (self.foo, self.foo), self.foo)

    def test_prototype_icontains(self):
        self.first_prototype_asserts(datatypes.string.icontains('O'), (self.foo, 'fOo'), self.foo)

    def test_compound_icontains(self):
        self.first_compound_asserts('string__icontains', ['O'], (self.foo, self.foo), self.foo)

    def test_prototype_startswith(self):
        self.first_prototype_asserts(datatypes.string.startswith('f'), (self.foo, self.foo), self.foo)

    def test_compound_startswith(self):
        self.first_compound_asserts('string__startswith', ['f'], (self.foo, self.foo), self.foo)

    def test_prototype_istartswith(self):
        self.first_prototype_asserts(datatypes.string.istartswith('F'), (self.foo, 'fOo'), self.foo)

    def test_compound_istartswith(self):
        self.first_compound_asserts('string__istartswith', ['F'], (self.foo, self.foo), self.foo)

    def test_prototype_endswith(self):
        self.first_prototype_asserts(datatypes.string.endswith('oo'), (self.foo, self.foo), self.foo)

    def test_compound_endswith(self):
        self.first_compound_asserts('string__endswith', ['oo'], (self.foo, self.foo), self.foo)

    def test_prototype_iendswith(self):
        self.first_prototype_asserts(datatypes.string.iendswith('OO'), (self.foo, 'fOo'), self.foo)

    def test_compound_iendswith(self):
        self.first_compound_asserts('string__iendswith', ['OO'], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.string.len(3), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.first_compound_asserts('string__len', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.string.lenlt(4), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.first_compound_asserts('string__lenlt', [4], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.string.lenlte(3), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.first_compound_asserts('string__lenlte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.string.lengt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlgt(self):
        self.first_compound_asserts('string__lengt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.string.lengte(3), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.first_compound_asserts('string__lengte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_isalnum(self):
        self.first_prototype_asserts(datatypes.string.isalnum(), (self.foo, self.foo), self.foo)

    def test_compound_isalnum(self):
        self.first_compound_asserts('string__isalnum', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalnums(self):
        self.first_prototype_asserts(datatypes.string.isalnums(), ('fo o', 'f Oo'), 'fo o')

    def test_compound_isalnums(self):
        self.first_compound_asserts('string__isalnums', [], ('fo o', 'f Oo'), 'fo o')

    def test_prototype_isalpha(self):
        self.first_prototype_asserts(datatypes.string.isalpha(), (self.foo, self.foo), self.foo)

    def test_compound_isalpha(self):
        self.first_compound_asserts('string__isalpha', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalphas(self):
        self.first_prototype_asserts(datatypes.string.isalphas(), ('fo o', 'f Oo'), 'fo o')

    def test_compound_isalphas(self):
        self.first_compound_asserts('string__isalphas', [], ('fo o', 'f Oo'), 'fo o')

    def test_prototype_isdigit(self):
        self.first_prototype_asserts(datatypes.string.isdigit(), ('1', '1'), '1')

    def test_compound_isdigit(self):
        self.first_compound_asserts('string__isdigit', [], ('1', '1'), '1')

    def test_prototype_islower(self):
        self.first_prototype_asserts(datatypes.string.islower(), (self.foo, self.foo), self.foo)

    def test_compound_islower(self):
        self.first_compound_asserts('string__islower', [], (self.foo, self.foo), self.foo)

    def test_prototype_isupper(self):
        self.first_prototype_asserts(datatypes.string.isupper(), ('FOO', 'FOO'), 'FOO')

    def test_compound_isupper(self):
        self.first_compound_asserts('string__isupper', [], ('FOO', 'FOO'), 'FOO')

    def test_prototype_isspace(self):
        self.first_prototype_asserts(datatypes.string.isspace(), ('    ', '    '), '    ')

    def test_compound_isspace(self):
        self.first_compound_asserts('string__isspace', [], ('    ', '    '), '    ')

    def test_prototype_istitle(self):
        self.first_prototype_asserts(datatypes.string.istitle(), ('Foo', 'Foo'), 'Foo')

    def test_compound_istitle(self):
        self.first_compound_asserts('string__istitle', [], ('Foo', 'Foo'), 'Foo')


class FirstCommandUnicodeDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'.decode()

    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.unicode.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.first_compound_asserts('unicode__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_iexact(self):
        self.first_prototype_asserts(datatypes.unicode.iexact(b'FOO'.decode()), (self.foo, b'fOo'.decode(),), self.foo)

    def test_compound_iexact(self):
        self.first_compound_asserts('unicode__iexact', [b'FOO'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.unicode.contains(b'o'.decode()), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.first_compound_asserts('unicode__contains', [b'o'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_icontains(self):
        self.first_prototype_asserts(datatypes.unicode.icontains(b'O'.decode()), (self.foo, b'fOo'.decode()), self.foo)

    def test_compound_icontains(self):
        self.first_compound_asserts('unicode__icontains', [b'O'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_startswith(self):
        self.first_prototype_asserts(datatypes.unicode.startswith(b'f'.decode()), (self.foo, self.foo), self.foo)

    def test_compound_startswith(self):
        self.first_compound_asserts('unicode__startswith', [b'f'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_istartswith(self):
        self.first_prototype_asserts(
            datatypes.unicode.istartswith(b'F'.decode()),
            (self.foo, b'fOo'.decode()), self.foo
        )

    def test_compound_istartswith(self):
        self.first_compound_asserts('unicode__istartswith', [b'F'.decode()], (self.foo, b'foo'.decode()), self.foo)

    def test_prototype_endswith(self):
        self.first_prototype_asserts(datatypes.unicode.endswith(b'oo'.decode()), (self.foo, self.foo), self.foo)

    def test_compound_endswith(self):
        self.first_compound_asserts('unicode__endswith', [b'oo'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_iendswith(self):
        self.first_prototype_asserts(datatypes.unicode.iendswith(b'OO'.decode()), (self.foo, b'fOo'.decode()), self.foo)

    def test_compound_iendswith(self):
        self.first_compound_asserts('unicode__iendswith', [b'OO'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.unicode.len(3), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.first_compound_asserts('unicode__len', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.unicode.lenlt(4), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.first_compound_asserts('unicode__lenlt', [4], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.unicode.lenlte(3), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.first_compound_asserts('unicode__lenlte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.unicode.lengt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlgt(self):
        self.first_compound_asserts('unicode__lengt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.unicode.lengte(3), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.first_compound_asserts('unicode__lengte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_isalnum(self):
        self.first_prototype_asserts(datatypes.unicode.isalnum(), (self.foo, self.foo), self.foo)

    def test_compound_isalnum(self):
        self.first_compound_asserts('unicode__isalnum', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalnums(self):
        self.first_prototype_asserts(
            datatypes.unicode.isalnums(),
            (b'fo o'.decode(), b'f Oo'.decode()),
            b'fo o'.decode()
        )

    def test_compound_isalnums(self):
        self.first_compound_asserts('unicode__isalnums', [], (b'fo o'.decode(), b'f Oo'.decode()), b'fo o'.decode())

    def test_prototype_isalpha(self):
        self.first_prototype_asserts(datatypes.unicode.isalpha(), (self.foo, self.foo), self.foo)

    def test_compound_isalpha(self):
        self.first_compound_asserts('unicode__isalpha', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalphas(self):
        self.first_prototype_asserts(
            datatypes.unicode.isalphas(),
            (b'fo o'.decode(), b'f Oo'.decode()),
            b'fo o'.decode()
        )

    def test_compound_isalphas(self):
        self.first_compound_asserts('unicode__isalphas', [], (b'fo o'.decode(), b'f Oo'.decode()), b'fo o'.decode())

    def test_prototype_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.first_prototype_asserts(datatypes.unicode.isdecimal(), (decimal, decimal), decimal)

    def test_compound_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.first_compound_asserts('unicode__isdecimal', [], (decimal, decimal), decimal)

    def test_prototype_isdigit(self):
        self.first_prototype_asserts(datatypes.unicode.isdigit(), (b'1'.decode(), b'1'.decode()), b'1'.decode())

    def test_compound_isdigit(self):
        self.first_compound_asserts('unicode__isdigit', [], (b'1'.decode(), b'1'.decode()), b'1'.decode())

    def test_prototype_islower(self):
        self.first_prototype_asserts(datatypes.unicode.islower(), (self.foo, self.foo), self.foo)

    def test_compound_islower(self):
        self.first_compound_asserts('unicode__islower', [], (self.foo, self.foo), self.foo)

    def test_prototype_isupper(self):
        self.first_prototype_asserts(datatypes.unicode.isupper(), (b'FOO'.decode(), b'FOO'.decode()), b'FOO'.decode())

    def test_compound_isupper(self):
        self.first_compound_asserts('unicode__isupper', [], (b'FOO'.decode(), b'FOO'.decode()), b'FOO'.decode())

    def test_prototype_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.first_prototype_asserts(datatypes.unicode.isnumeric(), (numeric, numeric), numeric)

    def test_compound_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.first_compound_asserts('unicode__isnumeric', [], (numeric, numeric), numeric)

    def test_prototype_isspace(self):
        space = b'    '.decode()
        self.first_prototype_asserts(datatypes.unicode.isspace(), (space, space), space)

    def test_compound_isspace(self):
        space = b'    '.decode()
        self.first_compound_asserts('unicode__isspace', [], (space, space), space)

    def test_prototype_istitle(self):
        self.first_prototype_asserts(datatypes.unicode.istitle(), (b'Foo'.decode(), b'Foo'.decode()), b'Foo'.decode())

    def test_compound_istitle(self):
        self.first_compound_asserts('unicode__istitle', [], (b'Foo'.decode(), b'Foo'.decode()), b'Foo'.decode())


class FirstCommandBytesDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'

    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.bytes.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.first_compound_asserts('bytes__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_iexact(self):
        self.first_prototype_asserts(datatypes.bytes.iexact(b'FOO'), (self.foo, b'fOo',), self.foo)

    def test_compound_iexact(self):
        self.first_compound_asserts('bytes__iexact', [b'FOO'], (self.foo, self.foo), self.foo)

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.bytes.contains(b'o'), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.first_compound_asserts('bytes__contains', [b'o'], (self.foo, self.foo), self.foo)

    def test_prototype_icontains(self):
        self.first_prototype_asserts(datatypes.bytes.icontains(b'O'), (self.foo, b'fOo'), self.foo)

    def test_compound_icontains(self):
        self.first_compound_asserts('bytes__icontains', [b'O'], (self.foo, self.foo), self.foo)

    def test_prototype_startswith(self):
        self.first_prototype_asserts(datatypes.bytes.startswith(b'f'), (self.foo, self.foo), self.foo)

    def test_compound_startswith(self):
        self.first_compound_asserts('bytes__startswith', [b'f'], (self.foo, self.foo), self.foo)

    def test_prototype_istartswith(self):
        self.first_prototype_asserts(datatypes.bytes.istartswith(b'F'), (self.foo, b'fOo'), self.foo)

    def test_compound_istartswith(self):
        self.first_compound_asserts('bytes__istartswith', [b'F'], (self.foo, self.foo), self.foo)

    def test_prototype_endswith(self):
        self.first_prototype_asserts(datatypes.bytes.endswith(b'oo'), (self.foo, self.foo), self.foo)

    def test_compound_endswith(self):
        self.first_compound_asserts('bytes__endswith', [b'oo'], (self.foo, self.foo), self.foo)

    def test_prototype_iendswith(self):
        self.first_prototype_asserts(datatypes.bytes.iendswith(b'OO'), (self.foo, b'fOo'), self.foo)

    def test_compound_iendswith(self):
        self.first_compound_asserts('bytes__iendswith', [b'OO'], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.bytes.len(3), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.first_compound_asserts('bytes__len', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.bytes.lenlt(4), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.first_compound_asserts('bytes__lenlt', [4], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.bytes.lenlte(3), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.first_compound_asserts('bytes__lenlte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.bytes.lengt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlgt(self):
        self.first_compound_asserts('bytes__lengt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.bytes.lengte(3), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.first_compound_asserts('bytes__lengte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_isalnum(self):
        self.first_prototype_asserts(datatypes.bytes.isalnum(), (self.foo, self.foo), self.foo)

    def test_compound_isalnum(self):
        self.first_compound_asserts('bytes__isalnum', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalnums(self):
        self.first_prototype_asserts(datatypes.bytes.isalnums(), (b'fo o', b'f Oo'), b'fo o')

    def test_compound_isalnums(self):
        self.first_compound_asserts('bytes__isalnums', [], (b'fo o', b'f Oo'), b'fo o')

    def test_prototype_isalpha(self):
        self.first_prototype_asserts(datatypes.bytes.isalpha(), (self.foo, self.foo), self.foo)

    def test_compound_isalpha(self):
        self.first_compound_asserts('bytes__isalpha', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalphas(self):
        self.first_prototype_asserts(datatypes.bytes.isalphas(), (b'fo o', b'f Oo'), b'fo o')

    def test_compound_isalphas(self):
        self.first_compound_asserts('bytes__isalphas', [], (b'fo o', b'f Oo'), b'fo o')

    def test_prototype_isdigit(self):
        self.first_prototype_asserts(datatypes.bytes.isdigit(), (b'1', b'1'), b'1')

    def test_compound_isdigit(self):
        self.first_compound_asserts('bytes__isdigit', [], (b'1', b'1'), b'1')

    def test_prototype_islower(self):
        self.first_prototype_asserts(datatypes.bytes.islower(), (self.foo, self.foo), self.foo)

    def test_compound_islower(self):
        self.first_compound_asserts('bytes__islower', [], (self.foo, self.foo), self.foo)

    def test_prototype_isupper(self):
        self.first_prototype_asserts(datatypes.bytes.isupper(), (b'FOO', b'FOO'), b'FOO')

    def test_compound_isupper(self):
        self.first_compound_asserts('bytes__isupper', [], (b'FOO', b'FOO'), b'FOO')

    def test_prototype_isspace(self):
        self.first_prototype_asserts(datatypes.bytes.isspace(), (b'    ', b'    '), b'    ')

    def test_compound_isspace(self):
        self.first_compound_asserts('bytes__isspace', [], (b'    ', b'    '), b'    ')

    def test_prototype_istitle(self):
        self.first_prototype_asserts(datatypes.bytes.istitle(), (b'Foo', b'Foo'), b'Foo')

    def test_compound_istitle(self):
        self.first_compound_asserts('bytes__istitle', [], (b'Foo', b'Foo'), b'Foo')


class FirstCommandBytearrayDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = bytearray(b'foo')

    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.bytearray.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.first_compound_asserts('bytearray__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_iexact(self):
        self.first_prototype_asserts(
            datatypes.bytearray.iexact(bytearray(b'FOO')),
            (self.foo, bytearray(b'fOo'),),
            self.foo
        )

    def test_compound_iexact(self):
        self.first_compound_asserts('bytearray__iexact', [bytearray(b'FOO')], (self.foo, self.foo), self.foo)

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.bytearray.contains(bytearray(b'o')), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.first_compound_asserts('bytearray__contains', [bytearray(b'o')], (self.foo, self.foo), self.foo)

    def test_prototype_icontains(self):
        self.first_prototype_asserts(
            datatypes.bytearray.icontains(bytearray(b'O')),
            (self.foo, bytearray(b'fOo')),
            self.foo
        )

    def test_compound_icontains(self):
        self.first_compound_asserts('bytearray__icontains', [bytearray(b'O')], (self.foo, self.foo), self.foo)

    def test_prototype_startswith(self):
        self.first_prototype_asserts(datatypes.bytearray.startswith(bytearray(b'f')), (self.foo, self.foo), self.foo)

    def test_compound_startswith(self):
        self.first_compound_asserts('bytearray__startswith', [bytearray(b'f')], (self.foo, self.foo), self.foo)

    def test_prototype_istartswith(self):
        self.first_prototype_asserts(
            datatypes.bytearray.istartswith(bytearray(b'F')),
            (self.foo, bytearray(b'fOo')),
            self.foo
        )

    def test_compound_istartswith(self):
        self.first_compound_asserts('bytearray__istartswith', [bytearray(b'F')], (self.foo, self.foo), self.foo)

    def test_prototype_endswith(self):
        self.first_prototype_asserts(datatypes.bytearray.endswith(bytearray(b'oo')), (self.foo, self.foo), self.foo)

    def test_compound_endswith(self):
        self.first_compound_asserts('bytearray__endswith', [bytearray(b'oo')], (self.foo, self.foo), self.foo)

    def test_prototype_iendswith(self):
        self.first_prototype_asserts(
            datatypes.bytearray.iendswith(bytearray(b'OO')),
            (self.foo, bytearray(b'fOo')),
            self.foo
        )

    def test_compound_iendswith(self):
        self.first_compound_asserts('bytearray__iendswith', [bytearray(b'OO')], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.bytearray.len(3), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.first_compound_asserts('bytearray__len', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.bytearray.lenlt(4), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.first_compound_asserts('bytearray__lenlt', [4], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.bytearray.lenlte(3), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.first_compound_asserts('bytearray__lenlte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.bytearray.lengt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlgt(self):
        self.first_compound_asserts('bytearray__lengt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.bytearray.lengte(3), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.first_compound_asserts('bytearray__lengte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_isalnum(self):
        self.first_prototype_asserts(datatypes.bytearray.isalnum(), (self.foo, self.foo), self.foo)

    def test_compound_isalnum(self):
        self.first_compound_asserts('bytearray__isalnum', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalnums(self):
        self.first_prototype_asserts(
            datatypes.bytearray.isalnums(),
            (bytearray(b'fo o'), bytearray(b'f Oo')),
            bytearray(b'fo o')
        )

    def test_compound_isalnums(self):
        self.first_compound_asserts(
            'bytearray__isalnums',
            [],
            (bytearray(b'fo o'), bytearray(b'f Oo')),
            bytearray(b'fo o')
        )

    def test_prototype_isalpha(self):
        self.first_prototype_asserts(datatypes.bytearray.isalpha(), (self.foo, self.foo), self.foo)

    def test_compound_isalpha(self):
        self.first_compound_asserts('bytearray__isalpha', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalphas(self):
        self.first_prototype_asserts(
            datatypes.bytearray.isalphas(),
            (bytearray(b'fo o'), bytearray(b'f Oo')),
            bytearray(b'fo o')
        )

    def test_compound_isalphas(self):
        self.first_compound_asserts(
            'bytearray__isalphas',
            [],
            (bytearray(b'fo o'), bytearray(b'f Oo')),
            bytearray(b'fo o')
        )

    def test_prototype_isdigit(self):
        self.first_prototype_asserts(datatypes.bytearray.isdigit(), (bytearray(b'1'), bytearray(b'1')), bytearray(b'1'))

    def test_compound_isdigit(self):
        self.first_compound_asserts('bytearray__isdigit', [], (bytearray(b'1'), bytearray(b'1')), bytearray(b'1'))

    def test_prototype_islower(self):
        self.first_prototype_asserts(datatypes.bytearray.islower(), (self.foo, self.foo), self.foo)

    def test_compound_islower(self):
        self.first_compound_asserts('bytearray__islower', [], (self.foo, self.foo), self.foo)

    def test_prototype_isupper(self):
        upper = bytearray(b'FOO')
        self.first_prototype_asserts(datatypes.bytearray.isupper(), (upper, upper), upper)

    def test_compound_isupper(self):
        upper = bytearray(b'FOO')
        self.first_compound_asserts('bytearray__isupper', [], (upper, upper), upper)

    def test_prototype_isspace(self):
        space = bytearray(b'    ')
        self.first_prototype_asserts(datatypes.bytearray.isspace(), (space, space), space)

    def test_compound_isspace(self):
        space = bytearray(b'    ')
        self.first_compound_asserts('bytearray__isspace', [], (space, space), space)

    def test_prototype_istitle(self):
        foo = bytearray(b'Foo')
        self.first_prototype_asserts(datatypes.bytearray.istitle(), (foo, foo), foo)

    def test_compound_istitle(self):
        foo = bytearray(b'Foo')
        self.first_compound_asserts('bytearray__istitle', [], (foo, foo), foo)


class FirstCommandNumericDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.numeric.exact(5.5), (5.5, 5.5), 5.5)

    def test_compound_exact(self):
        self.first_compound_asserts('numeric__exact', [5.5], (5.5, 5.5), 5.5)

    def test_prototype_gt(self):
        self.first_prototype_asserts(datatypes.numeric.gt(3), (4, 4), 4)

    def test_compound_gt(self):
        self.first_compound_asserts('numeric__gt', [3], (4, 4), 4)

    def test_prototype_gte(self):
        self.first_prototype_asserts(datatypes.numeric.gte(5), (5, 5), 5)

    def test_compound_gte(self):
        self.first_compound_asserts('numeric__gte', [5], (5, 5), 5)

    def test_prototype_lt(self):
        self.first_prototype_asserts(datatypes.numeric.lt(2), (1, 1), 1)

    def test_compound_lt(self):
        self.first_compound_asserts('numeric__lt', [2], (1, 1), 1)

    def test_prototype_lte(self):
        self.first_prototype_asserts(datatypes.numeric.lte(2), (2, 2), 2)

    def test_compound_lte(self):
        self.first_compound_asserts('numeric__lte', [2], (2, 2), 2)

    def test_prototype_between(self):
        self.first_prototype_asserts(datatypes.numeric.between(1, 2), (1, 1), 1)

    def test_compound_between(self):
        self.first_compound_asserts('numeric__between', [1, 2], (1, 1), 1)

    def test_prototype_ebetween(self):
        self.first_prototype_asserts(datatypes.numeric.ebetween(0, 2), (1, 1), 1)

    def test_compound_ebetween(self):
        self.first_compound_asserts('numeric__ebetween', [0, 2], (1, 1), 1)

    def test_prototype_isodd(self):
        self.first_prototype_asserts(datatypes.numeric.isodd(), (5, 5), 5)

    def test_compound_isodd(self):
        self.first_compound_asserts('numeric__isodd', [], (5, 5), 5)

    def test_prototype_iseven(self):
        self.first_prototype_asserts(datatypes.numeric.iseven(), (4, 4), 4)

    def test_compound_iseven(self):
        self.first_compound_asserts('numeric__iseven', [], (4, 4), 4)

    def test_prototype_divisibleby(self):
        self.first_prototype_asserts(datatypes.numeric.divisibleby(2), (4, 4), 4)

    def test_compound_divisibleby(self):
        self.first_compound_asserts('numeric__divisibleby', [2], (4, 4), 4)


class FirstCommandIntDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.int.exact(5), (5, 5), 5)

    def test_compound_exact(self):
        self.first_compound_asserts('int__exact', [5], (5, 5), 5)

    def test_prototype_gt(self):
        self.first_prototype_asserts(datatypes.int.gt(3), (4, 4), 4)

    def test_compound_gt(self):
        self.first_compound_asserts('int__gt', [3], (4, 4), 4)

    def test_prototype_gte(self):
        self.first_prototype_asserts(datatypes.int.gte(5), (5, 5), 5)

    def test_compound_gte(self):
        self.first_compound_asserts('int__gte', [5], (5, 5), 5)

    def test_prototype_lt(self):
        self.first_prototype_asserts(datatypes.int.lt(2), (1, 1), 1)

    def test_compound_lt(self):
        self.first_compound_asserts('int__lt', [2], (1, 1), 1)

    def test_prototype_lte(self):
        self.first_prototype_asserts(datatypes.int.lte(2), (2, 2), 2)

    def test_compound_lte(self):
        self.first_compound_asserts('int__lte', [2], (2, 2), 2)

    def test_prototype_between(self):
        self.first_prototype_asserts(datatypes.int.between(1, 2), (1, 1), 1)

    def test_compound_between(self):
        self.first_compound_asserts('int__between', [1, 2], (1, 1), 1)

    def test_prototype_ebetween(self):
        self.first_prototype_asserts(datatypes.int.ebetween(0, 2), (1, 1), 1)

    def test_compound_ebetween(self):
        self.first_compound_asserts('int__ebetween', [0, 2], (1, 1), 1)

    def test_prototype_isodd(self):
        self.first_prototype_asserts(datatypes.int.isodd(), (5, 5), 5)

    def test_compound_isodd(self):
        self.first_compound_asserts('int__isodd', [], (5, 5), 5)

    def test_prototype_iseven(self):
        self.first_prototype_asserts(datatypes.int.iseven(), (4, 4), 4)

    def test_compound_iseven(self):
        self.first_compound_asserts('int__iseven', [], (4, 4), 4)

    def test_prototype_divisibleby(self):
        self.first_prototype_asserts(datatypes.int.divisibleby(2), (4, 4), 4)

    def test_compound_divisibleby(self):
        self.first_compound_asserts('int__divisibleby', [2], (4, 4), 4)


class FirstCommandFloatDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.float.exact(5.5), (5.5, 5.5), 5.5)

    def test_compound_exact(self):
        self.first_compound_asserts('float__exact', [5.5], (5.5, 5.5), 5.5)

    def test_prototype_gt(self):
        self.first_prototype_asserts(datatypes.float.gt(3), (4.2, 4.2), 4.2)

    def test_compound_gt(self):
        self.first_compound_asserts('float__gt', [3], (4.2, 4.2), 4.2)

    def test_prototype_gte(self):
        self.first_prototype_asserts(datatypes.float.gte(5), (5.5, 5.5), 5.5)

    def test_compound_gte(self):
        self.first_compound_asserts('float__gte', [5], (5.5, 5.5), 5.5)

    def test_prototype_lt(self):
        self.first_prototype_asserts(datatypes.float.lt(2), (1.1, 1.1), 1.1)

    def test_compound_lt(self):
        self.first_compound_asserts('float__lt', [2], (1.1, 1.1), 1.1)

    def test_prototype_lte(self):
        self.first_prototype_asserts(datatypes.float.lte(2), (1.8, 1.8), 1.8)

    def test_compound_lte(self):
        self.first_compound_asserts('float__lte', [2], (1.8, 1.8), 1.8)

    def test_prototype_between(self):
        self.first_prototype_asserts(datatypes.float.between(1, 2), (1.4, 1.4), 1.4)

    def test_compound_between(self):
        self.first_compound_asserts('float__between', [1, 2], (1.4, 1.4), 1.4)

    def test_prototype_ebetween(self):
        self.first_prototype_asserts(datatypes.float.ebetween(0, 2), (1.5, 1.5), 1.5)

    def test_compound_ebetween(self):
        self.first_compound_asserts('float__ebetween', [0, 2], (1.5, 1.5), 1.5)

    def test_prototype_isinteger(self):
        self.first_prototype_asserts(datatypes.float.isinteger(), (5.0, 5.0), 5.0)

    def test_compound_isinteger(self):
        self.first_compound_asserts('float__isinteger', [], (5.0, 5.0), 5.0)

    def test_prototype_isodd(self):
        self.first_prototype_asserts(datatypes.float.isodd(), (5.2, 5.2), 5.2)

    def test_compound_isodd(self):
        self.first_compound_asserts('float__isodd', [], (5.2, 5.2), 5.2)

    def test_prototype_iseven(self):
        self.first_prototype_asserts(datatypes.float.iseven(), (4.3, 4.3), 4.3)

    def test_compound_iseven(self):
        self.first_compound_asserts('float__iseven', [], (4.3, 4.3), 4.3)

    def test_prototype_divisibleby(self):
        self.first_prototype_asserts(datatypes.float.divisibleby(2), (4.7, 4.7), 4.7)

    def test_compound_divisibleby(self):
        self.first_compound_asserts('float__divisibleby', [2], (4.7, 4.7), 4.7)


class FirstCommandLongDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.long.exact(2 ** 64), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_exact(self):
        self.first_compound_asserts('long__exact', [2 ** 64], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_gt(self):
        self.first_prototype_asserts(datatypes.long.gt(2 ** 63), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_gt(self):
        self.first_compound_asserts('long__gt', [2 ** 63], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_gte(self):
        self.first_prototype_asserts(datatypes.long.gte(2 ** 64), (2 ** 65, 2 ** 65), 2 ** 65)

    def test_compound_gte(self):
        self.first_compound_asserts('long__gte', [2 ** 64], (2 ** 65, 2 ** 65), 2 ** 65)

    def test_prototype_lt(self):
        self.first_prototype_asserts(datatypes.long.lt(2 ** 64), (2 ** 63, 2 ** 63), 2 ** 63)

    def test_compound_lt(self):
        self.first_compound_asserts('long__lt', [2 ** 64], (2 ** 63, 2 ** 63), 2 ** 63)

    def test_prototype_lte(self):
        self.first_prototype_asserts(datatypes.long.lte(2 ** 64), (2 ** 63, 2 ** 63), 2 ** 63)

    def test_compound_lte(self):
        self.first_compound_asserts('long__lte', [2 ** 64], (2 ** 63, 2 ** 63), 2 ** 63)

    def test_prototype_between(self):
        self.first_prototype_asserts(datatypes.long.between(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_between(self):
        self.first_compound_asserts('long__between', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_ebetween(self):
        self.first_prototype_asserts(datatypes.long.ebetween(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_ebetween(self):
        self.first_compound_asserts('long__ebetween', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_isodd(self):
        self.first_prototype_asserts(datatypes.long.isodd(), (3 ** 64, 3 ** 64), 3 ** 64)

    def test_compound_isodd(self):
        self.first_compound_asserts('long__isodd', [], (3 ** 64, 3 ** 64), 3 ** 64)

    def test_prototype_iseven(self):
        self.first_prototype_asserts(datatypes.long.iseven(), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_iseven(self):
        self.first_compound_asserts('long__iseven', [], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_divisibleby(self):
        self.first_prototype_asserts(datatypes.long.divisibleby(2), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_divisibleby(self):
        self.first_compound_asserts('long__divisibleby', [2], (2 ** 64, 2 ** 64), 2 ** 64)


class FirstCommandComplexDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.complex.exact(1j), (1j, 1j), 1j)

    def test_compound_exact(self):
        self.first_compound_asserts('complex__exact', [1j], (1j, 1j), 1j)


class FirstCommandIterableDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.iterable.exact(['foo']), (['foo'], ['foo']), ['foo'])

    def test_compound_exact(self):
        self.first_compound_asserts('iterable__exact', [['foo']], (['foo'], ['foo']), ['foo'])

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.iterable.len(1), (['foo'], ['foo']), ['foo'])

    def test_compound_len(self):
        self.first_compound_asserts('iterable__len', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.iterable.lenlt(2), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlt(self):
        self.first_compound_asserts('iterable__lenlt', [2], (['foo'], ['foo']), ['foo'])

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.iterable.lenlte(2), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlte(self):
        self.first_compound_asserts('iterable__lenlte', [2], (['foo'], ['foo']), ['foo'])

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.iterable.lengt(0), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlgt(self):
        self.first_compound_asserts('iterable__lengt', [0], (['foo'], ['foo']), ['foo'])

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.iterable.lengte(1), (['foo'], ['foo']), ['foo'])

    def test_compound_lengte(self):
        self.first_compound_asserts('iterable__lengte', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.iterable.contains('foo'), (['foo'], ('foo',)), ['foo'])

    def test_compound_contains(self):
        self.first_compound_asserts('iterable__contains', ['foo'], (['foo'], ['foo']), ['foo'])

    def test_prototype_contains_all(self):
        self.first_prototype_asserts(datatypes.iterable.contains_all(['f', 'o']), (['f', 'o'], ('f', 'o')), ['f', 'o'])

    def test_compound_contains_all(self):
        self.first_compound_asserts('iterable__contains_all', [['f', 'o']], (['f', 'o'], ('f', 'o')), ['f', 'o'])

    def test_prototype_contains_any(self):
        self.first_prototype_asserts(datatypes.iterable.contains_any(['f', 'z']), (['f', 'o'], ('f', 'o')), ['f', 'o'])

    def test_compound_contains_any(self):
        self.first_compound_asserts('iterable__contains_any', [['f', 'z']], (['f', 'o'], ('f', 'o')), ['f', 'o'])

    def test_prototype_str_contains_str(self):
        self.first_prototype_asserts(datatypes.iterable.str_contains_str('f'), (['fo'], ('fo',)), ['fo'])

    def test_compound_str_contains_str(self):
        self.first_compound_asserts('iterable__str_contains_str', ['f'], (['fo'], ('fo',)), ['fo'])


class FirstCommandListDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.list.exact(['foo']), (['foo'], ['foo']), ['foo'])

    def test_compound_exact(self):
        self.first_compound_asserts('list__exact', [['foo']], (['foo'], ['foo']), ['foo'])

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.list.len(1), (['foo'], ['foo']), ['foo'])

    def test_compound_len(self):
        self.first_compound_asserts('list__len', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.list.lenlt(2), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlt(self):
        self.first_compound_asserts('list__lenlt', [2], (['foo'], ['foo']), ['foo'])

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.list.lenlte(2), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlte(self):
        self.first_compound_asserts('list__lenlte', [2], (['foo'], ['foo']), ['foo'])

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.list.lengt(0), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlgt(self):
        self.first_compound_asserts('list__lengt', [0], (['foo'], ['foo']), ['foo'])

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.list.lengte(1), (['foo'], ['foo']), ['foo'])

    def test_compound_lengte(self):
        self.first_compound_asserts('list__lengte', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.list.contains('foo'), (['foo'], ['foo']), ['foo'])

    def test_compound_contains(self):
        self.first_compound_asserts('list__contains', ['foo'], (['foo'], ['foo']), ['foo'])

    def test_prototype_contains_all(self):
        self.first_prototype_asserts(datatypes.list.contains_all(['f', 'o']), (['f', 'o'], ['f', 'o']), ['f', 'o'])

    def test_compound_contains_all(self):
        self.first_compound_asserts('list__contains_all', [['f', 'o']], (['f', 'o'], ['f', 'o']), ['f', 'o'])

    def test_prototype_contains_any(self):
        self.first_prototype_asserts(datatypes.list.contains_any(['f', 'z']), (['f', 'o'], ['f', 'o']), ['f', 'o'])

    def test_compound_contains_any(self):
        self.first_compound_asserts('list__contains_any', [['f', 'z']], (['f', 'o'], ['f', 'o']), ['f', 'o'])

    def test_prototype_str_contains_str(self):
        self.first_prototype_asserts(datatypes.list.str_contains_str('f'), (['fo'], ['fo']), ['fo'])

    def test_compound_str_contains_str(self):
        self.first_compound_asserts('list__str_contains_str', ['f'], (['fo'], ['fo']), ['fo'])


class FirstCommandTupleDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.tuple.exact(('foo',)), (('foo',), ('foo',)), ('foo',))

    def test_compound_exact(self):
        self.first_compound_asserts('tuple__exact', [('foo',)], (('foo',), ('foo',)), ('foo',))

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.tuple.len(1), (('foo',), ('foo',)), ('foo',))

    def test_compound_len(self):
        self.first_compound_asserts('tuple__len', [1], (('foo',), ('foo',)), ('foo',))

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.tuple.lenlt(2), (('foo',), ('foo',)), ('foo',))

    def test_compound_lenlt(self):
        self.first_compound_asserts('tuple__lenlt', [2], (('foo',), ('foo',)), ('foo',))

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.tuple.lenlte(2), (('foo',), ('foo',)), ('foo',))

    def test_compound_lenlte(self):
        self.first_compound_asserts('tuple__lenlte', [2], (('foo',), ('foo',)), ('foo',))

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.tuple.lengt(0), (('foo',), ('foo',)), ('foo',))

    def test_compound_lenlgt(self):
        self.first_compound_asserts('tuple__lengt', [0], (('foo',), ('foo',)), ('foo',))

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.tuple.lengte(1), (('foo',), ('foo',)), ('foo',))

    def test_compound_lengte(self):
        self.first_compound_asserts('tuple__lengte', [1], (('foo',), ('foo',)), ('foo',))

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.tuple.contains('foo'), (('foo',), ('foo',)), ('foo',))

    def test_compound_contains(self):
        self.first_compound_asserts('tuple__contains', ['foo'], (('foo',), ('foo',)), ('foo',))

    def test_prototype_contains_all(self):
        self.first_prototype_asserts(datatypes.tuple.contains_all(('f', 'o')), (('f', 'o'), ('f', 'o')), ('f', 'o'))

    def test_compound_contains_all(self):
        self.first_compound_asserts('tuple__contains_all', [('f', 'o')], (('f', 'o'), ('f', 'o')), ('f', 'o'))

    def test_prototype_contains_any(self):
        self.first_prototype_asserts(datatypes.tuple.contains_any(('f', 'z')), (('f', 'o'), ('f', 'o')), ('f', 'o'))

    def test_compound_contains_any(self):
        self.first_compound_asserts('tuple__contains_any', [('f', 'z')], (('f', 'o'), ('f', 'o')), ('f', 'o'))

    def test_prototype_str_contains_str(self):
        self.first_prototype_asserts(datatypes.tuple.str_contains_str('f'), (('fo',), ('fo',)), ('fo',))

    def test_compound_str_contains_str(self):
        self.first_compound_asserts('tuple__str_contains_str', ['f'], (('fo',), ('fo',)), ('fo',))


class FirstCommandSetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = set(['foo'])

    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.set.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.first_compound_asserts('set__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.set.len(1), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.first_compound_asserts('set__len', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.set.lenlt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.first_compound_asserts('set__lenlt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.set.lenlte(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.first_compound_asserts('set__lenlte', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.set.lengt(0), (self.foo, self.foo), self.foo)

    def test_compound_lenlgt(self):
        self.first_compound_asserts('set__lengt', [0], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.set.lengte(1), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.first_compound_asserts('set__lengte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.set.contains('foo'), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.first_compound_asserts('set__contains', ['foo'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_all(self):
        foo = set(['f', 'o'])
        self.first_prototype_asserts(datatypes.set.contains_all(['f', 'o']), (foo, foo), foo)

    def test_compound_contains_all(self):
        foo = set(['f', 'o'])
        self.first_compound_asserts('set__contains_all', [['f', 'o']], (foo, foo), foo)

    def test_prototype_contains_any(self):
        foo = set(['f', 'o'])
        self.first_prototype_asserts(datatypes.set.contains_any(['f', 'z']), (foo, foo), foo)

    def test_compound_contains_any(self):
        foo = set(['f', 'o'])
        self.first_compound_asserts('set__contains_any', [['f', 'z']], (foo, foo), foo)

    def test_prototype_str_contains_str(self):
        foo = set(['fo'])
        self.first_prototype_asserts(datatypes.set.str_contains_str('f'), (foo, foo), foo)

    def test_compound_str_contains_str(self):
        foo = set(['fo'])
        self.first_compound_asserts('set__str_contains_str', ['f'], (foo, foo), foo)

    def test_prototype_isdisjoint(self):
        self.first_prototype_asserts(datatypes.set.isdisjoint(set(['bar'])), (self.foo, self.foo), self.foo)

    def test_compound_isdisjoint(self):
        self.first_compound_asserts('set__isdisjoint', [set(['bar'])], (self.foo, self.foo), self.foo)

    def test_prototype_issubset(self):
        self.first_prototype_asserts(datatypes.set.issubset(set(['foo'])), (self.foo, self.foo), self.foo)

    def test_compound_issubset(self):
        self.first_compound_asserts('set__issubset', [set(['foo'])], (self.foo, self.foo), self.foo)

    def test_prototype_eissubset(self):
        self.first_prototype_asserts(datatypes.set.eissubset(set(['foo', 'bar'])), (self.foo, self.foo), self.foo)

    def test_compound_eissubset(self):
        self.first_compound_asserts('set__eissubset', [set(['foo', 'bar'])], (self.foo, self.foo), self.foo)

    def test_prototype_issuperset(self):
        self.first_prototype_asserts(datatypes.set.issuperset(set(['foo'])), (self.foo, self.foo), self.foo)

    def test_compound_issuperset(self):
        self.first_compound_asserts('set__issuperset', [set(['foo'])], (self.foo, self.foo), self.foo)

    def test_prototype_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.first_prototype_asserts(datatypes.set.eissuperset(set(['foo'])), (foo, foo), foo)

    def test_compound_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.first_compound_asserts('set__eissuperset', [set(['foo'])], (foo, foo), foo)


class FirstCommandFrozensetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = frozenset(['foo'])

    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.frozenset.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.first_compound_asserts('frozenset__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.frozenset.len(1), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.first_compound_asserts('frozenset__len', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.frozenset.lenlt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.first_compound_asserts('frozenset__lenlt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.frozenset.lenlte(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.first_compound_asserts('frozenset__lenlte', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.frozenset.lengt(0), (self.foo, self.foo), self.foo)

    def test_compound_lenlgt(self):
        self.first_compound_asserts('frozenset__lengt', [0], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.frozenset.lengte(1), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.first_compound_asserts('frozenset__lengte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_contains(self):
        self.first_prototype_asserts(datatypes.frozenset.contains('foo'), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.first_compound_asserts('frozenset__contains', ['foo'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.first_prototype_asserts(datatypes.frozenset.contains_all(['f', 'o']), (foo, foo), foo)

    def test_compound_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.first_compound_asserts('frozenset__contains_all', [['f', 'o']], (foo, foo), foo)

    def test_prototype_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.first_prototype_asserts(datatypes.frozenset.contains_any(['f', 'z']), (foo, foo), foo)

    def test_compound_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.first_compound_asserts('frozenset__contains_any', [['f', 'z']], (foo, foo), foo)

    def test_prototype_str_contains_str(self):
        foo = frozenset(['fo'])
        self.first_prototype_asserts(datatypes.frozenset.str_contains_str('f'), (foo, foo), foo)

    def test_compound_str_contains_str(self):
        foo = frozenset(['fo'])
        self.first_compound_asserts('frozenset__str_contains_str', ['f'], (foo, foo), foo)

    def test_prototype_isdisjoint(self):
        self.first_prototype_asserts(datatypes.frozenset.isdisjoint(frozenset(['bar'])), (self.foo, self.foo), self.foo)

    def test_compound_isdisjoint(self):
        self.first_compound_asserts('frozenset__isdisjoint', [frozenset(['bar'])], (self.foo, self.foo), self.foo)

    def test_prototype_issubset(self):
        self.first_prototype_asserts(datatypes.frozenset.issubset(frozenset(['foo'])), (self.foo, self.foo), self.foo)

    def test_compound_issubset(self):
        self.first_compound_asserts('frozenset__issubset', [frozenset(['foo'])], (self.foo, self.foo), self.foo)

    def test_prototype_eissubset(self):
        foo = frozenset(['foo', 'bar'])
        self.first_prototype_asserts(datatypes.frozenset.eissubset(foo), (self.foo, self.foo), self.foo)

    def test_compound_eissubset(self):
        self.first_compound_asserts('frozenset__eissubset', [frozenset(['foo', 'bar'])], (self.foo, self.foo), self.foo)

    def test_prototype_issuperset(self):
        self.first_prototype_asserts(datatypes.frozenset.issuperset(frozenset(['foo'])), (self.foo, self.foo), self.foo)

    def test_compound_issuperset(self):
        self.first_compound_asserts('frozenset__issuperset', [frozenset(['foo'])], (self.foo, self.foo), self.foo)

    def test_prototype_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.first_prototype_asserts(datatypes.frozenset.eissuperset(frozenset(['foo'])), (foo, foo), foo)

    def test_compound_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.first_compound_asserts('frozenset__eissuperset', [frozenset(['foo'])], (foo, foo), foo)


class FirstCommandDictDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = {'foo': 'bar'}

    def test_prototype_exact(self):
        self.first_prototype_asserts(datatypes.dict.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.first_compound_asserts('dict__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.first_prototype_asserts(datatypes.dict.len(1), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.first_compound_asserts('dict__len', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.first_prototype_asserts(datatypes.dict.lenlt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.first_compound_asserts('dict__lenlt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.first_prototype_asserts(datatypes.dict.lenlte(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.first_compound_asserts('dict__lenlte', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.first_prototype_asserts(datatypes.dict.lengt(0), (self.foo, self.foo), self.foo)

    def test_compound_lenlgt(self):
        self.first_compound_asserts('dict__lengt', [0], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.first_prototype_asserts(datatypes.dict.lengte(1), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.first_compound_asserts('dict__lengte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_contains_key(self):
        self.first_prototype_asserts(datatypes.dict.contains_key('foo'), (self.foo, self.foo), self.foo)

    def test_compound_contains_key(self):
        self.first_compound_asserts('dict__contains_key', ['foo'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.first_prototype_asserts(datatypes.dict.contains_all_keys(['foo', 'bar']), (foo, foo), foo)

    def test_compound_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.first_compound_asserts('dict__contains_all_keys', [['foo', 'bar']], (foo, foo), foo)

    def test_prototype_contains_any_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.first_prototype_asserts(datatypes.dict.contains_any_keys(['foo', 'z']), (foo, foo), foo)

    def test_compound_contains_any_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.first_compound_asserts('dict__contains_any_keys', [['foo', 'z']], (foo, foo), foo)

    def test_prototype_key_contains_str(self):
        self.first_prototype_asserts(datatypes.dict.key_contains_str('f'), (self.foo, self.foo), self.foo)

    def test_compound_key_contains_str(self):
        self.first_compound_asserts('dict__key_contains_str', ['f'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_value(self):
        self.first_prototype_asserts(datatypes.dict.contains_value('bar'), (self.foo, self.foo), self.foo)

    def test_compound_contains_value(self):
        self.first_compound_asserts('dict__contains_value', ['bar'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.first_prototype_asserts(datatypes.dict.contains_all_values(['baz', 'bar']), (foo, foo), foo)

    def test_compound_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.first_compound_asserts('dict__contains_all_values', [['baz', 'bar']], (foo, foo), foo)

    def test_prototype_contains_any_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.first_prototype_asserts(datatypes.dict.contains_any_values(['baz', 'z']), (foo, foo), foo)

    def test_compound_contains_any_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.first_compound_asserts('dict__contains_any_values', [['baz', 'z']], (foo, foo), foo)

    def test_prototype_value_contains_str(self):
        self.first_prototype_asserts(datatypes.dict.value_contains_str('b'), (self.foo, self.foo), self.foo)

    def test_compound_value_contains_str(self):
        self.first_compound_asserts('dict__value_contains_str', ['b'], (self.foo, self.foo), self.foo)


class LastCommandTestCase(unittest.TestCase):
    def test_prototype(self):
        self.assertIsInstance(commands.last(datatypes.bool), commands.Command)
        self.assertEqual(commands.last(datatypes.bool).limit, 0)
        self.assertEqual(commands.last(datatypes.bool).inside([]), None)


class LastCommandBoolDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.bool.exact(True), (True, True), True)

    def test_compound_exact(self):
        self.last_compound_asserts('bool__exact', [True], (True, True), True)

    def test_prototype_true(self):
        self.last_prototype_asserts(datatypes.bool.true, (True, True), True)

    def test_compound_true(self):
        self.last_compound_asserts('bool__true', [], (True, True), True)

    def test_prototype_false(self):
        self.last_prototype_asserts(datatypes.bool.false, (False, False), False)

    def test_compound_false(self):
        self.last_compound_asserts('bool__false', [], (False, False), False)


class LastCommandStringDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = 'foo'

    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.string.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.last_compound_asserts('string__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_iexact(self):
        self.last_prototype_asserts(datatypes.string.iexact('FOO'), (self.foo, 'fOo',), 'fOo')

    def test_compound_iexact(self):
        self.last_compound_asserts('string__iexact', ['FOO'], (self.foo, 'fOo',), 'fOo')

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.string.contains('o'), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.last_compound_asserts('string__contains', ['o'], (self.foo, self.foo), self.foo)

    def test_prototype_icontains(self):
        self.last_prototype_asserts(datatypes.string.icontains('O'), (self.foo, 'fOo'), 'fOo')

    def test_compound_icontains(self):
        self.last_compound_asserts('string__icontains', ['O'], (self.foo, 'fOo'), 'fOo')

    def test_prototype_startswith(self):
        self.last_prototype_asserts(datatypes.string.startswith('f'), (self.foo, self.foo), self.foo)

    def test_compound_startswith(self):
        self.last_compound_asserts('string__startswith', ['f'], (self.foo, self.foo), self.foo)

    def test_prototype_istartswith(self):
        self.last_prototype_asserts(datatypes.string.istartswith('F'), (self.foo, 'fOo'), 'fOo')

    def test_compound_istartswith(self):
        self.last_compound_asserts('string__istartswith', ['F'], (self.foo, 'fOo'), 'fOo')

    def test_prototype_endswith(self):
        self.last_prototype_asserts(datatypes.string.endswith('oo'), (self.foo, self.foo), self.foo)

    def test_compound_endswith(self):
        self.last_compound_asserts('string__endswith', ['oo'], (self.foo, self.foo), self.foo)

    def test_prototype_iendswith(self):
        self.last_prototype_asserts(datatypes.string.iendswith('OO'), (self.foo, 'fOo'), 'fOo')

    def test_compound_iendswith(self):
        self.last_compound_asserts('string__iendswith', ['OO'], (self.foo, 'fOo'), 'fOo')

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.string.len(3), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.last_compound_asserts('string__len', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.string.lenlt(4), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.last_compound_asserts('string__lenlt', [4], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.string.lenlte(3), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.last_compound_asserts('string__lenlte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.string.lengt(2), (self.foo, self.foo), self.foo)

    def test_compound_lengt(self):
        self.last_compound_asserts('string__lengt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.string.lengte(3), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.last_compound_asserts('string__lengte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_isalnum(self):
        self.last_prototype_asserts(datatypes.string.isalnum(), (self.foo, self.foo), self.foo)

    def test_compound_isalnum(self):
        self.last_compound_asserts('string__isalnum', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalnums(self):
        self.last_prototype_asserts(datatypes.string.isalnums(), ('fo o', 'f Oo'), 'f Oo')

    def test_compound_isalnums(self):
        self.last_compound_asserts('string__isalnums', [], ('fo o', 'f Oo'), 'f Oo')

    def test_prototype_isalpha(self):
        self.last_prototype_asserts(datatypes.string.isalpha(), (self.foo, self.foo), self.foo)

    def test_compound_isalpha(self):
        self.last_compound_asserts('string__isalpha', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalphas(self):
        self.last_prototype_asserts(datatypes.string.isalphas(), ('fo o', 'f Oo'), 'f Oo')

    def test_compound_isalphas(self):
        self.last_compound_asserts('string__isalphas', [], ('fo o', 'f Oo'), 'f Oo')

    def test_prototype_isdigit(self):
        self.last_prototype_asserts(datatypes.string.isdigit(), ('1', '1'), '1')

    def test_compound_isdigit(self):
        self.last_compound_asserts('string__isdigit', [], ('1', '1'), '1')

    def test_prototype_islower(self):
        self.last_prototype_asserts(datatypes.string.islower(), (self.foo, self.foo), self.foo)

    def test_compound_islower(self):
        self.last_compound_asserts('string__islower', [], (self.foo, self.foo), self.foo)

    def test_prototype_isupper(self):
        self.last_prototype_asserts(datatypes.string.isupper(), ('FOO', 'FOO'), 'FOO')

    def test_compound_isupper(self):
        self.last_compound_asserts('string__isupper', [], ('FOO', 'FOO'), 'FOO')

    def test_prototype_isspace(self):
        self.last_prototype_asserts(datatypes.string.isspace(), ('    ', '    '), '    ')

    def test_compound_isspace(self):
        self.last_compound_asserts('string__isspace', [], ('    ', '    '), '    ')

    def test_prototype_istitle(self):
        self.last_prototype_asserts(datatypes.string.istitle(), ('Foo', 'Foo'), 'Foo')

    def test_compound_istitle(self):
        self.last_compound_asserts('string__istitle', [], ('Foo', 'Foo'), 'Foo')


class LastCommandUnicodeDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'.decode()

    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.unicode.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.last_compound_asserts('unicode__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_iexact(self):
        self.last_prototype_asserts(
            datatypes.unicode.iexact(b'FOO'.decode()),
            (self.foo, b'fOo'.decode(),),
            b'fOo'.decode()
        )

    def test_compound_iexact(self):
        self.last_compound_asserts(
            'unicode__iexact',
            [b'FOO'.decode()],
            (self.foo, b'fOo'.decode(),),
            b'fOo'.decode()
        )

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.unicode.contains(b'o'.decode()), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.last_compound_asserts('unicode__contains', [b'o'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_icontains(self):
        self.last_prototype_asserts(
            datatypes.unicode.icontains(b'O'.decode()),
            (self.foo, b'fOo'.decode()),
            b'fOo'.decode()
        )

    def test_compound_icontains(self):
        self.last_compound_asserts(
            'unicode__icontains',
            [b'O'.decode()],
            (self.foo, b'fOo'.decode()),
            b'fOo'.decode()
        )

    def test_prototype_startswith(self):
        self.last_prototype_asserts(datatypes.unicode.startswith(b'f'.decode()), (self.foo, self.foo), self.foo)

    def test_compound_startswith(self):
        self.last_compound_asserts('unicode__startswith', [b'f'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_istartswith(self):
        self.last_prototype_asserts(
            datatypes.unicode.istartswith(b'F'.decode()),
            (self.foo, b'fOo'.decode()),
            b'fOo'.decode()
        )

    def test_compound_istartswith(self):
        self.last_compound_asserts(
            'unicode__istartswith',
            [b'F'.decode()],
            (self.foo, b'fOo'.decode()),
            b'fOo'.decode()
        )

    def test_prototype_endswith(self):
        self.last_prototype_asserts(datatypes.unicode.endswith(b'oo'.decode()), (self.foo, self.foo), self.foo)

    def test_compound_endswith(self):
        self.last_compound_asserts('unicode__endswith', [b'oo'.decode()], (self.foo, self.foo), self.foo)

    def test_prototype_iendswith(self):
        self.last_prototype_asserts(
            datatypes.unicode.iendswith(b'OO'.decode()),
            (self.foo, b'fOo'.decode()),
            b'fOo'.decode()
        )

    def test_compound_iendswith(self):
        self.last_compound_asserts(
            'unicode__iendswith',
            [b'OO'.decode()],
            (self.foo, b'fOo'.decode()),
            b'fOo'.decode()
        )

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.unicode.len(3), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.last_compound_asserts('unicode__len', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.unicode.lenlt(4), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.last_compound_asserts('unicode__lenlt', [4], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.unicode.lenlte(3), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.last_compound_asserts('unicode__lenlte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.unicode.lengt(2), (self.foo, self.foo), self.foo)

    def test_compound_lengt(self):
        self.last_compound_asserts('unicode__lengt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.unicode.lengte(3), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.last_compound_asserts('unicode__lengte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_isalnum(self):
        self.last_prototype_asserts(datatypes.unicode.isalnum(), (self.foo, self.foo), self.foo)

    def test_compound_isalnum(self):
        self.last_compound_asserts('unicode__isalnum', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalnums(self):
        self.last_prototype_asserts(
            datatypes.unicode.isalnums(),
            (b'fo o'.decode(), b'f Oo'.decode()),
            b'f Oo'.decode()
        )

    def test_compound_isalnums(self):
        self.last_compound_asserts('unicode__isalnums', [], (b'fo o'.decode(), b'f Oo'.decode()), b'f Oo'.decode())

    def test_prototype_isalpha(self):
        self.last_prototype_asserts(datatypes.unicode.isalpha(), (self.foo, self.foo), self.foo)

    def test_compound_isalpha(self):
        self.last_compound_asserts('unicode__isalpha', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalphas(self):
        self.last_prototype_asserts(
            datatypes.unicode.isalphas(),
            (b'fo o'.decode(), b'f Oo'.decode()),
            b'f Oo'.decode()
        )

    def test_compound_isalphas(self):
        self.last_compound_asserts('unicode__isalphas', [], (b'fo o'.decode(), b'f Oo'.decode()), b'f Oo'.decode())

    def test_prototype_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.last_prototype_asserts(datatypes.unicode.isdecimal(), (decimal, decimal), decimal)

    def test_compound_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.last_compound_asserts('unicode__isdecimal', [], (decimal, decimal), decimal)

    def test_prototype_isdigit(self):
        self.last_prototype_asserts(datatypes.unicode.isdigit(), (b'1'.decode(), b'1'.decode()), b'1'.decode())

    def test_compound_isdigit(self):
        self.last_compound_asserts('unicode__isdigit', [], (b'1'.decode(), b'1'.decode()), b'1'.decode())

    def test_prototype_islower(self):
        self.last_prototype_asserts(datatypes.unicode.islower(), (self.foo, self.foo), self.foo)

    def test_compound_islower(self):
        self.last_compound_asserts('unicode__islower', [], (self.foo, self.foo), self.foo)

    def test_prototype_isupper(self):
        upper = b'FOO'.decode()
        self.last_prototype_asserts(datatypes.unicode.isupper(), (upper, upper), upper)

    def test_compound_isupper(self):
        upper = b'FOO'.decode()
        self.last_compound_asserts('unicode__isupper', [], (upper, upper), upper)

    def test_prototype_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.last_prototype_asserts(datatypes.unicode.isnumeric(), (numeric, numeric), numeric)

    def test_compound_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.last_compound_asserts('unicode__isnumeric', [], (numeric, numeric), numeric)

    def test_prototype_isspace(self):
        space = b'    '.decode()
        self.last_prototype_asserts(datatypes.unicode.isspace(), (space, space), space)

    def test_compound_isspace(self):
        space = b'    '.decode()
        self.last_compound_asserts('unicode__isspace', [], (space, space), space)

    def test_prototype_istitle(self):
        foo = b'Foo'.decode()
        self.last_prototype_asserts(datatypes.unicode.istitle(), (foo, foo), foo)

    def test_compound_istitle(self):
        foo = b'Foo'.decode()
        self.last_compound_asserts('unicode__istitle', [], (foo, foo), foo)


class LastCommandBytesDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'

    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.bytes.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.last_compound_asserts('bytes__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_iexact(self):
        self.last_prototype_asserts(datatypes.bytes.iexact(b'FOO'), (self.foo, b'fOo',), b'fOo')

    def test_compound_iexact(self):
        self.last_compound_asserts('bytes__iexact', [b'FOO'], (self.foo, b'fOo',), b'fOo')

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.bytes.contains(b'o'), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.last_compound_asserts('bytes__contains', [b'o'], (self.foo, self.foo), self.foo)

    def test_prototype_icontains(self):
        self.last_prototype_asserts(datatypes.bytes.icontains(b'O'), (self.foo, b'fOo'), b'fOo')

    def test_compound_icontains(self):
        self.last_compound_asserts('bytes__icontains', [b'O'], (self.foo, b'fOo'), b'fOo')

    def test_prototype_startswith(self):
        self.last_prototype_asserts(datatypes.bytes.startswith(b'f'), (self.foo, self.foo), self.foo)

    def test_compound_startswith(self):
        self.last_compound_asserts('bytes__startswith', [b'f'], (self.foo, self.foo), self.foo)

    def test_prototype_istartswith(self):
        self.last_prototype_asserts(datatypes.bytes.istartswith(b'F'), (self.foo, b'fOo'), b'fOo')

    def test_compound_istartswith(self):
        self.last_compound_asserts('bytes__istartswith', [b'F'], (self.foo, b'fOo'), b'fOo')

    def test_prototype_endswith(self):
        self.last_prototype_asserts(datatypes.bytes.endswith(b'oo'), (self.foo, self.foo), self.foo)

    def test_compound_endswith(self):
        self.last_compound_asserts('bytes__endswith', [b'oo'], (self.foo, self.foo), self.foo)

    def test_prototype_iendswith(self):
        self.last_prototype_asserts(datatypes.bytes.iendswith(b'OO'), (self.foo, b'fOo'), b'fOo')

    def test_compound_iendswith(self):
        self.last_compound_asserts('bytes__iendswith', [b'OO'], (self.foo, b'fOo'), b'fOo')

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.bytes.len(3), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.last_compound_asserts('bytes__len', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.bytes.lenlt(4), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.last_compound_asserts('bytes__lenlt', [4], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.bytes.lenlte(3), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.last_compound_asserts('bytes__lenlte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.bytes.lengt(2), (self.foo, self.foo), self.foo)

    def test_compound_lengt(self):
        self.last_compound_asserts('bytes__lengt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.bytes.lengte(3), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.last_compound_asserts('bytes__lengte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_isalnum(self):
        self.last_prototype_asserts(datatypes.bytes.isalnum(), (self.foo, self.foo), self.foo)

    def test_compound_isalnum(self):
        self.last_compound_asserts('bytes__isalnum', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalnums(self):
        self.last_prototype_asserts(datatypes.bytes.isalnums(), (b'fo o', b'f Oo'), b'f Oo')

    def test_compound_isalnums(self):
        self.last_compound_asserts('bytes__isalnums', [], (b'fo o', b'f Oo'), b'f Oo')

    def test_prototype_isalpha(self):
        self.last_prototype_asserts(datatypes.bytes.isalpha(), (self.foo, self.foo), self.foo)

    def test_compound_isalpha(self):
        self.last_compound_asserts('bytes__isalpha', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalphas(self):
        self.last_prototype_asserts(datatypes.bytes.isalphas(), (b'fo o', b'f Oo'), b'f Oo')

    def test_compound_isalphas(self):
        self.last_compound_asserts('bytes__isalphas', [], (b'fo o', b'f Oo'), b'f Oo')

    def test_prototype_isdigit(self):
        self.last_prototype_asserts(datatypes.bytes.isdigit(), (b'1', b'1'), b'1')

    def test_compound_isdigit(self):
        self.last_compound_asserts('bytes__isdigit', [], (b'1', b'1'), b'1')

    def test_prototype_islower(self):
        self.last_prototype_asserts(datatypes.bytes.islower(), (self.foo, self.foo), self.foo)

    def test_compound_islower(self):
        self.last_compound_asserts('bytes__islower', [], (self.foo, self.foo), self.foo)

    def test_prototype_isupper(self):
        self.last_prototype_asserts(datatypes.bytes.isupper(), (b'FOO', b'FOO'), b'FOO')

    def test_compound_isupper(self):
        self.last_compound_asserts('bytes__isupper', [], (b'FOO', b'FOO'), b'FOO')

    def test_prototype_isspace(self):
        self.last_prototype_asserts(datatypes.bytes.isspace(), (b'    ', b'    '), b'    ')

    def test_compound_isspace(self):
        self.last_compound_asserts('bytes__isspace', [], (b'    ', b'    '), b'    ')

    def test_prototype_istitle(self):
        self.last_prototype_asserts(datatypes.bytes.istitle(), (b'Foo', b'Foo'), b'Foo')

    def test_compound_istitle(self):
        self.last_compound_asserts('bytes__istitle', [], (b'Foo', b'Foo'), b'Foo')


class LastCommandBytearrayDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = bytearray(b'foo')

    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.bytearray.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.last_compound_asserts('bytearray__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_iexact(self):
        foo = bytearray(b'fOo')
        self.last_prototype_asserts(datatypes.bytearray.iexact(bytearray(b'FOO')), (self.foo, foo,), foo)

    def test_compound_iexact(self):
        foo = bytearray(b'fOo')
        self.last_compound_asserts('bytearray__iexact', [bytearray(b'FOO')], (self.foo, foo,), foo)

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.bytearray.contains(bytearray(b'o')), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.last_compound_asserts('bytearray__contains', [bytearray(b'o')], (self.foo, self.foo), self.foo)

    def test_prototype_icontains(self):
        foo = bytearray(b'fOo')
        self.last_prototype_asserts(datatypes.bytearray.icontains(bytearray(b'O')), (self.foo, foo), foo)

    def test_compound_icontains(self):
        foo = bytearray(b'fOo')
        self.last_compound_asserts('bytearray__icontains', [bytearray(b'O')], (self.foo, foo), foo)

    def test_prototype_startswith(self):
        self.last_prototype_asserts(datatypes.bytearray.startswith(bytearray(b'f')), (self.foo, self.foo), self.foo)

    def test_compound_startswith(self):
        self.last_compound_asserts('bytearray__startswith', [bytearray(b'f')], (self.foo, self.foo), self.foo)

    def test_prototype_istartswith(self):
        foo = bytearray(b'fOo')
        self.last_prototype_asserts(datatypes.bytearray.istartswith(bytearray(b'F')), (self.foo, foo), foo)

    def test_compound_istartswith(self):
        foo = bytearray(b'fOo')
        self.last_compound_asserts('bytearray__istartswith', [bytearray(b'F')], (self.foo, foo), foo)

    def test_prototype_endswith(self):
        self.last_prototype_asserts(datatypes.bytearray.endswith(bytearray(b'oo')), (self.foo, self.foo), self.foo)

    def test_compound_endswith(self):
        self.last_compound_asserts('bytearray__endswith', [bytearray(b'oo')], (self.foo, self.foo), self.foo)

    def test_prototype_iendswith(self):
        foo = bytearray(b'fOo')
        self.last_prototype_asserts(datatypes.bytearray.iendswith(bytearray(b'OO')), (self.foo, foo), foo)

    def test_compound_iendswith(self):
        foo = bytearray(b'fOo')
        self.last_compound_asserts('bytearray__iendswith', [bytearray(b'OO')], (self.foo, foo), foo)

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.bytearray.len(3), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.last_compound_asserts('bytearray__len', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.bytearray.lenlt(4), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.last_compound_asserts('bytearray__lenlt', [4], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.bytearray.lenlte(3), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.last_compound_asserts('bytearray__lenlte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.bytearray.lengt(2), (self.foo, self.foo), self.foo)

    def test_compound_lengt(self):
        self.last_compound_asserts('bytearray__lengt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.bytearray.lengte(3), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.last_compound_asserts('bytearray__lengte', [3], (self.foo, self.foo), self.foo)

    def test_prototype_isalnum(self):
        self.last_prototype_asserts(datatypes.bytearray.isalnum(), (self.foo, self.foo), self.foo)

    def test_compound_isalnum(self):
        self.last_compound_asserts('bytearray__isalnum', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalnums(self):
        foo = bytearray(b'f Oo')
        self.last_prototype_asserts(datatypes.bytearray.isalnums(), (bytearray(b'fo o'), foo), foo)

    def test_compound_isalnums(self):
        foo = bytearray(b'f Oo')
        self.last_compound_asserts('bytearray__isalnums', [], (bytearray(b'fo o'), foo), foo)

    def test_prototype_isalpha(self):
        self.last_prototype_asserts(datatypes.bytearray.isalpha(), (self.foo, self.foo), self.foo)

    def test_compound_isalpha(self):
        self.last_compound_asserts('bytearray__isalpha', [], (self.foo, self.foo), self.foo)

    def test_prototype_isalphas(self):
        foo = bytearray(b'f Oo')
        self.last_prototype_asserts(datatypes.bytearray.isalphas(), (bytearray(b'fo o'), foo), foo)

    def test_compound_isalphas(self):
        foo = bytearray(b'f Oo')
        self.last_compound_asserts('bytearray__isalphas', [], (bytearray(b'fo o'), foo), foo)

    def test_prototype_isdigit(self):
        one = bytearray(b'1')
        self.last_prototype_asserts(datatypes.bytearray.isdigit(), (one, one), one)

    def test_compound_isdigit(self):
        one = bytearray(b'1')
        self.last_compound_asserts('bytearray__isdigit', [], (one, one), one)

    def test_prototype_islower(self):
        self.last_prototype_asserts(datatypes.bytearray.islower(), (self.foo, self.foo), self.foo)

    def test_compound_islower(self):
        self.last_compound_asserts('bytearray__islower', [], (self.foo, self.foo), self.foo)

    def test_prototype_isupper(self):
        upper = bytearray(b'FOO')
        self.last_prototype_asserts(datatypes.bytearray.isupper(), (upper, upper), upper)

    def test_compound_isupper(self):
        upper = bytearray(b'FOO')
        self.last_compound_asserts('bytearray__isupper', [], (upper, upper), upper)

    def test_prototype_isspace(self):
        space = bytearray(b'    ')
        self.last_prototype_asserts(datatypes.bytearray.isspace(), (space, space), space)

    def test_compound_isspace(self):
        space = bytearray(b'    ')
        self.last_compound_asserts('bytearray__isspace', [], (space, space), space)

    def test_prototype_istitle(self):
        foo = bytearray(b'Foo')
        self.last_prototype_asserts(datatypes.bytearray.istitle(), (foo, foo), foo)

    def test_compound_istitle(self):
        foo = bytearray(b'Foo')
        self.last_compound_asserts('bytearray__istitle', [], (foo, foo), foo)


class LastCommandNumericDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.numeric.exact(5.5), (5.5, 5.5), 5.5)

    def test_compound_exact(self):
        self.last_compound_asserts('numeric__exact', [5.5], (5.5, 5.5), 5.5)

    def test_prototype_gt(self):
        self.last_prototype_asserts(datatypes.numeric.gt(3), (4, 4), 4)

    def test_compound_gt(self):
        self.last_compound_asserts('numeric__gt', [3], (4, 4), 4)

    def test_prototype_gte(self):
        self.last_prototype_asserts(datatypes.numeric.gte(5), (5, 5), 5)

    def test_compound_gte(self):
        self.last_compound_asserts('numeric__gte', [5], (5, 5), 5)

    def test_prototype_lt(self):
        self.last_prototype_asserts(datatypes.numeric.lt(2), (1, 1), 1)

    def test_compound_lt(self):
        self.last_compound_asserts('numeric__lt', [2], (1, 1), 1)

    def test_prototype_lte(self):
        self.last_prototype_asserts(datatypes.numeric.lte(2), (2, 2), 2)

    def test_compound_lte(self):
        self.last_compound_asserts('numeric__lte', [2], (2, 2), 2)

    def test_prototype_between(self):
        self.last_prototype_asserts(datatypes.numeric.between(1, 2), (1, 1), 1)

    def test_compound_between(self):
        self.last_compound_asserts('numeric__between', [1, 2], (1, 1), 1)

    def test_prototype_ebetween(self):
        self.last_prototype_asserts(datatypes.numeric.ebetween(0, 2), (1, 1), 1)

    def test_compound_ebetween(self):
        self.last_compound_asserts('numeric__ebetween', [0, 2], (1, 1), 1)

    def test_prototype_isodd(self):
        self.last_prototype_asserts(datatypes.numeric.isodd(), (5, 5), 5)

    def test_compound_isodd(self):
        self.last_compound_asserts('numeric__isodd', [], (5, 5), 5)

    def test_prototype_iseven(self):
        self.last_prototype_asserts(datatypes.numeric.iseven(), (4, 4), 4)

    def test_compound_iseven(self):
        self.last_compound_asserts('numeric__iseven', [], (4, 4), 4)

    def test_prototype_divisibleby(self):
        self.last_prototype_asserts(datatypes.numeric.divisibleby(2), (4, 4), 4)

    def test_compound_divisibleby(self):
        self.last_compound_asserts('numeric__divisibleby', [2], (4, 4), 4)


class LastCommandIntDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.int.exact(5), (5, 5), 5)

    def test_compound_exact(self):
        self.last_compound_asserts('int__exact', [5], (5, 5), 5)

    def test_prototype_gt(self):
        self.last_prototype_asserts(datatypes.int.gt(3), (4, 4), 4)

    def test_compound_gt(self):
        self.last_compound_asserts('int__gt', [3], (4, 4), 4)

    def test_prototype_gte(self):
        self.last_prototype_asserts(datatypes.int.gte(5), (5, 5), 5)

    def test_compound_gte(self):
        self.last_compound_asserts('int__gte', [5], (5, 5), 5)

    def test_prototype_lt(self):
        self.last_prototype_asserts(datatypes.int.lt(2), (1, 1), 1)

    def test_compound_lt(self):
        self.last_compound_asserts('int__lt', [2], (1, 1), 1)

    def test_prototype_lte(self):
        self.last_prototype_asserts(datatypes.int.lte(2), (2, 2), 2)

    def test_compound_lte(self):
        self.last_compound_asserts('int__lte', [2], (2, 2), 2)

    def test_prototype_between(self):
        self.last_prototype_asserts(datatypes.int.between(1, 2), (1, 1), 1)

    def test_compound_between(self):
        self.last_compound_asserts('int__between', [1, 2], (1, 1), 1)

    def test_prototype_ebetween(self):
        self.last_prototype_asserts(datatypes.int.ebetween(0, 2), (1, 1), 1)

    def test_compound_ebetween(self):
        self.last_compound_asserts('int__ebetween', [0, 2], (1, 1), 1)

    def test_prototype_isodd(self):
        self.last_prototype_asserts(datatypes.int.isodd(), (5, 5), 5)

    def test_compound_isodd(self):
        self.last_compound_asserts('int__isodd', [], (5, 5), 5)

    def test_prototype_iseven(self):
        self.last_prototype_asserts(datatypes.int.iseven(), (4, 4), 4)

    def test_compound_iseven(self):
        self.last_compound_asserts('int__iseven', [], (4, 4), 4)

    def test_prototype_divisibleby(self):
        self.last_prototype_asserts(datatypes.int.divisibleby(2), (4, 4), 4)

    def test_compound_divisibleby(self):
        self.last_compound_asserts('int__divisibleby', [2], (4, 4), 4)


class LastCommandFloatDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.float.exact(5.5), (5.5, 5.5), 5.5)

    def test_compound_exact(self):
        self.last_compound_asserts('float__exact', [5.5], (5.5, 5.5), 5.5)

    def test_prototype_gt(self):
        self.last_prototype_asserts(datatypes.float.gt(3), (4.2, 4.2), 4.2)

    def test_compound_gt(self):
        self.last_compound_asserts('float__gt', [3], (4.2, 4.2), 4.2)

    def test_prototype_gte(self):
        self.last_prototype_asserts(datatypes.float.gte(5), (5.5, 5.5), 5.5)

    def test_compound_gte(self):
        self.last_compound_asserts('float__gte', [5], (5.5, 5.5), 5.5)

    def test_prototype_lt(self):
        self.last_prototype_asserts(datatypes.float.lt(2), (1.1, 1.1), 1.1)

    def test_compound_lt(self):
        self.last_compound_asserts('float__lt', [2], (1.1, 1.1), 1.1)

    def test_prototype_lte(self):
        self.last_prototype_asserts(datatypes.float.lte(2), (1.8, 1.8), 1.8)

    def test_compound_lte(self):
        self.last_compound_asserts('float__lte', [2], (1.8, 1.8), 1.8)

    def test_prototype_between(self):
        self.last_prototype_asserts(datatypes.float.between(1, 2), (1.4, 1.4), 1.4)

    def test_compound_between(self):
        self.last_compound_asserts('float__between', [1, 2], (1.4, 1.4), 1.4)

    def test_prototype_ebetween(self):
        self.last_prototype_asserts(datatypes.float.ebetween(0, 2), (1.5, 1.5), 1.5)

    def test_compound_ebetween(self):
        self.last_compound_asserts('float__ebetween', [0, 2], (1.5, 1.5), 1.5)

    def test_prototype_isinteger(self):
        self.last_prototype_asserts(datatypes.float.isinteger(), (5.0, 5.0), 5.0)

    def test_compound_isinteger(self):
        self.last_compound_asserts('float__isinteger', [], (5.0, 5.0), 5.0)

    def test_prototype_isodd(self):
        self.last_prototype_asserts(datatypes.float.isodd(), (5.2, 5.2), 5.2)

    def test_compound_isodd(self):
        self.last_compound_asserts('float__isodd', [], (5.2, 5.2), 5.2)

    def test_prototype_iseven(self):
        self.last_prototype_asserts(datatypes.float.iseven(), (4.3, 4.3), 4.3)

    def test_compound_iseven(self):
        self.last_compound_asserts('float__iseven', [], (4.3, 4.3), 4.3)

    def test_prototype_divisibleby(self):
        self.last_prototype_asserts(datatypes.float.divisibleby(2), (4.7, 4.7), 4.7)

    def test_compound_divisibleby(self):
        self.last_compound_asserts('float__divisibleby', [2], (4.7, 4.7), 4.7)


class LastCommandLongDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.long.exact(2 ** 64), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_exact(self):
        self.last_compound_asserts('long__exact', [2 ** 64], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_gt(self):
        self.last_prototype_asserts(datatypes.long.gt(2 ** 63), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_gt(self):
        self.last_compound_asserts('long__gt', [2 ** 63], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_gte(self):
        self.last_prototype_asserts(datatypes.long.gte(2 ** 64), (2 ** 65, 2 ** 65), 2 ** 65)

    def test_compound_gte(self):
        self.last_compound_asserts('long__gte', [2 ** 64], (2 ** 65, 2 ** 65), 2 ** 65)

    def test_prototype_lt(self):
        self.last_prototype_asserts(datatypes.long.lt(2 ** 64), (2 ** 63, 2 ** 63), 2 ** 63)

    def test_compound_lt(self):
        self.last_compound_asserts('long__lt', [2 ** 64], (2 ** 63, 2 ** 63), 2 ** 63)

    def test_prototype_lte(self):
        self.last_prototype_asserts(datatypes.long.lte(2 ** 64), (2 ** 63, 2 ** 63), 2 ** 63)

    def test_compound_lte(self):
        self.last_compound_asserts('long__lte', [2 ** 64], (2 ** 63, 2 ** 63), 2 ** 63)

    def test_prototype_between(self):
        self.last_prototype_asserts(datatypes.long.between(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_between(self):
        self.last_compound_asserts('long__between', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_ebetween(self):
        self.last_prototype_asserts(datatypes.long.ebetween(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_ebetween(self):
        self.last_compound_asserts('long__ebetween', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_isodd(self):
        self.last_prototype_asserts(datatypes.long.isodd(), (3 ** 64, 3 ** 64), 3 ** 64)

    def test_compound_isodd(self):
        self.last_compound_asserts('long__isodd', [], (3 ** 64, 3 ** 64), 3 ** 64)

    def test_prototype_iseven(self):
        self.last_prototype_asserts(datatypes.long.iseven(), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_iseven(self):
        self.last_compound_asserts('long__iseven', [], (2 ** 64, 2 ** 64), 2 ** 64)

    def test_prototype_divisibleby(self):
        self.last_prototype_asserts(datatypes.long.divisibleby(2), (2 ** 64, 2 ** 64), 2 ** 64)

    def test_compound_divisibleby(self):
        self.last_compound_asserts('long__divisibleby', [2], (2 ** 64, 2 ** 64), 2 ** 64)


class LastCommandComplexDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.complex.exact(1j), (1j, 1j), 1j)

    def test_compound_exact(self):
        self.last_compound_asserts('complex__exact', [1j], (1j, 1j), 1j)


class LastCommandIterableDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.iterable.exact(['foo']), (['foo'], ['foo']), ['foo'])

    def test_compound_exact(self):
        self.last_compound_asserts('iterable__exact', [['foo']], (['foo'], ['foo']), ['foo'])

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.iterable.len(1), (['foo'], ['foo']), ['foo'])

    def test_compound_len(self):
        self.last_compound_asserts('iterable__len', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.iterable.lenlt(2), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlt(self):
        self.last_compound_asserts('iterable__lenlt', [2], (['foo'], ['foo']), ['foo'])

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.iterable.lenlte(1), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlte(self):
        self.last_compound_asserts('iterable__lenlte', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.iterable.lengt(0), (['foo'], ['foo']), ['foo'])

    def test_compound_lengt(self):
        self.last_compound_asserts('iterable__lengt', [0], (['foo'], ['foo']), ['foo'])

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.iterable.lengte(1), (['foo'], ['foo']), ['foo'])

    def test_compound_lengte(self):
        self.last_compound_asserts('iterable__lengte', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.iterable.contains('foo'), (['foo'], ('foo',)), ('foo',))

    def test_compound_contains(self):
        self.last_compound_asserts('iterable__contains', ['foo'], (['foo'], ('foo',)), ('foo',))

    def test_prototype_contains_all(self):
        self.last_prototype_asserts(datatypes.iterable.contains_all(['f', 'o']), (['f', 'o'], ('f', 'o')), ('f', 'o'))

    def test_compound_contains_all(self):
        self.last_compound_asserts('iterable__contains_all', [['f', 'o']], (['f', 'o'], ('f', 'o')), ('f', 'o'))

    def test_prototype_contains_any(self):
        self.last_prototype_asserts(datatypes.iterable.contains_any(['f', 'z']), (['f', 'o'], ('f', 'o')), ('f', 'o'))

    def test_compound_contains_any(self):
        self.last_compound_asserts('iterable__contains_any', [['f', 'z']], (['f', 'o'], ('f', 'o')), ('f', 'o'))

    def test_prototype_str_contains_str(self):
        self.last_prototype_asserts(datatypes.iterable.str_contains_str('f'), (['fo'], ('fo',)), ('fo',))

    def test_compound_str_contains_str(self):
        self.last_compound_asserts('iterable__str_contains_str', ['f'], (['fo'], ('fo',)), ('fo',))


class LastCommandListDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.list.exact(['foo']), (['foo'], ['foo']), ['foo'])

    def test_compound_exact(self):
        self.last_compound_asserts('list__exact', [['foo']], (['foo'], ['foo']), ['foo'])

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.list.len(1), (['foo'], ['foo']), ['foo'])

    def test_compound_len(self):
        self.last_compound_asserts('list__len', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.list.lenlt(2), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlt(self):
        self.last_compound_asserts('list__lenlt', [2], (['foo'], ['foo']), ['foo'])

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.list.lenlte(1), (['foo'], ['foo']), ['foo'])

    def test_compound_lenlte(self):
        self.last_compound_asserts('list__lenlte', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.list.lengt(0), (['foo'], ['foo']), ['foo'])

    def test_compound_lengt(self):
        self.last_compound_asserts('list__lengt', [0], (['foo'], ['foo']), ['foo'])

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.list.lengte(1), (['foo'], ['foo']), ['foo'])

    def test_compound_lengte(self):
        self.last_compound_asserts('list__lengte', [1], (['foo'], ['foo']), ['foo'])

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.list.contains('foo'), (['foo'], ['foo']), ['foo'])

    def test_compound_contains(self):
        self.last_compound_asserts('list__contains', ['foo'], (['foo'], ['foo']), ['foo'])

    def test_prototype_contains_all(self):
        self.last_prototype_asserts(datatypes.list.contains_all(['f', 'o']), (['f', 'o'], ['f', 'o']), ['f', 'o'])

    def test_compound_contains_all(self):
        self.last_compound_asserts('list__contains_all', [['f', 'o']], (['f', 'o'], ['f', 'o']), ['f', 'o'])

    def test_prototype_contains_any(self):
        self.last_prototype_asserts(datatypes.list.contains_any(['f', 'z']), (['f', 'o'], ['f', 'o']), ['f', 'o'])

    def test_compound_contains_any(self):
        self.last_compound_asserts('list__contains_any', [['f', 'z']], (['f', 'o'], ['f', 'o']), ['f', 'o'])

    def test_prototype_str_contains_str(self):
        self.last_prototype_asserts(datatypes.list.str_contains_str('f'), (['fo'], ['fo']), ['fo'])

    def test_compound_str_contains_str(self):
        self.last_compound_asserts('list__str_contains_str', ['f'], (['fo'], ['fo']), ['fo'])


class LastCommandTupleDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.tuple.exact(('foo',)), (('foo',), ('foo',)), ('foo',))

    def test_compound_exact(self):
        self.last_compound_asserts('tuple__exact', [('foo',)], (('foo',), ('foo',)), ('foo',))

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.tuple.len(1), (('foo',), ('foo',)), ('foo',))

    def test_compound_len(self):
        self.last_compound_asserts('tuple__len', [1], (('foo',), ('foo',)), ('foo',))

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.tuple.lenlt(2), (('foo',), ('foo',)), ('foo',))

    def test_compound_lenlt(self):
        self.last_compound_asserts('tuple__lenlt', [2], (('foo',), ('foo',)), ('foo',))

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.tuple.lenlte(1), (('foo',), ('foo',)), ('foo',))

    def test_compound_lenlte(self):
        self.last_compound_asserts('tuple__lenlte', [1], (('foo',), ('foo',)), ('foo',))

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.tuple.lengt(0), (('foo',), ('foo',)), ('foo',))

    def test_compound_lengt(self):
        self.last_compound_asserts('tuple__lengt', [0], (('foo',), ('foo',)), ('foo',))

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.tuple.lengte(1), (('foo',), ('foo',)), ('foo',))

    def test_compound_lengte(self):
        self.last_compound_asserts('tuple__lengte', [1], (('foo',), ('foo',)), ('foo',))

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.tuple.contains('foo'), (('foo',), ('foo',)), ('foo',))

    def test_compound_contains(self):
        self.last_compound_asserts('tuple__contains', ['foo'], (('foo',), ('foo',)), ('foo',))

    def test_prototype_contains_all(self):
        self.last_prototype_asserts(datatypes.tuple.contains_all(('f', 'o')), (('f', 'o'), ('f', 'o')), ('f', 'o'))

    def test_compound_contains_all(self):
        self.last_compound_asserts('tuple__contains_all', [('f', 'o')], (('f', 'o'), ('f', 'o')), ('f', 'o'))

    def test_prototype_contains_any(self):
        self.last_prototype_asserts(datatypes.tuple.contains_any(('f', 'z')), (('f', 'o'), ('f', 'o')), ('f', 'o'))

    def test_compound_contains_any(self):
        self.last_compound_asserts('tuple__contains_any', [('f', 'z')], (('f', 'o'), ('f', 'o')), ('f', 'o'))

    def test_prototype_str_contains_str(self):
        self.last_prototype_asserts(datatypes.tuple.str_contains_str('f'), (('fo',), ('fo',)), ('fo',))

    def test_compound_str_contains_str(self):
        self.last_compound_asserts('tuple__str_contains_str', ['f'], (('fo',), ('fo',)), ('fo',))


class LastCommandSetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = set(['foo'])

    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.set.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.last_compound_asserts('set__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.set.len(1), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.last_compound_asserts('set__len', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.set.lenlt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.last_compound_asserts('set__lenlt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.set.lenlte(1), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.last_compound_asserts('set__lenlte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.set.lengt(0), (self.foo, self.foo), self.foo)

    def test_compound_lengt(self):
        self.last_compound_asserts('set__lengt', [0], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.set.lengte(1), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.last_compound_asserts('set__lengte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.set.contains('foo'), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.last_compound_asserts('set__contains', ['foo'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_all(self):
        foo = set(['f', 'o'])
        self.last_prototype_asserts(datatypes.set.contains_all(['f', 'o']), (foo, foo), foo)

    def test_compound_contains_all(self):
        foo = set(['f', 'o'])
        self.last_compound_asserts('set__contains_all', [['f', 'o']], (foo, foo), foo)

    def test_prototype_contains_any(self):
        foo = set(['f', 'o'])
        self.last_prototype_asserts(datatypes.set.contains_any(['f', 'z']), (foo, foo), foo)

    def test_compound_contains_any(self):
        foo = set(['f', 'o'])
        self.last_compound_asserts('set__contains_any', [['f', 'z']], (foo, foo), foo)

    def test_prototype_str_contains_str(self):
        foo = set(['fo'])
        self.last_prototype_asserts(datatypes.set.str_contains_str('f'), (foo, foo), foo)

    def test_compound_str_contains_str(self):
        foo = set(['fo'])
        self.last_compound_asserts('set__str_contains_str', ['f'], (foo, foo), foo)

    def test_prototype_isdisjoint(self):
        self.last_prototype_asserts(datatypes.set.isdisjoint(set(['bar'])), (self.foo, self.foo), self.foo)

    def test_compound_isdisjoint(self):
        self.last_compound_asserts('set__isdisjoint', [set(['bar'])], (self.foo, self.foo), self.foo)

    def test_prototype_issubset(self):
        self.last_prototype_asserts(datatypes.set.issubset(set(['foo'])), (self.foo, self.foo), self.foo)

    def test_compound_issubset(self):
        self.last_compound_asserts('set__issubset', [set(['foo'])], (self.foo, self.foo), self.foo)

    def test_prototype_eissubset(self):
        self.last_prototype_asserts(datatypes.set.eissubset(set(['foo', 'bar'])), (self.foo, self.foo), self.foo)

    def test_compound_eissubset(self):
        self.last_compound_asserts('set__eissubset', [set(['foo', 'bar'])], (self.foo, self.foo), self.foo)

    def test_prototype_issuperset(self):
        self.last_prototype_asserts(datatypes.set.issuperset(set(['foo'])), (self.foo, self.foo), self.foo)

    def test_compound_issuperset(self):
        self.last_compound_asserts('set__issuperset', [set(['foo'])], (self.foo, self.foo), self.foo)

    def test_prototype_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.last_prototype_asserts(datatypes.set.eissuperset(set(['foo'])), (foo, foo), foo)

    def test_compound_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.last_compound_asserts('set__eissuperset', [set(['foo'])], (foo, foo), foo)


class LastCommandFrozensetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = frozenset(['foo'])

    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.frozenset.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.last_compound_asserts('frozenset__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.frozenset.len(1), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.last_compound_asserts('frozenset__len', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.frozenset.lenlt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.last_compound_asserts('frozenset__lenlt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.frozenset.lenlte(1), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.last_compound_asserts('frozenset__lenlte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.frozenset.lengt(0), (self.foo, self.foo), self.foo)

    def test_compound_lengt(self):
        self.last_compound_asserts('frozenset__lengt', [0], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.frozenset.lengte(1), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.last_compound_asserts('frozenset__lengte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_contains(self):
        self.last_prototype_asserts(datatypes.frozenset.contains('foo'), (self.foo, self.foo), self.foo)

    def test_compound_contains(self):
        self.last_compound_asserts('frozenset__contains', ['foo'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.last_prototype_asserts(datatypes.frozenset.contains_all(['f', 'o']), (foo, foo), foo)

    def test_compound_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.last_compound_asserts('frozenset__contains_all', [['f', 'o']], (foo, foo), foo)

    def test_prototype_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.last_prototype_asserts(datatypes.frozenset.contains_any(['f', 'z']), (foo, foo), foo)

    def test_compound_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.last_compound_asserts('frozenset__contains_any', [['f', 'z']], (foo, foo), foo)

    def test_prototype_str_contains_str(self):
        foo = frozenset(['fo'])
        self.last_prototype_asserts(datatypes.frozenset.str_contains_str('f'), (foo, foo), foo)

    def test_compound_str_contains_str(self):
        foo = frozenset(['fo'])
        self.last_compound_asserts('frozenset__str_contains_str', ['f'], (foo, foo), foo)

    def test_prototype_isdisjoint(self):
        self.last_prototype_asserts(datatypes.frozenset.isdisjoint(frozenset(['bar'])), (self.foo, self.foo), self.foo)

    def test_compound_isdisjoint(self):
        self.last_compound_asserts('frozenset__isdisjoint', [frozenset(['bar'])], (self.foo, self.foo), self.foo)

    def test_prototype_issubset(self):
        self.last_prototype_asserts(datatypes.frozenset.issubset(frozenset(['foo'])), (self.foo, self.foo), self.foo)

    def test_compound_issubset(self):
        self.last_compound_asserts('frozenset__issubset', [frozenset(['foo'])], (self.foo, self.foo), self.foo)

    def test_prototype_eissubset(self):
        foo = frozenset(['foo', 'bar'])
        self.last_prototype_asserts(datatypes.frozenset.eissubset(foo), (self.foo, self.foo), self.foo)

    def test_compound_eissubset(self):
        self.last_compound_asserts('frozenset__eissubset', [frozenset(['foo', 'bar'])], (self.foo, self.foo), self.foo)

    def test_prototype_issuperset(self):
        self.last_prototype_asserts(datatypes.frozenset.issuperset(frozenset(['foo'])), (self.foo, self.foo), self.foo)

    def test_compound_issuperset(self):
        self.last_compound_asserts('frozenset__issuperset', [frozenset(['foo'])], (self.foo, self.foo), self.foo)

    def test_prototype_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.last_prototype_asserts(datatypes.frozenset.eissuperset(frozenset(['foo'])), (foo, foo), foo)

    def test_compound_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.last_compound_asserts('frozenset__eissuperset', [frozenset(['foo'])], (foo, foo), foo)


class LastCommandDictDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = {'foo': 'bar'}

    def test_prototype_exact(self):
        self.last_prototype_asserts(datatypes.dict.exact(self.foo), (self.foo, self.foo), self.foo)

    def test_compound_exact(self):
        self.last_compound_asserts('dict__exact', [self.foo], (self.foo, self.foo), self.foo)

    def test_prototype_len(self):
        self.last_prototype_asserts(datatypes.dict.len(1), (self.foo, self.foo), self.foo)

    def test_compound_len(self):
        self.last_compound_asserts('dict__len', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lenlt(self):
        self.last_prototype_asserts(datatypes.dict.lenlt(2), (self.foo, self.foo), self.foo)

    def test_compound_lenlt(self):
        self.last_compound_asserts('dict__lenlt', [2], (self.foo, self.foo), self.foo)

    def test_prototype_lenlte(self):
        self.last_prototype_asserts(datatypes.dict.lenlte(1), (self.foo, self.foo), self.foo)

    def test_compound_lenlte(self):
        self.last_compound_asserts('dict__lenlte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_lengt(self):
        self.last_prototype_asserts(datatypes.dict.lengt(0), (self.foo, self.foo), self.foo)

    def test_compound_lengt(self):
        self.last_compound_asserts('dict__lengt', [0], (self.foo, self.foo), self.foo)

    def test_prototype_lengte(self):
        self.last_prototype_asserts(datatypes.dict.lengte(1), (self.foo, self.foo), self.foo)

    def test_compound_lengte(self):
        self.last_compound_asserts('dict__lengte', [1], (self.foo, self.foo), self.foo)

    def test_prototype_contains_key(self):
        self.last_prototype_asserts(datatypes.dict.contains_key('foo'), (self.foo, self.foo), self.foo)

    def test_compound_contains_key(self):
        self.last_compound_asserts('dict__contains_key', ['foo'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.last_prototype_asserts(datatypes.dict.contains_all_keys(['foo', 'bar']), (foo, foo), foo)

    def test_compound_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.last_compound_asserts('dict__contains_all_keys', [['foo', 'bar']], (foo, foo), foo)

    def test_prototype_contains_any_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.last_prototype_asserts(datatypes.dict.contains_any_keys(['foo', 'z']), (foo, foo), foo)

    def test_compound_contains_any_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.last_compound_asserts('dict__contains_any_keys', [['foo', 'z']], (foo, foo), foo)

    def test_prototype_key_contains_str(self):
        self.last_prototype_asserts(datatypes.dict.key_contains_str('f'), (self.foo, self.foo), self.foo)

    def test_compound_key_contains_str(self):
        self.last_compound_asserts('dict__key_contains_str', ['f'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_value(self):
        self.last_prototype_asserts(datatypes.dict.contains_value('bar'), (self.foo, self.foo), self.foo)

    def test_compound_contains_value(self):
        self.last_compound_asserts('dict__contains_value', ['bar'], (self.foo, self.foo), self.foo)

    def test_prototype_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.last_prototype_asserts(datatypes.dict.contains_all_values(['bar', 'baz']), (foo, foo), foo)

    def test_compound_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.last_compound_asserts('dict__contains_all_values', [['bar', 'baz']], (foo, foo), foo)

    def test_prototype_contains_any_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.last_prototype_asserts(datatypes.dict.contains_any_values(['bar', 'z']), (foo, foo), foo)

    def test_compound_contains_any_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.last_compound_asserts('dict__contains_any_values', [['bar', 'z']], (foo, foo), foo)

    def test_prototype_value_contains_str(self):
        self.last_prototype_asserts(datatypes.dict.value_contains_str('b'), (self.foo, self.foo), self.foo)

    def test_compound_value_contains_str(self):
        self.last_compound_asserts('dict__value_contains_str', ['b'], (self.foo, self.foo), self.foo)


class ExistsCommandTestCase(unittest.TestCase):
    def test_prototype(self):
        self.assertIsInstance(commands.exists(datatypes.bool), commands.Command)


class ExistsCommandBoolDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.bool.exact(True), (True, True), True)
        self.exists_prototype_asserts(datatypes.bool.exact(False), (True, True), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('bool__exact', [True], (True, True), True)
        self.exists_compound_asserts('bool__exact', [False], (True, True), False)

    def test_prototype_true(self):
        self.exists_prototype_asserts(datatypes.bool.true, (True, True), True)
        self.exists_prototype_asserts(datatypes.bool.true, (False, False), False)

    def test_compound_true(self):
        self.exists_compound_asserts('bool__true', [], (True, True), True)
        self.exists_compound_asserts('bool__true', [], (False, False), False)

    def test_prototype_false(self):
        self.exists_prototype_asserts(datatypes.bool.false, (False, False), True)
        self.exists_prototype_asserts(datatypes.bool.false, (True, True), False)

    def test_compound_false(self):
        self.exists_compound_asserts('bool__false', [], (False, False), True)
        self.exists_compound_asserts('bool__false', [], (True, True), False)


class ExistsCommandStringDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = 'foo'

    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.string.exact(self.foo), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.exact('bar'), (self.foo, self.foo), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('string__exact', [self.foo], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__exact', ['bar'], (self.foo, self.foo), False)

    def test_prototype_iexact(self):
        self.exists_prototype_asserts(datatypes.string.iexact('FOO'), (self.foo, 'fOo',), True)
        self.exists_prototype_asserts(datatypes.string.iexact('BAR'), (self.foo, 'fOo',), False)

    def test_compound_iexact(self):
        self.exists_compound_asserts('string__iexact', ['FOO'], (self.foo, 'fOo',), True)
        self.exists_compound_asserts('string__iexact', ['BAR'], (self.foo, 'fOo',), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.string.contains('o'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.contains('b'), (self.foo, self.foo), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('string__contains', ['o'], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__contains', ['b'], (self.foo, self.foo), False)

    def test_prototype_icontains(self):
        self.exists_prototype_asserts(datatypes.string.icontains('O'), (self.foo, 'fOo'), True)
        self.exists_prototype_asserts(datatypes.string.icontains('B'), (self.foo, 'fOo'), False)

    def test_compound_icontains(self):
        self.exists_compound_asserts('string__icontains', ['O'], (self.foo, 'fOo'), True)
        self.exists_compound_asserts('string__icontains', ['B'], (self.foo, 'fOo'), False)

    def test_prototype_startswith(self):
        self.exists_prototype_asserts(datatypes.string.startswith('f'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.startswith('b'), (self.foo, self.foo), False)

    def test_compound_startswith(self):
        self.exists_compound_asserts('string__startswith', ['f'], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__startswith', ['b'], (self.foo, self.foo), False)

    def test_prototype_istartswith(self):
        self.exists_prototype_asserts(datatypes.string.istartswith('F'), (self.foo, 'fOo'), True)
        self.exists_prototype_asserts(datatypes.string.istartswith('B'), (self.foo, 'fOo'), False)

    def test_compound_istartswith(self):
        self.exists_compound_asserts('string__istartswith', ['F'], (self.foo, 'fOo'), True)
        self.exists_compound_asserts('string__istartswith', ['B'], (self.foo, 'fOo'), False)

    def test_prototype_endswith(self):
        self.exists_prototype_asserts(datatypes.string.endswith('oo'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.endswith('ar'), (self.foo, self.foo), False)

    def test_compound_endswith(self):
        self.exists_compound_asserts('string__endswith', ['oo'], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__endswith', ['ar'], (self.foo, self.foo), False)

    def test_prototype_iendswith(self):
        self.exists_prototype_asserts(datatypes.string.iendswith('OO'), (self.foo, 'fOo'), True)
        self.exists_prototype_asserts(datatypes.string.iendswith('AR'), (self.foo, 'fOo'), False)

    def test_compound_iendswith(self):
        self.exists_compound_asserts('string__iendswith', ['OO'], (self.foo, 'fOo'), True)
        self.exists_compound_asserts('string__iendswith', ['AR'], (self.foo, 'fOo'), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.string.len(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.len(4), (self.foo, self.foo), False)

    def test_compound_len(self):
        self.exists_compound_asserts('string__len', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__len', [4], (self.foo, self.foo), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.string.lenlt(4), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.lenlt(3), (self.foo, self.foo), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('string__lenlt', [4], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__lenlt', [3], (self.foo, self.foo), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.string.lenlte(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.lenlte(2), (self.foo, self.foo), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('string__lenlte', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__lenlte', [2], (self.foo, self.foo), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.string.lengt(2), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.lengt(3), (self.foo, self.foo), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('string__lengt', [2], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__lengt', [3], (self.foo, self.foo), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.string.lengte(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.lengte(4), (self.foo, self.foo), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('string__lengte', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__lengte', [4], (self.foo, self.foo), False)

    def test_prototype_isalnum(self):
        self.exists_prototype_asserts(datatypes.string.isalnum(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.isalnum(), (123, 456), False)

    def test_compound_isalnum(self):
        self.exists_compound_asserts('string__isalnum', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__isalnum', [], (123, 456), False)

    def test_prototype_isalnums(self):
        self.exists_prototype_asserts(datatypes.string.isalnums(), ('fo o', 'f Oo'), True)
        self.exists_prototype_asserts(datatypes.string.isalnum(), (123, 456), False)

    def test_compound_isalnums(self):
        self.exists_compound_asserts('string__isalnums', [], ('fo o', 'f Oo'), True)
        self.exists_compound_asserts('string__isalnums', [], (123, 456), False)

    def test_prototype_isalpha(self):
        self.exists_prototype_asserts(datatypes.string.isalpha(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.isalpha(), (' ', ' '), False)

    def test_compound_isalpha(self):
        self.exists_compound_asserts('string__isalpha', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__isalpha', [], (' ', ' '), False)

    def test_prototype_isalphas(self):
        self.exists_prototype_asserts(datatypes.string.isalphas(), ('fo o', 'f Oo'), True)
        self.exists_prototype_asserts(datatypes.string.isalphas(), ('--', '--'), False)

    def test_compound_isalphas(self):
        self.exists_compound_asserts('string__isalphas', [], ('fo o', 'f Oo'), True)
        self.exists_compound_asserts('string__isalphas', [], ('--', '--'), False)

    def test_prototype_isdigit(self):
        self.exists_prototype_asserts(datatypes.string.isdigit(), ('1', '1'), True)
        self.exists_prototype_asserts(datatypes.string.isdigit(), (self.foo, self.foo), False)

    def test_compound_isdigit(self):
        self.exists_compound_asserts('string__isdigit', [], ('1', '1'), True)
        self.exists_compound_asserts('string__isdigit', [], (self.foo, self.foo), False)

    def test_prototype_islower(self):
        self.exists_prototype_asserts(datatypes.string.islower(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.string.islower(), ('FOO', 'FOO'), False)

    def test_compound_islower(self):
        self.exists_compound_asserts('string__islower', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('string__islower', [], ('FOO', 'FOO'), False)

    def test_prototype_isupper(self):
        self.exists_prototype_asserts(datatypes.string.isupper(), ('FOO', 'FOO'), True)
        self.exists_prototype_asserts(datatypes.string.isupper(), (self.foo, self.foo), False)

    def test_compound_isupper(self):
        self.exists_compound_asserts('string__isupper', [], ('FOO', 'FOO'), True)
        self.exists_compound_asserts('string__isupper', [], (self.foo, self.foo), False)

    def test_prototype_isspace(self):
        self.exists_prototype_asserts(datatypes.string.isspace(), ('    ', '    '), True)
        self.exists_prototype_asserts(datatypes.string.isspace(), (self.foo, 'bar'), False)

    def test_compound_isspace(self):
        self.exists_compound_asserts('string__isspace', [], ('    ', '    '), True)
        self.exists_compound_asserts('string__isspace', [], (self.foo, 'bar'), False)

    def test_prototype_istitle(self):
        self.exists_prototype_asserts(datatypes.string.istitle(), ('Foo', 'Foo'), True)
        self.exists_prototype_asserts(datatypes.string.istitle(), (self.foo, self.foo), False)

    def test_compound_istitle(self):
        self.exists_compound_asserts('string__istitle', [], ('Foo', 'Foo'), True)
        self.exists_compound_asserts('string__istitle', [], (self.foo, self.foo), False)


class ExistsCommandUnicodeDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'.decode()

    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.unicode.exact(self.foo), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.exact(b'bar'.decode()), (self.foo, self.foo), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('unicode__exact', [self.foo], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__exact', [b'bar'.decode()], (self.foo, self.foo), False)

    def test_prototype_iexact(self):
        self.exists_prototype_asserts(datatypes.unicode.iexact(b'FOO'.decode()), (self.foo, b'fOo'.decode(),), True)
        self.exists_prototype_asserts(datatypes.unicode.iexact(b'BAR'.decode()), (self.foo, b'fOo'.decode(),), False)

    def test_compound_iexact(self):
        self.exists_compound_asserts('unicode__iexact', [b'FOO'.decode()], (self.foo, b'fOo'.decode(),), True)
        self.exists_compound_asserts('unicode__iexact', [b'BAR'.decode()], (self.foo, b'fOo'.decode(),), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.unicode.contains(b'o'.decode()), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.contains(b'b'.decode()), (self.foo, self.foo), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('unicode__contains', [b'o'.decode()], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__contains', [b'b'.decode()], (self.foo, self.foo), False)

    def test_prototype_icontains(self):
        self.exists_prototype_asserts(datatypes.unicode.icontains(b'O'.decode()), (self.foo, b'fOo'.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.icontains(b'B'.decode()), (self.foo, b'fOo'.decode()), False)

    def test_compound_icontains(self):
        self.exists_compound_asserts('unicode__icontains', [b'O'.decode()], (self.foo, b'fOo'.decode()), True)
        self.exists_compound_asserts('unicode__icontains', [b'B'.decode()], (self.foo, b'fOo'.decode()), False)

    def test_prototype_startswith(self):
        self.exists_prototype_asserts(datatypes.unicode.startswith(b'f'.decode()), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.startswith(b'b'.decode()), (self.foo, self.foo), False)

    def test_compound_startswith(self):
        self.exists_compound_asserts('unicode__startswith', [b'f'.decode()], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__startswith', [b'b'.decode()], (self.foo, self.foo), False)

    def test_prototype_istartswith(self):
        self.exists_prototype_asserts(datatypes.unicode.istartswith(b'F'.decode()), (self.foo, b'fOo'.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.istartswith(b'B'.decode()), (self.foo, b'fOo'.decode()), False)

    def test_compound_istartswith(self):
        self.exists_compound_asserts('unicode__istartswith', [b'F'.decode()], (self.foo, b'fOo'.decode()), True)
        self.exists_compound_asserts('unicode__istartswith', [b'B'.decode()], (self.foo, b'fOo'.decode()), False)

    def test_prototype_endswith(self):
        self.exists_prototype_asserts(datatypes.unicode.endswith(b'oo'.decode()), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.endswith(b'ar'.decode()), (self.foo, self.foo), False)

    def test_compound_endswith(self):
        self.exists_compound_asserts('unicode__endswith', [b'oo'.decode()], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__endswith', [b'ar'.decode()], (self.foo, self.foo), False)

    def test_prototype_iendswith(self):
        self.exists_prototype_asserts(datatypes.unicode.iendswith(b'OO'.decode()), (self.foo, b'fOo'.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.iendswith(b'AR'.decode()), (self.foo, b'fOo'.decode()), False)

    def test_compound_iendswith(self):
        self.exists_compound_asserts('unicode__iendswith', [b'OO'.decode()], (self.foo, b'fOo'.decode()), True)
        self.exists_compound_asserts('unicode__iendswith', [b'AR'.decode()], (self.foo, b'fOo'.decode()), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.unicode.len(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.len(4), (self.foo, self.foo), False)

    def test_compound_len(self):
        self.exists_compound_asserts('unicode__len', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__len', [4], (self.foo, self.foo), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.unicode.lenlt(4), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.lenlt(3), (self.foo, self.foo), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('unicode__lenlt', [4], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__lenlt', [3], (self.foo, self.foo), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.unicode.lenlte(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.lenlte(2), (self.foo, self.foo), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('unicode__lenlte', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__lenlte', [2], (self.foo, self.foo), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.unicode.lengt(2), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.lengt(3), (self.foo, self.foo), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('unicode__lengt', [2], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__lengt', [3], (self.foo, self.foo), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.unicode.lengte(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.lengte(4), (self.foo, self.foo), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('unicode__lengte', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__lengte', [4], (self.foo, self.foo), False)

    def test_prototype_isalnum(self):
        self.exists_prototype_asserts(datatypes.unicode.isalnum(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.isalnum(), (123, 456), False)

    def test_compound_isalnum(self):
        self.exists_compound_asserts('unicode__isalnum', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__isalnum', [], (123, 456), False)

    def test_prototype_isalnums(self):
        self.exists_prototype_asserts(datatypes.unicode.isalnums(), (b'fo o'.decode(), b'f Oo'.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.isalnum(), (123, 456), False)

    def test_compound_isalnums(self):
        self.exists_compound_asserts('unicode__isalnums', [], (b'fo o'.decode(), b'f Oo'.decode()), True)
        self.exists_compound_asserts('unicode__isalnums', [], (123, 456), False)

    def test_prototype_isalpha(self):
        self.exists_prototype_asserts(datatypes.unicode.isalpha(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.isalpha(), (b' '.decode(), b' '.decode()), False)

    def test_compound_isalpha(self):
        self.exists_compound_asserts('unicode__isalpha', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__isalpha', [], (b' '.decode(), b' '.decode()), False)

    def test_prototype_isalphas(self):
        self.exists_prototype_asserts(datatypes.unicode.isalphas(), (b'fo o'.decode(), b'f Oo'.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.isalphas(), (b'--'.decode(), b'--'.decode()), False)

    def test_compound_isalphas(self):
        self.exists_compound_asserts('unicode__isalphas', [], (b'fo o'.decode(), b'f Oo'.decode()), True)
        self.exists_compound_asserts('unicode__isalphas', [], (b'--'.decode(), b'--'.decode()), False)

    def test_prototype_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.exists_prototype_asserts(datatypes.unicode.isdecimal(), (decimal, decimal), True)
        self.exists_prototype_asserts(datatypes.unicode.isdecimal(), (1, 2), False)

    def test_compound_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.exists_compound_asserts('unicode__isdecimal', [], (decimal, decimal), True)
        self.exists_compound_asserts('unicode__isdecimal', [], (1, 2), False)

    def test_prototype_isdigit(self):
        self.exists_prototype_asserts(datatypes.unicode.isdigit(), (b'1'.decode(), b'1'.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.isdigit(), (self.foo, self.foo), False)

    def test_compound_isdigit(self):
        self.exists_compound_asserts('unicode__isdigit', [], (b'1'.decode(), b'1'.decode()), True)
        self.exists_compound_asserts('unicode__isdigit', [], (self.foo, self.foo), False)

    def test_prototype_islower(self):
        self.exists_prototype_asserts(datatypes.unicode.islower(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.unicode.islower(), (b'FOO'.decode(), b'FOO'.decode()), False)

    def test_compound_islower(self):
        self.exists_compound_asserts('unicode__islower', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('unicode__islower', [], (b'FOO'.decode(), b'FOO'.decode()), False)

    def test_prototype_isupper(self):
        self.exists_prototype_asserts(datatypes.unicode.isupper(), (b'FOO'.decode(), b'FOO'.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.isupper(), (self.foo, self.foo), False)

    def test_compound_isupper(self):
        self.exists_compound_asserts('unicode__isupper', [], (b'FOO'.decode(), b'FOO'.decode()), True)
        self.exists_compound_asserts('unicode__isupper', [], (self.foo, self.foo), False)

    def test_prototype_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.exists_prototype_asserts(datatypes.unicode.isnumeric(), (numeric, numeric), True)
        self.exists_prototype_asserts(datatypes.unicode.isnumeric(), (1, 2), False)

    def test_compound_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.exists_compound_asserts('unicode__isnumeric', [], (numeric, numeric), True)
        self.exists_compound_asserts('unicode__isnumeric', [], (1, 2), False)

    def test_prototype_isspace(self):
        self.exists_prototype_asserts(datatypes.unicode.isspace(), (b'    '.decode(), b'    '.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.isspace(), (self.foo, b'bar'.decode()), False)

    def test_compound_isspace(self):
        self.exists_compound_asserts('unicode__isspace', [], (b'    '.decode(), b'    '.decode()), True)
        self.exists_compound_asserts('unicode__isspace', [], (self.foo, b'bar'.decode()), False)

    def test_prototype_istitle(self):
        self.exists_prototype_asserts(datatypes.unicode.istitle(), (b'Foo'.decode(), b'Foo'.decode()), True)
        self.exists_prototype_asserts(datatypes.unicode.istitle(), (self.foo, self.foo), False)

    def test_compound_istitle(self):
        self.exists_compound_asserts('unicode__istitle', [], (b'Foo'.decode(), b'Foo'.decode()), True)
        self.exists_compound_asserts('unicode__istitle', [], (self.foo, self.foo), False)


class ExistsCommandBytesDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'

    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.bytes.exact(self.foo), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.exact(b'bar'), (self.foo, self.foo), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('bytes__exact', [self.foo], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__exact', [b'bar'], (self.foo, self.foo), False)

    def test_prototype_iexact(self):
        self.exists_prototype_asserts(datatypes.bytes.iexact(b'FOO'), (self.foo, b'fOo',), True)
        self.exists_prototype_asserts(datatypes.bytes.iexact(b'BAR'), (self.foo, b'fOo',), False)

    def test_compound_iexact(self):
        self.exists_compound_asserts('bytes__iexact', [b'FOO'], (self.foo, b'fOo',), True)
        self.exists_compound_asserts('bytes__iexact', [b'BAR'], (self.foo, b'fOo',), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.bytes.contains(b'o'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.contains(b'b'), (self.foo, self.foo), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('bytes__contains', [b'o'], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__contains', [b'b'], (self.foo, self.foo), False)

    def test_prototype_icontains(self):
        self.exists_prototype_asserts(datatypes.bytes.icontains(b'O'), (self.foo, b'fOo'), True)
        self.exists_prototype_asserts(datatypes.bytes.icontains(b'B'), (self.foo, b'fOo'), False)

    def test_compound_icontains(self):
        self.exists_compound_asserts('bytes__icontains', [b'O'], (self.foo, b'fOo'), True)
        self.exists_compound_asserts('bytes__icontains', [b'B'], (self.foo, b'fOo'), False)

    def test_prototype_startswith(self):
        self.exists_prototype_asserts(datatypes.bytes.startswith(b'f'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.startswith(b'b'), (self.foo, self.foo), False)

    def test_compound_startswith(self):
        self.exists_compound_asserts('bytes__startswith', [b'f'], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__startswith', [b'b'], (self.foo, self.foo), False)

    def test_prototype_istartswith(self):
        self.exists_prototype_asserts(datatypes.bytes.istartswith(b'F'), (self.foo, b'fOo'), True)
        self.exists_prototype_asserts(datatypes.bytes.istartswith(b'B'), (self.foo, b'fOo'), False)

    def test_compound_istartswith(self):
        self.exists_compound_asserts('bytes__istartswith', [b'F'], (self.foo, b'fOo'), True)
        self.exists_compound_asserts('bytes__istartswith', [b'B'], (self.foo, b'fOo'), False)

    def test_prototype_endswith(self):
        self.exists_prototype_asserts(datatypes.bytes.endswith(b'oo'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.endswith(b'ar'), (self.foo, self.foo), False)

    def test_compound_endswith(self):
        self.exists_compound_asserts('bytes__endswith', [b'oo'], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__endswith', [b'ar'], (self.foo, self.foo), False)

    def test_prototype_iendswith(self):
        self.exists_prototype_asserts(datatypes.bytes.iendswith(b'OO'), (self.foo, b'fOo'), True)
        self.exists_prototype_asserts(datatypes.bytes.iendswith(b'AR'), (self.foo, b'fOo'), False)

    def test_compound_iendswith(self):
        self.exists_compound_asserts('bytes__iendswith', [b'OO'], (self.foo, b'fOo'), True)
        self.exists_compound_asserts('bytes__iendswith', [b'AR'], (self.foo, b'fOo'), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.bytes.len(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.len(4), (self.foo, self.foo), False)

    def test_compound_len(self):
        self.exists_compound_asserts('bytes__len', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__len', [4], (self.foo, self.foo), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.bytes.lenlt(4), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.lenlt(3), (self.foo, self.foo), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('bytes__lenlt', [4], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__lenlt', [3], (self.foo, self.foo), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.bytes.lenlte(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.lenlte(2), (self.foo, self.foo), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('bytes__lenlte', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__lenlte', [2], (self.foo, self.foo), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.bytes.lengt(2), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.lengt(3), (self.foo, self.foo), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('bytes__lengt', [2], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__lengt', [3], (self.foo, self.foo), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.bytes.lengte(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.lengte(4), (self.foo, self.foo), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('bytes__lengte', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__lengte', [4], (self.foo, self.foo), False)

    def test_prototype_isalnum(self):
        self.exists_prototype_asserts(datatypes.bytes.isalnum(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.isalnum(), (123, 456), False)

    def test_compound_isalnum(self):
        self.exists_compound_asserts('bytes__isalnum', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__isalnum', [], (123, 456), False)

    def test_prototype_isalnums(self):
        self.exists_prototype_asserts(datatypes.bytes.isalnums(), (b'fo o', b'f Oo'), True)
        self.exists_prototype_asserts(datatypes.bytes.isalnum(), (123, 456), False)

    def test_compound_isalnums(self):
        self.exists_compound_asserts('bytes__isalnums', [], (b'fo o', b'f Oo'), True)
        self.exists_compound_asserts('bytes__isalnums', [], (123, 456), False)

    def test_prototype_isalpha(self):
        self.exists_prototype_asserts(datatypes.bytes.isalpha(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.isalpha(), (b' ', b' '), False)

    def test_compound_isalpha(self):
        self.exists_compound_asserts('bytes__isalpha', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__isalpha', [], (b' ', b' '), False)

    def test_prototype_isalphas(self):
        self.exists_prototype_asserts(datatypes.bytes.isalphas(), (b'fo o', b'f Oo'), True)
        self.exists_prototype_asserts(datatypes.bytes.isalphas(), (b'--', b'--'), False)

    def test_compound_isalphas(self):
        self.exists_compound_asserts('bytes__isalphas', [], (b'fo o', b'f Oo'), True)
        self.exists_compound_asserts('bytes__isalphas', [], (b'--', b'--'), False)

    def test_prototype_isdigit(self):
        self.exists_prototype_asserts(datatypes.bytes.isdigit(), (b'1', b'1'), True)
        self.exists_prototype_asserts(datatypes.bytes.isdigit(), (self.foo, self.foo), False)

    def test_compound_isdigit(self):
        self.exists_compound_asserts('bytes__isdigit', [], (b'1', b'1'), True)
        self.exists_compound_asserts('bytes__isdigit', [], (self.foo, self.foo), False)

    def test_prototype_islower(self):
        self.exists_prototype_asserts(datatypes.bytes.islower(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytes.islower(), (b'FOO', b'FOO'), False)

    def test_compound_islower(self):
        self.exists_compound_asserts('bytes__islower', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytes__islower', [], (b'FOO', b'FOO'), False)

    def test_prototype_isupper(self):
        self.exists_prototype_asserts(datatypes.bytes.isupper(), (b'FOO', b'FOO'), True)
        self.exists_prototype_asserts(datatypes.bytes.isupper(), (self.foo, self.foo), False)

    def test_compound_isupper(self):
        self.exists_compound_asserts('bytes__isupper', [], (b'FOO', b'FOO'), True)
        self.exists_compound_asserts('bytes__isupper', [], (self.foo, self.foo), False)

    def test_prototype_isspace(self):
        self.exists_prototype_asserts(datatypes.bytes.isspace(), (b'    ', b'    '), True)
        self.exists_prototype_asserts(datatypes.bytes.isspace(), (self.foo, b'bar'), False)

    def test_compound_isspace(self):
        self.exists_compound_asserts('bytes__isspace', [], (b'    ', b'    '), True)
        self.exists_compound_asserts('bytes__isspace', [], (self.foo, b'bar'), False)

    def test_prototype_istitle(self):
        self.exists_prototype_asserts(datatypes.bytes.istitle(), (b'Foo', b'Foo'), True)
        self.exists_prototype_asserts(datatypes.bytes.istitle(), (self.foo, self.foo), False)

    def test_compound_istitle(self):
        self.exists_compound_asserts('bytes__istitle', [], (b'Foo', b'Foo'), True)
        self.exists_compound_asserts('bytes__istitle', [], (self.foo, self.foo), False)


class ExistsCommandBytearrayDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = bytearray(b'foo')

    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.bytearray.exact(self.foo), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.exact(bytearray(b'bar')), (self.foo, self.foo), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('bytearray__exact', [self.foo], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__exact', [bytearray(b'bar')], (self.foo, self.foo), False)

    def test_prototype_iexact(self):
        foo = bytearray(b'fOo')
        self.exists_prototype_asserts(datatypes.bytearray.iexact(bytearray(b'FOO')), (self.foo, foo,), True)
        self.exists_prototype_asserts(datatypes.bytearray.iexact(bytearray(b'BAR')), (self.foo, foo,), False)

    def test_compound_iexact(self):
        foo = bytearray(b'fOo')
        self.exists_compound_asserts('bytearray__iexact', [bytearray(b'FOO')], (self.foo, foo,), True)
        self.exists_compound_asserts('bytearray__iexact', [bytearray(b'BAR')], (self.foo, foo,), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.bytearray.contains(bytearray(b'o')), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.contains(bytearray(b'b')), (self.foo, self.foo), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('bytearray__contains', [bytearray(b'o')], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__contains', [bytearray(b'b')], (self.foo, self.foo), False)

    def test_prototype_icontains(self):
        foo = bytearray(b'fOo')
        self.exists_prototype_asserts(datatypes.bytearray.icontains(bytearray(b'O')), (self.foo, foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.icontains(bytearray(b'B')), (self.foo, foo), False)

    def test_compound_icontains(self):
        foo = bytearray(b'fOo')
        self.exists_compound_asserts('bytearray__icontains', [bytearray(b'O')], (self.foo, foo), True)
        self.exists_compound_asserts('bytearray__icontains', [bytearray(b'B')], (self.foo, foo), False)

    def test_prototype_startswith(self):
        self.exists_prototype_asserts(datatypes.bytearray.startswith(bytearray(b'f')), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.startswith(bytearray(b'b')), (self.foo, self.foo), False)

    def test_compound_startswith(self):
        self.exists_compound_asserts('bytearray__startswith', [bytearray(b'f')], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__startswith', [bytearray(b'b')], (self.foo, self.foo), False)

    def test_prototype_istartswith(self):
        foo = bytearray(b'fOo')
        self.exists_prototype_asserts(datatypes.bytearray.istartswith(bytearray(b'F')), (self.foo, foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.istartswith(bytearray(b'B')), (self.foo, foo), False)

    def test_compound_istartswith(self):
        foo = bytearray(b'fOo')
        self.exists_compound_asserts('bytearray__istartswith', [bytearray(b'F')], (self.foo, foo), True)
        self.exists_compound_asserts('bytearray__istartswith', [bytearray(b'B')], (self.foo, foo), False)

    def test_prototype_endswith(self):
        self.exists_prototype_asserts(datatypes.bytearray.endswith(bytearray(b'oo')), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.endswith(bytearray(b'ar')), (self.foo, self.foo), False)

    def test_compound_endswith(self):
        self.exists_compound_asserts('bytearray__endswith', [bytearray(b'oo')], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__endswith', [bytearray(b'ar')], (self.foo, self.foo), False)

    def test_prototype_iendswith(self):
        foo = bytearray(b'fOo')
        self.exists_prototype_asserts(datatypes.bytearray.iendswith(bytearray(b'OO')), (self.foo, foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.iendswith(bytearray(b'AR')), (self.foo, foo), False)

    def test_compound_iendswith(self):
        foo = bytearray(b'fOo')
        self.exists_compound_asserts('bytearray__iendswith', [bytearray(b'OO')], (self.foo, foo), True)
        self.exists_compound_asserts('bytearray__iendswith', [bytearray(b'AR')], (self.foo, foo), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.bytearray.len(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.len(4), (self.foo, self.foo), False)

    def test_compound_len(self):
        self.exists_compound_asserts('bytearray__len', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__len', [4], (self.foo, self.foo), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.bytearray.lenlt(4), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.lenlt(3), (self.foo, self.foo), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('bytearray__lenlt', [4], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__lenlt', [3], (self.foo, self.foo), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.bytearray.lenlte(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.lenlte(2), (self.foo, self.foo), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('bytearray__lenlte', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__lenlte', [2], (self.foo, self.foo), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.bytearray.lengt(2), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.lengt(3), (self.foo, self.foo), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('bytearray__lengt', [2], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__lengt', [3], (self.foo, self.foo), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.bytearray.lengte(3), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.lengte(4), (self.foo, self.foo), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('bytearray__lengte', [3], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__lengte', [4], (self.foo, self.foo), False)

    def test_prototype_isalnum(self):
        self.exists_prototype_asserts(datatypes.bytearray.isalnum(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.isalnum(), (123, 456), False)

    def test_compound_isalnum(self):
        self.exists_compound_asserts('bytearray__isalnum', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__isalnum', [], (123, 456), False)

    def test_prototype_isalnums(self):
        self.exists_prototype_asserts(datatypes.bytearray.isalnums(), (bytearray(b'fo o'), bytearray(b'f Oo')), True)
        self.exists_prototype_asserts(datatypes.bytearray.isalnum(), (123, 456), False)

    def test_compound_isalnums(self):
        self.exists_compound_asserts('bytearray__isalnums', [], (bytearray(b'fo o'), bytearray(b'f Oo')), True)
        self.exists_compound_asserts('bytearray__isalnums', [], (123, 456), False)

    def test_prototype_isalpha(self):
        self.exists_prototype_asserts(datatypes.bytearray.isalpha(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.isalpha(), (bytearray(b' '), bytearray(b' ')), False)

    def test_compound_isalpha(self):
        self.exists_compound_asserts('bytearray__isalpha', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__isalpha', [], (bytearray(b' '), bytearray(b' ')), False)

    def test_prototype_isalphas(self):
        self.exists_prototype_asserts(datatypes.bytearray.isalphas(), (bytearray(b'fo o'), bytearray(b'f Oo')), True)
        self.exists_prototype_asserts(datatypes.bytearray.isalphas(), (bytearray(b'--'), bytearray(b'--')), False)

    def test_compound_isalphas(self):
        self.exists_compound_asserts('bytearray__isalphas', [], (bytearray(b'fo o'), bytearray(b'f Oo')), True)
        self.exists_compound_asserts('bytearray__isalphas', [], (bytearray(b'--'), bytearray(b'--')), False)

    def test_prototype_isdigit(self):
        self.exists_prototype_asserts(datatypes.bytearray.isdigit(), (bytearray(b'1'), bytearray(b'1')), True)
        self.exists_prototype_asserts(datatypes.bytearray.isdigit(), (self.foo, self.foo), False)

    def test_compound_isdigit(self):
        self.exists_compound_asserts('bytearray__isdigit', [], (bytearray(b'1'), bytearray(b'1')), True)
        self.exists_compound_asserts('bytearray__isdigit', [], (self.foo, self.foo), False)

    def test_prototype_islower(self):
        self.exists_prototype_asserts(datatypes.bytearray.islower(), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.bytearray.islower(), (bytearray(b'FOO'), bytearray(b'FOO')), False)

    def test_compound_islower(self):
        self.exists_compound_asserts('bytearray__islower', [], (self.foo, self.foo), True)
        self.exists_compound_asserts('bytearray__islower', [], (bytearray(b'FOO'), bytearray(b'FOO')), False)

    def test_prototype_isupper(self):
        self.exists_prototype_asserts(datatypes.bytearray.isupper(), (bytearray(b'FOO'), bytearray(b'FOO')), True)
        self.exists_prototype_asserts(datatypes.bytearray.isupper(), (self.foo, self.foo), False)

    def test_compound_isupper(self):
        self.exists_compound_asserts('bytearray__isupper', [], (bytearray(b'FOO'), bytearray(b'FOO')), True)
        self.exists_compound_asserts('bytearray__isupper', [], (self.foo, self.foo), False)

    def test_prototype_isspace(self):
        self.exists_prototype_asserts(datatypes.bytearray.isspace(), (bytearray(b'    '), bytearray(b'    ')), True)
        self.exists_prototype_asserts(datatypes.bytearray.isspace(), (self.foo, bytearray(b'bar')), False)

    def test_compound_isspace(self):
        self.exists_compound_asserts('bytearray__isspace', [], (bytearray(b'    '), bytearray(b'    ')), True)
        self.exists_compound_asserts('bytearray__isspace', [], (self.foo, bytearray(b'bar')), False)

    def test_prototype_istitle(self):
        self.exists_prototype_asserts(datatypes.bytearray.istitle(), (bytearray(b'Foo'), bytearray(b'Foo')), True)
        self.exists_prototype_asserts(datatypes.bytearray.istitle(), (self.foo, self.foo), False)

    def test_compound_istitle(self):
        self.exists_compound_asserts('bytearray__istitle', [], (bytearray(b'Foo'), bytearray(b'Foo')), True)
        self.exists_compound_asserts('bytearray__istitle', [], (self.foo, self.foo), False)


class ExistsCommandNumericDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.numeric.exact(5.5), (5.5, 5.5), True)
        self.exists_prototype_asserts(datatypes.numeric.exact(5.5), (1, 1), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('numeric__exact', [5.5], (5.5, 5.5), True)
        self.exists_compound_asserts('numeric__exact', [5.5], (1, 1), False)

    def test_prototype_gt(self):
        self.exists_prototype_asserts(datatypes.numeric.gt(3), (4, 4), True)
        self.exists_prototype_asserts(datatypes.numeric.gt(3), (1, 1), False)

    def test_compound_gt(self):
        self.exists_compound_asserts('numeric__gt', [3], (4, 4), True)
        self.exists_compound_asserts('numeric__gt', [3], (1, 1), False)

    def test_prototype_gte(self):
        self.exists_prototype_asserts(datatypes.numeric.gte(5), (5, 5), True)
        self.exists_prototype_asserts(datatypes.numeric.gte(5), (4, 4), False)

    def test_compound_gte(self):
        self.exists_compound_asserts('numeric__gte', [5], (5, 5), True)
        self.exists_compound_asserts('numeric__gte', [5], (4, 4), False)

    def test_prototype_lt(self):
        self.exists_prototype_asserts(datatypes.numeric.lt(2), (1, 1), True)
        self.exists_prototype_asserts(datatypes.numeric.lt(2), (3, 3), False)

    def test_compound_lt(self):
        self.exists_compound_asserts('numeric__lt', [2], (1, 1), True)
        self.exists_compound_asserts('numeric__lt', [2], (3, 3), False)

    def test_prototype_lte(self):
        self.exists_prototype_asserts(datatypes.numeric.lte(2), (2, 2), True)
        self.exists_prototype_asserts(datatypes.numeric.lte(2), (3, 3), False)

    def test_compound_lte(self):
        self.exists_compound_asserts('numeric__lte', [2], (2, 2), True)
        self.exists_compound_asserts('numeric__lte', [2], (3, 3), False)

    def test_prototype_between(self):
        self.exists_prototype_asserts(datatypes.numeric.between(1, 2), (1, 1), True)
        self.exists_prototype_asserts(datatypes.numeric.between(1, 2), (5, 5), False)

    def test_compound_between(self):
        self.exists_compound_asserts('numeric__between', [1, 2], (1, 1), True)
        self.exists_compound_asserts('numeric__between', [1, 2], (5, 5), False)

    def test_prototype_ebetween(self):
        self.exists_prototype_asserts(datatypes.numeric.ebetween(0, 2), (1, 1), True)
        self.exists_prototype_asserts(datatypes.numeric.ebetween(1, 2), (5, 5), False)

    def test_compound_ebetween(self):
        self.exists_compound_asserts('numeric__ebetween', [0, 2], (1, 1), True)
        self.exists_compound_asserts('numeric__ebetween', [0, 2], (5, 5), False)

    def test_prototype_isodd(self):
        self.exists_prototype_asserts(datatypes.numeric.isodd(), (5, 5), True)
        self.exists_prototype_asserts(datatypes.numeric.isodd(), (2, 2), False)

    def test_compound_isodd(self):
        self.exists_compound_asserts('numeric__isodd', [], (5, 5), True)
        self.exists_compound_asserts('numeric__isodd', [], (2, 2), False)

    def test_prototype_iseven(self):
        self.exists_prototype_asserts(datatypes.numeric.iseven(), (4, 4), True)
        self.exists_prototype_asserts(datatypes.numeric.iseven(), (3, 3), False)

    def test_compound_iseven(self):
        self.exists_compound_asserts('numeric__iseven', [], (4, 4), True)
        self.exists_compound_asserts('numeric__iseven', [], (3, 3), False)

    def test_prototype_divisibleby(self):
        self.exists_prototype_asserts(datatypes.numeric.divisibleby(2), (4, 4), True)
        self.exists_prototype_asserts(datatypes.numeric.divisibleby(2), (3, 3), False)

    def test_compound_divisibleby(self):
        self.exists_compound_asserts('numeric__divisibleby', [2], (4, 4), True)
        self.exists_compound_asserts('numeric__divisibleby', [2], (3, 3), False)


class ExistsCommandIntDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.int.exact(5), (5, 5), True)
        self.exists_prototype_asserts(datatypes.int.exact(5), (4, 4), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('int__exact', [5], (5, 5), True)
        self.exists_compound_asserts('int__exact', [5], (4, 4), False)

    def test_prototype_gt(self):
        self.exists_prototype_asserts(datatypes.int.gt(3), (4, 4), True)
        self.exists_prototype_asserts(datatypes.int.gt(3), (2, 2), False)

    def test_compound_gt(self):
        self.exists_compound_asserts('int__gt', [3], (4, 4), True)
        self.exists_compound_asserts('int__gt', [3], (2, 2), False)

    def test_prototype_gte(self):
        self.exists_prototype_asserts(datatypes.int.gte(5), (5, 5), True)
        self.exists_prototype_asserts(datatypes.int.gte(5), (2, 2), False)

    def test_compound_gte(self):
        self.exists_compound_asserts('int__gte', [5], (5, 5), True)
        self.exists_compound_asserts('int__gte', [5], (2, 2), False)

    def test_prototype_lt(self):
        self.exists_prototype_asserts(datatypes.int.lt(2), (1, 1), True)
        self.exists_prototype_asserts(datatypes.int.lt(2), (4, 4), False)

    def test_compound_lt(self):
        self.exists_compound_asserts('int__lt', [2], (1, 1), True)
        self.exists_compound_asserts('int__lt', [2], (4, 4), False)

    def test_prototype_lte(self):
        self.exists_prototype_asserts(datatypes.int.lte(2), (2, 2), True)
        self.exists_prototype_asserts(datatypes.int.lte(2), (4, 4), False)

    def test_compound_lte(self):
        self.exists_compound_asserts('int__lte', [2], (2, 2), True)
        self.exists_compound_asserts('int__lte', [2], (4, 4), False)

    def test_prototype_between(self):
        self.exists_prototype_asserts(datatypes.int.between(1, 2), (1, 1), True)
        self.exists_prototype_asserts(datatypes.int.between(1, 2), (4, 4), False)

    def test_compound_between(self):
        self.exists_compound_asserts('int__between', [1, 2], (1, 1), True)
        self.exists_compound_asserts('int__between', [1, 2], (4, 4), False)

    def test_prototype_ebetween(self):
        self.exists_prototype_asserts(datatypes.int.ebetween(0, 2), (1, 1), True)
        self.exists_prototype_asserts(datatypes.int.ebetween(1, 2), (4, 4), False)

    def test_compound_ebetween(self):
        self.exists_compound_asserts('int__ebetween', [0, 2], (1, 1), True)
        self.exists_compound_asserts('int__ebetween', [0, 2], (4, 4), False)

    def test_prototype_isodd(self):
        self.exists_prototype_asserts(datatypes.int.isodd(), (5, 5), True)
        self.exists_prototype_asserts(datatypes.int.isodd(), (4, 4), False)

    def test_compound_isodd(self):
        self.exists_compound_asserts('int__isodd', [], (5, 5), True)
        self.exists_compound_asserts('int__isodd', [], (4, 4), False)

    def test_prototype_iseven(self):
        self.exists_prototype_asserts(datatypes.int.iseven(), (4, 4), True)
        self.exists_prototype_asserts(datatypes.int.iseven(), (5, 5), False)

    def test_compound_iseven(self):
        self.exists_compound_asserts('int__iseven', [], (4, 4), True)
        self.exists_compound_asserts('int__iseven', [], (5, 5), False)

    def test_prototype_divisibleby(self):
        self.exists_prototype_asserts(datatypes.int.divisibleby(2), (4, 4), True)
        self.exists_prototype_asserts(datatypes.int.divisibleby(2), (3, 3), False)

    def test_compound_divisibleby(self):
        self.exists_compound_asserts('int__divisibleby', [2], (4, 4), True)
        self.exists_compound_asserts('int__divisibleby', [2], (3, 3), False)


class ExistsCommandFloatDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.float.exact(5.5), (5.5, 5.5), True)
        self.exists_prototype_asserts(datatypes.float.exact(5.5), (5, 5), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('float__exact', [5.5], (5.5, 5.5), True)
        self.exists_compound_asserts('float__exact', [5.5], (4, 4), False)

    def test_prototype_gt(self):
        self.exists_prototype_asserts(datatypes.float.gt(3), (4.2, 4.2), True)
        self.exists_prototype_asserts(datatypes.float.gt(3), (2, 2), False)

    def test_compound_gt(self):
        self.exists_compound_asserts('float__gt', [3], (4.2, 4.2), True)
        self.exists_compound_asserts('float__gt', [3], (2, 2), False)

    def test_prototype_gte(self):
        self.exists_prototype_asserts(datatypes.float.gte(5), (5.5, 5.5), True)
        self.exists_prototype_asserts(datatypes.float.gte(5), (2, 2), False)

    def test_compound_gte(self):
        self.exists_compound_asserts('float__gte', [5], (5.5, 5.5), True)
        self.exists_compound_asserts('float__gte', [5], (2, 2), False)

    def test_prototype_lt(self):
        self.exists_prototype_asserts(datatypes.float.lt(2), (1.1, 1.1), True)
        self.exists_prototype_asserts(datatypes.float.lt(2), (3, 3), False)

    def test_compound_lt(self):
        self.exists_compound_asserts('float__lt', [2], (1.1, 1.1), True)
        self.exists_compound_asserts('float__lt', [2], (3, 3), False)

    def test_prototype_lte(self):
        self.exists_prototype_asserts(datatypes.float.lte(2), (1.8, 1.8), True)
        self.exists_prototype_asserts(datatypes.float.lte(2), (3, 3), False)

    def test_compound_lte(self):
        self.exists_compound_asserts('float__lte', [2], (1.8, 1.8), True)
        self.exists_compound_asserts('float__lte', [2], (3, 3), False)

    def test_prototype_between(self):
        self.exists_prototype_asserts(datatypes.float.between(1, 2), (1.4, 1.4), True)
        self.exists_prototype_asserts(datatypes.float.between(1, 2), (4, 4), False)

    def test_compound_between(self):
        self.exists_compound_asserts('float__between', [1, 2], (1.4, 1.4), True)
        self.exists_compound_asserts('float__between', [1, 2], (4, 4), False)

    def test_prototype_ebetween(self):
        self.exists_prototype_asserts(datatypes.float.ebetween(0, 2), (1.5, 1.5), True)
        self.exists_prototype_asserts(datatypes.float.ebetween(0, 2), (4, 4), False)

    def test_compound_ebetween(self):
        self.exists_compound_asserts('float__ebetween', [0, 2], (1.5, 1.5), True)
        self.exists_compound_asserts('float__ebetween', [0, 2], (4, 4), False)

    def test_prototype_isinteger(self):
        self.exists_prototype_asserts(datatypes.float.isinteger(), (5.0, 5.0), True)
        self.exists_prototype_asserts(datatypes.float.isinteger(), (5.2, 5.2), False)

    def test_compound_isinteger(self):
        self.exists_compound_asserts('float__isinteger', [], (5.0, 5.0), True)
        self.exists_compound_asserts('float__isinteger', [], (5.2, 5.2), False)

    def test_prototype_isodd(self):
        self.exists_prototype_asserts(datatypes.float.isodd(), (5.2, 5.2), True)
        self.exists_prototype_asserts(datatypes.float.isodd(), (2, 2), False)

    def test_compound_isodd(self):
        self.exists_compound_asserts('float__isodd', [], (5.2, 5.2), True)
        self.exists_compound_asserts('float__isodd', [], (2, 2), False)

    def test_prototype_iseven(self):
        self.exists_prototype_asserts(datatypes.float.iseven(), (4.3, 4.3), True)
        self.exists_prototype_asserts(datatypes.float.iseven(), (3, 3), False)

    def test_compound_iseven(self):
        self.exists_compound_asserts('float__iseven', [], (4.3, 4.3), True)
        self.exists_compound_asserts('float__iseven', [], (3, 3), False)

    def test_prototype_divisibleby(self):
        self.exists_prototype_asserts(datatypes.float.divisibleby(2), (4.7, 4.7), True)
        self.exists_prototype_asserts(datatypes.float.divisibleby(2), (3, 3), False)

    def test_compound_divisibleby(self):
        self.exists_compound_asserts('float__divisibleby', [2], (4.7, 4.7), True)
        self.exists_compound_asserts('float__divisibleby', [2], (3, 3), False)


class ExistsCommandLongDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.long.exact(2 ** 64), (2 ** 64, 2 ** 64), True)
        self.exists_prototype_asserts(datatypes.long.exact(2 ** 64), (2 ** 63, 2 ** 63), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('long__exact', [2 ** 64], (2 ** 64, 2 ** 64), True)
        self.exists_compound_asserts('long__exact', [2 ** 64], (2 ** 63, 2 ** 63), False)

    def test_prototype_gt(self):
        self.exists_prototype_asserts(datatypes.long.gt(2 ** 63), (2 ** 64, 2 ** 64), True)
        self.exists_prototype_asserts(datatypes.long.gt(2 ** 63), (2 ** 62, 2 ** 62), False)

    def test_compound_gt(self):
        self.exists_compound_asserts('long__gt', [2 ** 63], (2 ** 64, 2 ** 64), True)
        self.exists_compound_asserts('long__gt', [2 ** 63], (2 ** 62, 2 ** 62), False)

    def test_prototype_gte(self):
        self.exists_prototype_asserts(datatypes.long.gte(2 ** 64), (2 ** 65, 2 ** 65), True)
        self.exists_prototype_asserts(datatypes.long.gte(2 ** 64), (2 ** 63, 2 ** 63), False)

    def test_compound_gte(self):
        self.exists_compound_asserts('long__gte', [2 ** 64], (2 ** 65, 2 ** 65), True)
        self.exists_compound_asserts('long__gte', [2 ** 64], (2 ** 63, 2 ** 63), False)

    def test_prototype_lt(self):
        self.exists_prototype_asserts(datatypes.long.lt(2 ** 64), (2 ** 63, 2 ** 63), True)
        self.exists_prototype_asserts(datatypes.long.lt(2 ** 64), (2 ** 65, 2 ** 65), False)

    def test_compound_lt(self):
        self.exists_compound_asserts('long__lt', [2 ** 64], (2 ** 63, 2 ** 63), True)
        self.exists_compound_asserts('long__lt', [2 ** 64], (2 ** 65, 2 ** 65), False)

    def test_prototype_lte(self):
        self.exists_prototype_asserts(datatypes.long.lte(2 ** 64), (2 ** 63, 2 ** 63), True)
        self.exists_prototype_asserts(datatypes.long.lte(2 ** 64), (2 ** 65, 2 ** 65), False)

    def test_compound_lte(self):
        self.exists_compound_asserts('long__lte', [2 ** 64], (2 ** 63, 2 ** 63), True)
        self.exists_compound_asserts('long__lte', [2 ** 64], (2 ** 65, 2 ** 65), False)

    def test_prototype_between(self):
        self.exists_prototype_asserts(datatypes.long.between(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64), True)
        self.exists_prototype_asserts(datatypes.long.between(2 ** 63, 2 ** 65), (2 ** 66, 2 ** 66), False)

    def test_compound_between(self):
        self.exists_compound_asserts('long__between', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64), True)
        self.exists_compound_asserts('long__between', [2 ** 63, 2 ** 65], (2 ** 66, 2 ** 66), False)

    def test_prototype_ebetween(self):
        self.exists_prototype_asserts(datatypes.long.ebetween(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64), True)
        self.exists_prototype_asserts(datatypes.long.ebetween(2 ** 63, 2 ** 65), (2 ** 66, 2 ** 66), False)

    def test_compound_ebetween(self):
        self.exists_compound_asserts('long__ebetween', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64), True)
        self.exists_compound_asserts('long__ebetween', [2 ** 63, 2 ** 65], (2 ** 66, 2 ** 66), False)

    def test_prototype_isodd(self):
        self.exists_prototype_asserts(datatypes.long.isodd(), (3 ** 64, 3 ** 64), True)
        self.exists_prototype_asserts(datatypes.long.isodd(), (2 ** 64, 2 ** 64), False)

    def test_compound_isodd(self):
        self.exists_compound_asserts('long__isodd', [], (3 ** 64, 3 ** 64), True)
        self.exists_compound_asserts('long__isodd', [], (2 ** 64, 2 ** 64), False)

    def test_prototype_iseven(self):
        self.exists_prototype_asserts(datatypes.long.iseven(), (2 ** 64, 2 ** 64), True)
        self.exists_prototype_asserts(datatypes.long.iseven(), (3 ** 64, 3 ** 64), False)

    def test_compound_iseven(self):
        self.exists_compound_asserts('long__iseven', [], (2 ** 64, 2 ** 64), True)
        self.exists_compound_asserts('long__iseven', [], (3 ** 64, 3 ** 64), False)

    def test_prototype_divisibleby(self):
        self.exists_prototype_asserts(datatypes.long.divisibleby(2), (2 ** 64, 2 ** 64), True)
        self.exists_prototype_asserts(datatypes.long.divisibleby(2), (3 ** 64, 3 ** 64), False)

    def test_compound_divisibleby(self):
        self.exists_compound_asserts('long__divisibleby', [2], (2 ** 64, 2 ** 64), True)
        self.exists_compound_asserts('long__divisibleby', [2], (3 ** 64, 3 ** 64), False)


class ExistsCommandComplexDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.complex.exact(1j), (1j, 1j), True)
        self.exists_prototype_asserts(datatypes.complex.exact(1j), (2j, 2j), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('complex__exact', [1j], (1j, 1j), True)
        self.exists_compound_asserts('complex__exact', [1j], (2j, 2j), False)


class ExistsCommandIterableDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.iterable.exact(['foo']), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.iterable.exact(['foo']), (['bar'], ['bar']), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('iterable__exact', [['foo']], (['foo'], ['foo']), True)
        self.exists_compound_asserts('iterable__exact', [['foo']], (['bar'], ['bar']), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.iterable.len(1), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.iterable.len(4), (['bar'], ['bar']), False)

    def test_compound_len(self):
        self.exists_compound_asserts('iterable__len', [1], (['foo'], ['foo']), True)
        self.exists_compound_asserts('iterable__len', [4], (['bar'], ['bar']), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.iterable.lenlt(2), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.iterable.lenlt(1), (['bar'], ['bar']), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('iterable__lenlt', [2], (['foo'], ['foo']), True)
        self.exists_compound_asserts('iterable__lenlt', [1], (['bar'], ['bar']), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.iterable.lenlte(1), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.iterable.lenlte(0), (['bar'], ['bar']), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('iterable__lenlte', [1], (['foo'], ['foo']), True)
        self.exists_compound_asserts('iterable__lenlte', [0], (['bar'], ['bar']), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.iterable.lengt(0), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.iterable.lengt(1), (['bar'], ['bar']), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('iterable__lengt', [0], (['foo'], ['foo']), True)
        self.exists_compound_asserts('iterable__lengt', [1], (['bar'], ['bar']), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.iterable.lengte(1), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.iterable.lengte(2), (['bar'], ['bar']), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('iterable__lengte', [1], (['foo'], ['foo']), True)
        self.exists_compound_asserts('iterable__lengte', [2], (['bar'], ['bar']), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.iterable.contains('foo'), (['foo'], ('foo',)), True)
        self.exists_prototype_asserts(datatypes.iterable.contains('foo'), (['bar'], ('bar',)), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('iterable__contains', ['foo'], (['foo'], ['foo']), True)
        self.exists_compound_asserts('iterable__contains', ['foo'], (['bar'], ['bar']), False)

    def test_prototype_contains_all(self):
        self.exists_prototype_asserts(datatypes.iterable.contains_all(['f', 'o']), (['f', 'o'], ('f', 'o')), True)
        self.exists_prototype_asserts(datatypes.iterable.contains_all(['f', 'o']), (['b', 'z'], ('b', 'z')), False)

    def test_compound_contains_all(self):
        self.exists_compound_asserts('iterable__contains_all', [['f', 'o']], (['f', 'o'], ('f', 'o')), True)
        self.exists_compound_asserts('iterable__contains_all', [['f', 'o']], (['b', 'z'], ('b', 'z')), False)

    def test_prototype_contains_any(self):
        self.exists_prototype_asserts(datatypes.iterable.contains_any(['f', 'z']), (['f', 'o'], ('f', 'o')), True)
        self.exists_prototype_asserts(datatypes.iterable.contains_any(['f', 'z']), (['b', 'a'], ('b', 'a')), False)

    def test_compound_contains_any(self):
        self.exists_compound_asserts('iterable__contains_any', [['f', 'z']], (['f', 'o'], ('f', 'o')), True)
        self.exists_compound_asserts('iterable__contains_any', [['f', 'z']], (['b', 'a'], ('b', 'a')), False)

    def test_prototype_str_contains_str(self):
        self.exists_prototype_asserts(datatypes.iterable.str_contains_str('f'), (['fo'], ('fo',)), True)
        self.exists_prototype_asserts(datatypes.iterable.str_contains_str('f'), (['ba'], ('ba',)), False)

    def test_compound_str_contains_str(self):
        self.exists_compound_asserts('iterable__str_contains_str', ['f'], (['fo'], ('fo',)), True)
        self.exists_compound_asserts('iterable__str_contains_str', ['f'], (['ba'], ('ba',)), False)


class ExistsCommandListDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.list.exact(['foo']), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.list.exact(['foo']), (['bar'], ['bar']), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('list__exact', [['foo']], (['foo'], ['foo']), True)
        self.exists_compound_asserts('list__exact', [['foo']], (['bar'], ['bar']), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.list.len(1), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.list.len(4), (['bar'], ['bar']), False)

    def test_compound_len(self):
        self.exists_compound_asserts('list__len', [1], (['foo'], ['foo']), True)
        self.exists_compound_asserts('list__len', [4], (['bar'], ['bar']), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.list.lenlt(2), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.list.lenlt(1), (['bar'], ['bar']), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('list__lenlt', [2], (['foo'], ['foo']), True)
        self.exists_compound_asserts('list__lenlt', [1], (['bar'], ['bar']), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.list.lenlte(1), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.list.lenlte(0), (['bar'], ['bar']), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('list__lenlte', [1], (['foo'], ['foo']), True)
        self.exists_compound_asserts('list__lenlte', [0], (['bar'], ['bar']), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.list.lengt(0), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.list.lengt(1), (['bar'], ['bar']), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('list__lengt', [0], (['foo'], ['foo']), True)
        self.exists_compound_asserts('list__lengt', [1], (['bar'], ['bar']), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.list.lengte(1), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.list.lengte(2), (['bar'], ['bar']), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('list__lengte', [1], (['foo'], ['foo']), True)
        self.exists_compound_asserts('list__lengte', [2], (['bar'], ['bar']), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.list.contains('foo'), (['foo'], ['foo']), True)
        self.exists_prototype_asserts(datatypes.list.contains('foo'), (['bar'], ['bar']), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('list__contains', ['foo'], (['foo'], ['foo']), True)
        self.exists_compound_asserts('list__contains', ['foo'], (['bar'], ['bar']), False)

    def test_prototype_contains_all(self):
        self.exists_prototype_asserts(datatypes.list.contains_all(['f', 'o']), (['f', 'o'], ['f', 'o']), True)
        self.exists_prototype_asserts(datatypes.list.contains_all(['f', 'o']), (['b', 'z'], ['b', 'z']), False)

    def test_compound_contains_all(self):
        self.exists_compound_asserts('list__contains_all', [['f', 'o']], (['f', 'o'], ['f', 'o']), True)
        self.exists_compound_asserts('list__contains_all', [['f', 'o']], (['b', 'z'], ['b', 'z']), False)

    def test_prototype_contains_any(self):
        self.exists_prototype_asserts(datatypes.list.contains_any(['f', 'z']), (['f', 'o'], ['f', 'o']), True)
        self.exists_prototype_asserts(datatypes.list.contains_any(['f', 'z']), (['b', 'a'], ['b', 'a']), False)

    def test_compound_contains_any(self):
        self.exists_compound_asserts('list__contains_any', [['f', 'z']], (['f', 'o'], ['f', 'o']), True)
        self.exists_compound_asserts('list__contains_any', [['f', 'z']], (['b', 'a'], ['b', 'a']), False)

    def test_prototype_str_contains_str(self):
        self.exists_prototype_asserts(datatypes.list.str_contains_str('f'), (['fo'], ['fo']), True)
        self.exists_prototype_asserts(datatypes.list.str_contains_str('f'), (['ba'], ['ba']), False)

    def test_compound_str_contains_str(self):
        self.exists_compound_asserts('list__str_contains_str', ['f'], (['fo'], ['fo']), True)
        self.exists_compound_asserts('list__str_contains_str', ['f'], (['ba'], ['ba']), False)


class ExistsCommandTupleDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.tuple.exact(('foo',)), (('foo',), ('foo',)), True)
        self.exists_prototype_asserts(datatypes.tuple.exact(('foo',)), (('bar',), ('bar',)), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('tuple__exact', [('foo',)], (('foo',), ('foo',)), True)
        self.exists_compound_asserts('tuple__exact', [('foo',)], (('bar',), ('bar',)), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.tuple.len(1), (('foo',), ('foo',)), True)
        self.exists_prototype_asserts(datatypes.tuple.len(4), (('bar',), ('bar',)), False)

    def test_compound_len(self):
        self.exists_compound_asserts('tuple__len', [1], (('foo',), ('foo',)), True)
        self.exists_compound_asserts('tuple__len', [4], (('bar',), ('bar',)), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.tuple.lenlt(2), (('foo',), ('foo',)), True)
        self.exists_prototype_asserts(datatypes.tuple.lenlt(1), (('bar',), ('bar',)), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('tuple__lenlt', [2], (('foo',), ('foo',)), True)
        self.exists_compound_asserts('tuple__lenlt', [1], (('bar',), ('bar',)), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.tuple.lenlte(1), (('foo',), ('foo',)), True)
        self.exists_prototype_asserts(datatypes.tuple.lenlte(0), (('bar',), ('bar',)), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('tuple__lenlte', [1], (('foo',), ('foo',)), True)
        self.exists_compound_asserts('tuple__lenlte', [0], (('bar',), ('bar',)), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.tuple.lengt(0), (('foo',), ('foo',)), True)
        self.exists_prototype_asserts(datatypes.tuple.lengt(1), (('bar',), ('bar',)), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('tuple__lengt', [0], (('foo',), ('foo',)), True)
        self.exists_compound_asserts('tuple__lengt', [1], (('bar',), ('bar',)), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.tuple.lengte(1), (('foo',), ('foo',)), True)
        self.exists_prototype_asserts(datatypes.tuple.lengte(2), (('bar',), ('bar',)), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('tuple__lengte', [1], (('foo',), ('foo',)), True)
        self.exists_compound_asserts('tuple__lengte', [2], (('bar',), ('bar',)), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.tuple.contains('foo'), (('foo',), ('foo',)), True)
        self.exists_prototype_asserts(datatypes.tuple.contains('foo'), (('bar',), ('bar',)), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('tuple__contains', ['foo'], (('foo',), ('foo',)), True)
        self.exists_compound_asserts('tuple__contains', ['foo'], (('bar',), ('bar',)), False)

    def test_prototype_contains_all(self):
        self.exists_prototype_asserts(datatypes.tuple.contains_all(('f', 'o')), (('f', 'o'), ('f', 'o')), True)
        self.exists_prototype_asserts(datatypes.tuple.contains_all(('f', 'o')), (('b', 'a'), ('b', 'a')), False)

    def test_compound_contains_all(self):
        self.exists_compound_asserts('tuple__contains_all', [('f', 'o')], (('f', 'o'), ('f', 'o')), True)
        self.exists_compound_asserts('tuple__contains_all', [('f', 'o')], (('b', 'a'), ('b', 'a')), False)

    def test_prototype_contains_any(self):
        self.exists_prototype_asserts(datatypes.tuple.contains_any(('f', 'z')), (('f', 'o'), ('f', 'o')), True)
        self.exists_prototype_asserts(datatypes.tuple.contains_any(('f', 'z')), (('b', 'a'), ('b', 'a')), False)

    def test_compound_contains_any(self):
        self.exists_compound_asserts('tuple__contains_any', [('f', 'z')], (('f', 'o'), ('f', 'o')), True)
        self.exists_compound_asserts('tuple__contains_any', [('f', 'z')], (('b', 'a'), ('b', 'a')), False)

    def test_prototype_str_contains_str(self):
        self.exists_prototype_asserts(datatypes.tuple.str_contains_str('f'), (('fo',), ('fo',)), True)
        self.exists_prototype_asserts(datatypes.tuple.str_contains_str('f'), (('ba',), ('ba',)), False)

    def test_compound_str_contains_str(self):
        self.exists_compound_asserts('tuple__str_contains_str', ['f'], (('fo',), ('fo',)), True)
        self.exists_compound_asserts('tuple__str_contains_str', ['f'], (('ba',), ('ba',)), False)


class ExistsCommandSetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = set(['foo'])

    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.set.exact(self.foo), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.exact(self.foo), (['bar'], ['bar']), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('set__exact', [self.foo], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__exact', [self.foo], (['bar'], ['bar']), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.set.len(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.len(4), (['bar'], ['bar']), False)

    def test_compound_len(self):
        self.exists_compound_asserts('set__len', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__len', [4], (['bar'], ['bar']), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.set.lenlt(2), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.lenlt(1), (['bar'], ['bar']), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('set__lenlt', [2], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__lenlt', [1], (['bar'], ['bar']), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.set.lenlte(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.lenlte(0), (['bar'], ['bar']), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('set__lenlte', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__lenlte', [0], (['bar'], ['bar']), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.set.lengt(0), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.lengt(1), (['bar'], ['bar']), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('set__lengt', [0], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__lengt', [1], (['bar'], ['bar']), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.set.lengte(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.lengte(2), (['bar'], ['bar']), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('set__lengte', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__lengte', [2], (['bar'], ['bar']), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.set.contains('foo'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.contains('foo'), (['bar'], ['bar']), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('set__contains', ['foo'], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__contains', ['foo'], (['bar'], ['bar']), False)

    def test_prototype_contains_all(self):
        self.exists_prototype_asserts(datatypes.set.contains_all(['f', 'o']), (set(['f', 'o']), set(['f', 'o'])), True)
        self.exists_prototype_asserts(datatypes.set.contains_all(['f', 'o']), (['b', 'z'], ['b', 'z']), False)

    def test_compound_contains_all(self):
        self.exists_compound_asserts('set__contains_all', [['f', 'o']], (set(['f', 'o']), set(['f', 'o'])), True)
        self.exists_compound_asserts('set__contains_all', [['f', 'o']], (['b', 'z'], ['b', 'z']), False)

    def test_prototype_contains_any(self):
        self.exists_prototype_asserts(datatypes.set.contains_any(['f', 'z']), (set(['f', 'o']), set(['f', 'o'])), True)
        self.exists_prototype_asserts(datatypes.set.contains_any(['f', 'z']), (['b', 'a'], ['b', 'a']), False)

    def test_compound_contains_any(self):
        self.exists_compound_asserts('set__contains_any', [['f', 'z']], (set(['f', 'o']), set(['f', 'o'])), True)
        self.exists_compound_asserts('set__contains_any', [['f', 'z']], (['b', 'a'], ['b', 'a']), False)

    def test_prototype_str_contains_str(self):
        self.exists_prototype_asserts(datatypes.set.str_contains_str('f'), (set(['fo']), set(['fo'])), True)
        self.exists_prototype_asserts(datatypes.set.str_contains_str('f'), (['ba'], ['ba']), False)

    def test_compound_str_contains_str(self):
        self.exists_compound_asserts('set__str_contains_str', ['f'], (set(['fo']), set(['fo'])), True)
        self.exists_compound_asserts('set__str_contains_str', ['f'], (['ba'], ['ba']), False)

    def test_prototype_isdisjoint(self):
        self.exists_prototype_asserts(datatypes.set.isdisjoint(set(['bar'])), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.isdisjoint(set(['foo'])), (self.foo, self.foo), False)

    def test_compound_isdisjoint(self):
        self.exists_compound_asserts('set__isdisjoint', [set(['bar'])], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__isdisjoint', [set(['foo'])], (self.foo, self.foo), False)

    def test_prototype_issubset(self):
        self.exists_prototype_asserts(datatypes.set.issubset(set(['foo'])), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.issubset(set(['bar'])), (self.foo, self.foo), False)

    def test_compound_issubset(self):
        self.exists_compound_asserts('set__issubset', [set(['foo'])], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__issubset', [set(['bar'])], (self.foo, self.foo), False)

    def test_prototype_eissubset(self):
        self.exists_prototype_asserts(datatypes.set.eissubset(set(['foo', 'bar'])), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.eissubset(set(['bar', 'baz'])), (self.foo, self.foo), False)

    def test_compound_eissubset(self):
        self.exists_compound_asserts('set__eissubset', [set(['foo', 'bar'])], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__eissubset', [set(['bar', 'baz'])], (self.foo, self.foo), False)

    def test_prototype_issuperset(self):
        self.exists_prototype_asserts(datatypes.set.issuperset(set(['foo'])), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.set.issuperset(set(['bar'])), (self.foo, self.foo), False)

    def test_compound_issuperset(self):
        self.exists_compound_asserts('set__issuperset', [set(['foo'])], (self.foo, self.foo), True)
        self.exists_compound_asserts('set__issuperset', [set(['bar'])], (self.foo, self.foo), False)

    def test_prototype_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.exists_prototype_asserts(datatypes.set.eissuperset(set(['foo'])), (foo, foo), True)
        self.exists_prototype_asserts(datatypes.set.eissuperset(set(['baz'])), (foo, foo), False)

    def test_compound_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.exists_compound_asserts('set__eissuperset', [set(['foo'])], (foo, foo), True)
        self.exists_compound_asserts('set__eissuperset', [set(['baz'])], (foo, foo), False)


class ExistsCommandFrozensetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = frozenset(['foo'])

    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.frozenset.exact(self.foo), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.exact(self.foo), (['bar'], ['bar']), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('frozenset__exact', [self.foo], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__exact', [self.foo], (['bar'], ['bar']), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.frozenset.len(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.len(4), (['bar'], ['bar']), False)

    def test_compound_len(self):
        self.exists_compound_asserts('frozenset__len', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__len', [4], (['bar'], ['bar']), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.frozenset.lenlt(2), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.lenlt(1), (['bar'], ['bar']), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('frozenset__lenlt', [2], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__lenlt', [1], (['bar'], ['bar']), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.frozenset.lenlte(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.lenlte(0), (['bar'], ['bar']), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('frozenset__lenlte', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__lenlte', [0], (['bar'], ['bar']), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.frozenset.lengt(0), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.lengt(1), (['bar'], ['bar']), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('frozenset__lengt', [0], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__lengt', [1], (['bar'], ['bar']), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.frozenset.lengte(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.lengte(2), (['bar'], ['bar']), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('frozenset__lengte', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__lengte', [2], (['bar'], ['bar']), False)

    def test_prototype_contains(self):
        self.exists_prototype_asserts(datatypes.frozenset.contains('foo'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.contains('foo'), (['bar'], ['bar']), False)

    def test_compound_contains(self):
        self.exists_compound_asserts('frozenset__contains', ['foo'], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__contains', ['foo'], (['bar'], ['bar']), False)

    def test_prototype_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.exists_prototype_asserts(datatypes.frozenset.contains_all(['f', 'o']), (foo, foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.contains_all(['f', 'o']), (['b', 'z'], ['b', 'z']), False)

    def test_compound_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.exists_compound_asserts('frozenset__contains_all', [['f', 'o']], (foo, foo), True)
        self.exists_compound_asserts('frozenset__contains_all', [['f', 'o']], (['b', 'z'], ['b', 'z']), False)

    def test_prototype_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.exists_prototype_asserts(datatypes.frozenset.contains_any(['f', 'z']), (foo, foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.contains_any(['f', 'z']), (['b', 'a'], ['b', 'a']), False)

    def test_compound_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.exists_compound_asserts('frozenset__contains_any', [['f', 'z']], (foo, foo), True)
        self.exists_compound_asserts('frozenset__contains_any', [['f', 'z']], (['b', 'a'], ['b', 'a']), False)

    def test_prototype_str_contains_str(self):
        foo = frozenset(['fo'])
        self.exists_prototype_asserts(datatypes.frozenset.str_contains_str('f'), (foo, foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.str_contains_str('f'), (['ba'], ['ba']), False)

    def test_compound_str_contains_str(self):
        foo = frozenset(['fo'])
        self.exists_compound_asserts('frozenset__str_contains_str', ['f'], (foo, foo), True)
        self.exists_compound_asserts('frozenset__str_contains_str', ['f'], (['ba'], ['ba']), False)

    def test_prototype_isdisjoint(self):
        self.exists_prototype_asserts(datatypes.frozenset.isdisjoint(frozenset(['bar'])), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.isdisjoint(frozenset(['foo'])), (self.foo, self.foo), False)

    def test_compound_isdisjoint(self):
        self.exists_compound_asserts('frozenset__isdisjoint', [frozenset(['bar'])], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__isdisjoint', [frozenset(['foo'])], (self.foo, self.foo), False)

    def test_prototype_issubset(self):
        self.exists_prototype_asserts(datatypes.frozenset.issubset(frozenset(['foo'])), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.issubset(frozenset(['bar'])), (self.foo, self.foo), False)

    def test_compound_issubset(self):
        self.exists_compound_asserts('frozenset__issubset', [frozenset(['foo'])], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__issubset', [frozenset(['bar'])], (self.foo, self.foo), False)

    def test_prototype_eissubset(self):
        foo = self.foo
        self.exists_prototype_asserts(datatypes.frozenset.eissubset(frozenset(['foo', 'bar'])), (foo, foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.eissubset(frozenset(['bar', 'baz'])), (foo, foo), False)

    def test_compound_eissubset(self):
        self.exists_compound_asserts('frozenset__eissubset', [frozenset(['foo', 'bar'])], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__eissubset', [frozenset(['bar', 'baz'])], (self.foo, self.foo), False)

    def test_prototype_issuperset(self):
        self.exists_prototype_asserts(datatypes.frozenset.issuperset(frozenset(['foo'])), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.issuperset(frozenset(['bar'])), (self.foo, self.foo), False)

    def test_compound_issuperset(self):
        self.exists_compound_asserts('frozenset__issuperset', [frozenset(['foo'])], (self.foo, self.foo), True)
        self.exists_compound_asserts('frozenset__issuperset', [frozenset(['bar'])], (self.foo, self.foo), False)

    def test_prototype_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.exists_prototype_asserts(datatypes.frozenset.eissuperset(frozenset(['foo'])), (foo, foo), True)
        self.exists_prototype_asserts(datatypes.frozenset.eissuperset(frozenset(['baz'])), (foo, foo), False)

    def test_compound_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.exists_compound_asserts('frozenset__eissuperset', [frozenset(['foo'])], (foo, foo), True)
        self.exists_compound_asserts('frozenset__eissuperset', [frozenset(['baz'])], (foo, foo), False)


class ExistsCommandDictDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = {'foo': 'bar'}
        cls.bar = {'yada': 'yada'}

    def test_prototype_exact(self):
        self.exists_prototype_asserts(datatypes.dict.exact(self.foo), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.exact(self.foo), (self.bar, self.bar), False)

    def test_compound_exact(self):
        self.exists_compound_asserts('dict__exact', [self.foo], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__exact', [self.foo], (self.bar, self.bar), False)

    def test_prototype_len(self):
        self.exists_prototype_asserts(datatypes.dict.len(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.len(4), (self.bar, self.bar), False)

    def test_compound_len(self):
        self.exists_compound_asserts('dict__len', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__len', [4], (self.bar, self.bar), False)

    def test_prototype_lenlt(self):
        self.exists_prototype_asserts(datatypes.dict.lenlt(2), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.lenlt(1), (self.bar, self.bar), False)

    def test_compound_lenlt(self):
        self.exists_compound_asserts('dict__lenlt', [2], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__lenlt', [1], (self.bar, self.bar), False)

    def test_prototype_lenlte(self):
        self.exists_prototype_asserts(datatypes.dict.lenlte(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.lenlte(0), (self.bar, self.bar), False)

    def test_compound_lenlte(self):
        self.exists_compound_asserts('dict__lenlte', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__lenlte', [0], (self.bar, self.bar), False)

    def test_prototype_lengt(self):
        self.exists_prototype_asserts(datatypes.dict.lengt(0), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.lengt(1), (self.bar, self.bar), False)

    def test_compound_lengt(self):
        self.exists_compound_asserts('dict__lengt', [0], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__lengt', [1], (self.bar, self.bar), False)

    def test_prototype_lengte(self):
        self.exists_prototype_asserts(datatypes.dict.lengte(1), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.lengte(2), (self.bar, self.bar), False)

    def test_compound_lengte(self):
        self.exists_compound_asserts('dict__lengte', [1], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__lengte', [2], (self.bar, self.bar), False)

    def test_prototype_contains_key(self):
        self.exists_prototype_asserts(datatypes.dict.contains_key('foo'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.contains_key('foo'), (self.bar, self.bar), False)

    def test_compound_contains_key(self):
        self.exists_compound_asserts('dict__contains_key', ['foo'], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__contains_key', ['foo'], (self.bar, self.bar), False)

    def test_prototype_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.exists_prototype_asserts(datatypes.dict.contains_all_keys(['foo', 'bar']), (foo, foo), True)
        self.exists_prototype_asserts(datatypes.dict.contains_all_keys(['foo', 'bar']), (self.bar, self.bar), False)

    def test_compound_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.exists_compound_asserts('dict__contains_all_keys', [['foo', 'bar']], (foo, foo), True)
        self.exists_compound_asserts('dict__contains_all_keys', [['foo', 'bar']], (self.bar, self.bar), False)

    def test_prototype_contains_any_keys(self):
        self.exists_prototype_asserts(datatypes.dict.contains_any_keys(['foo', 'z']), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.contains_any_keys(['foo', 'z']), (self.bar, self.bar), False)

    def test_compound_contains_any_keys(self):
        self.exists_compound_asserts('dict__contains_any_keys', [['foo', 'z']], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__contains_any_keys', [['foo', 'z']], (self.bar, self.bar), False)

    def test_prototype_key_contains_str(self):
        self.exists_prototype_asserts(datatypes.dict.key_contains_str('f'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.key_contains_str('f'), (self.bar, self.bar), False)

    def test_compound_key_contains_str(self):
        self.exists_compound_asserts('dict__key_contains_str', ['f'], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__key_contains_str', ['f'], (self.bar, self.bar), False)

    def test_prototype_contains_value(self):
        self.exists_prototype_asserts(datatypes.dict.contains_value('bar'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.contains_value('bar'), (self.bar, self.bar), False)

    def test_compound_contains_value(self):
        self.exists_compound_asserts('dict__contains_value', ['bar'], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__contains_value', ['bar'], (self.bar, self.bar), False)

    def test_prototype_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.exists_prototype_asserts(datatypes.dict.contains_all_values(['baz', 'bar']), (foo, foo), True)
        self.exists_prototype_asserts(datatypes.dict.contains_all_values(['baz', 'bar']), (self.bar, self.bar), False)

    def test_compound_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.exists_compound_asserts('dict__contains_all_values', [['baz', 'bar']], (foo, foo), True)
        self.exists_compound_asserts('dict__contains_all_values', [['baz', 'bar']], (self.bar, self.bar), False)

    def test_prototype_contains_any_values(self):
        self.exists_prototype_asserts(datatypes.dict.contains_any_values(['bar', 'z']), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.contains_any_values(['bar', 'z']), (self.bar, self.bar), False)

    def test_compound_contains_any_values(self):
        self.exists_compound_asserts('dict__contains_any_values', [['bar', 'z']], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__contains_any_values', [['bar', 'z']], (self.bar, self.bar), False)

    def test_prototype_value_contains_str(self):
        self.exists_prototype_asserts(datatypes.dict.value_contains_str('b'), (self.foo, self.foo), True)
        self.exists_prototype_asserts(datatypes.dict.value_contains_str('b'), (self.bar, self.bar), False)

    def test_compound_value_contains_str(self):
        self.exists_compound_asserts('dict__value_contains_str', ['b'], (self.foo, self.foo), True)
        self.exists_compound_asserts('dict__value_contains_str', ['b'], (self.bar, self.bar), False)


class CountCommandTestCase(unittest.TestCase):
    def test_prototype(self):
        self.assertIsInstance(commands.count(datatypes.bool), commands.Command)
        self.assertEqual(commands.count(datatypes.bool, limit=1).inside([]), 0)


class CountCommandBoolDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.bool.exact(True), (True, True), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('bool__exact', [True], (True, True), 2)

    def test_prototype_true(self):
        self.count_prototype_asserts(datatypes.bool.true, (True, True), 2)

    def test_compound_true(self):
        self.count_compound_asserts('bool__true', [], (True, True), 2)

    def test_prototype_false(self):
        self.count_prototype_asserts(datatypes.bool.false, (False, False), 2)

    def test_compound_false(self):
        self.count_compound_asserts('bool__false', [], (False, False), 2)


class CountCommandStringDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = 'foo'

    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.string.exact(self.foo), (self.foo, self.foo), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('string__exact', [self.foo], (self.foo, self.foo), 2)

    def test_prototype_iexact(self):
        self.count_prototype_asserts(datatypes.string.iexact('FOO'), (self.foo, 'fOo', 'Foo'), 3)

    def test_compound_iexact(self):
        self.count_compound_asserts('string__iexact', ['FOO'], (self.foo, 'fOo', 'Foo'), 3)

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.string.contains('o'), (self.foo,), 1)

    def test_compound_contains(self):
        self.count_compound_asserts('string__contains', ['o'], (self.foo,), 1)

    def test_prototype_icontains(self):
        self.count_prototype_asserts(datatypes.string.icontains('O'), (self.foo, 'fOo'), 2)

    def test_compound_icontains(self):
        self.count_compound_asserts('string__icontains', ['O'], (self.foo, 'fOo'), 2)

    def test_prototype_startswith(self):
        self.count_prototype_asserts(datatypes.string.startswith('f'), (self.foo, self.foo), 2)

    def test_compound_startswith(self):
        self.count_compound_asserts('string__startswith', ['f'], (self.foo, self.foo), 2)

    def test_prototype_istartswith(self):
        self.count_prototype_asserts(datatypes.string.istartswith('F'), (self.foo, 'fOo'), 2)

    def test_compound_istartswith(self):
        self.count_compound_asserts('string__istartswith', ['F'], (self.foo, 'fOo'), 2)

    def test_prototype_endswith(self):
        self.count_prototype_asserts(datatypes.string.endswith('oo'), (self.foo, 'bar'), 1)

    def test_compound_endswith(self):
        self.count_compound_asserts('string__endswith', ['oo'], (self.foo, 'bar'), 1)

    def test_prototype_iendswith(self):
        self.count_prototype_asserts(datatypes.string.iendswith('OO'), (self.foo, 'fOo'), 2)

    def test_compound_iendswith(self):
        self.count_compound_asserts('string__iendswith', ['OO'], (self.foo, 'fOo'), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.string.len(3), (self.foo, self.foo), 2)

    def test_compound_len(self):
        self.count_compound_asserts('string__len', [3], (self.foo, self.foo), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.string.lenlt(4), (self.foo, self.foo), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('string__lenlt', [4], (self.foo, self.foo), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.string.lenlte(3), (self.foo, self.foo), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('string__lenlte', [3], (self.foo, self.foo), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.string.lengt(2), (self.foo, self.foo), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('string__lengt', [2], (self.foo, self.foo), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.string.lengte(3), (self.foo, self.foo), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('string__lengte', [3], (self.foo, self.foo), 2)

    def test_prototype_isalnum(self):
        self.count_prototype_asserts(datatypes.string.isalnum(), (self.foo, self.foo), 2)

    def test_compound_isalnum(self):
        self.count_compound_asserts('string__isalnum', [], (self.foo, self.foo), 2)

    def test_prototype_isalnums(self):
        self.count_prototype_asserts(datatypes.string.isalnums(), ('fo o', 'f Oo'), 2)

    def test_compound_isalnums(self):
        self.count_compound_asserts('string__isalnums', [], ('fo o', 'f Oo'), 2)

    def test_prototype_isalpha(self):
        self.count_prototype_asserts(datatypes.string.isalpha(), (self.foo, self.foo), 2)

    def test_compound_isalpha(self):
        self.count_compound_asserts('string__isalpha', [], (self.foo, self.foo), 2)

    def test_prototype_isalphas(self):
        self.count_prototype_asserts(datatypes.string.isalphas(), ('fo o', 'f Oo'), 2)

    def test_compound_isalphas(self):
        self.count_compound_asserts('string__isalphas', [], ('fo o', 'f Oo'), 2)

    def test_prototype_isdigit(self):
        self.count_prototype_asserts(datatypes.string.isdigit(), ('1', '1'), 2)

    def test_compound_isdigit(self):
        self.count_compound_asserts('string__isdigit', [], ('1', '1'), 2)

    def test_prototype_islower(self):
        self.count_prototype_asserts(datatypes.string.islower(), (self.foo, self.foo), 2)

    def test_compound_islower(self):
        self.count_compound_asserts('string__islower', [], (self.foo, self.foo), 2)

    def test_prototype_isupper(self):
        self.count_prototype_asserts(datatypes.string.isupper(), ('FOO', 'FOO'), 2)

    def test_compound_isupper(self):
        self.count_compound_asserts('string__isupper', [], ('FOO', 'FOO'), 2)

    def test_prototype_isspace(self):
        self.count_prototype_asserts(datatypes.string.isspace(), ('    ', '    '), 2)

    def test_compound_isspace(self):
        self.count_compound_asserts('string__isspace', [], ('    ', '    '), 2)

    def test_prototype_istitle(self):
        self.count_prototype_asserts(datatypes.string.istitle(), ('Foo', 'Foo'), 2)

    def test_compound_istitle(self):
        self.count_compound_asserts('string__istitle', [], ('Foo', 'Foo'), 2)


class CountCommandUnicodeDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'.decode()

    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.unicode.exact(self.foo), (self.foo, self.foo), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('unicode__exact', [self.foo], (self.foo, self.foo), 2)

    def test_prototype_iexact(self):
        self.count_prototype_asserts(
            datatypes.unicode.iexact(b'FOO'.decode()),
            (self.foo, b'fOo'.decode(), b'Foo'.decode()), 3
        )

    def test_compound_iexact(self):
        self.count_compound_asserts(
            'unicode__iexact', [b'FOO'.decode()],
            (self.foo, b'fOo'.decode(), b'Foo'.decode()), 3
        )

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.unicode.contains(b'o'.decode()), (self.foo,), 1)

    def test_compound_contains(self):
        self.count_compound_asserts('unicode__contains', [b'o'.decode()], (self.foo,), 1)

    def test_prototype_icontains(self):
        self.count_prototype_asserts(datatypes.unicode.icontains(b'O'.decode()), (self.foo, b'fOo'.decode()), 2)

    def test_compound_icontains(self):
        self.count_compound_asserts('unicode__icontains', [b'O'.decode()], (self.foo, b'fOo'.decode()), 2)

    def test_prototype_startswith(self):
        self.count_prototype_asserts(datatypes.unicode.startswith(b'f'.decode()), (self.foo, self.foo), 2)

    def test_compound_startswith(self):
        self.count_compound_asserts('unicode__startswith', [b'f'.decode()], (self.foo, self.foo), 2)

    def test_prototype_istartswith(self):
        self.count_prototype_asserts(datatypes.unicode.istartswith(b'F'.decode()), (self.foo, b'fOo'.decode()), 2)

    def test_compound_istartswith(self):
        self.count_compound_asserts('unicode__istartswith', [b'F'.decode()], (self.foo, b'fOo'.decode()), 2)

    def test_prototype_endswith(self):
        self.count_prototype_asserts(datatypes.unicode.endswith(b'oo'.decode()), (self.foo, b'bar'.decode()), 1)

    def test_compound_endswith(self):
        self.count_compound_asserts('unicode__endswith', [b'oo'.decode()], (self.foo, b'bar'.decode()), 1)

    def test_prototype_iendswith(self):
        self.count_prototype_asserts(datatypes.unicode.iendswith(b'OO'.decode()), (self.foo, b'fOo'.decode()), 2)

    def test_compound_iendswith(self):
        self.count_compound_asserts('unicode__iendswith', [b'OO'.decode()], (self.foo, b'fOo'.decode()), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.unicode.len(3), (self.foo, self.foo), 2)

    def test_compound_len(self):
        self.count_compound_asserts('unicode__len', [3], (self.foo, self.foo), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.unicode.lenlt(4), (self.foo, self.foo), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('unicode__lenlt', [4], (self.foo, self.foo), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.unicode.lenlte(3), (self.foo, self.foo), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('unicode__lenlte', [3], (self.foo, self.foo), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.unicode.lengt(2), (self.foo, self.foo), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('unicode__lengt', [2], (self.foo, self.foo), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.unicode.lengte(3), (self.foo, self.foo), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('unicode__lengte', [3], (self.foo, self.foo), 2)

    def test_prototype_isalnum(self):
        self.count_prototype_asserts(datatypes.unicode.isalnum(), (self.foo, self.foo), 2)

    def test_compound_isalnum(self):
        self.count_compound_asserts('unicode__isalnum', [], (self.foo, self.foo), 2)

    def test_prototype_isalnums(self):
        self.count_prototype_asserts(datatypes.unicode.isalnums(), (b'fo o'.decode(), b'f Oo'.decode()), 2)

    def test_compound_isalnums(self):
        self.count_compound_asserts('unicode__isalnums', [], (b'fo o'.decode(), b'f Oo'.decode()), 2)

    def test_prototype_isalpha(self):
        self.count_prototype_asserts(datatypes.unicode.isalpha(), (self.foo, self.foo), 2)

    def test_compound_isalpha(self):
        self.count_compound_asserts('unicode__isalpha', [], (self.foo, self.foo), 2)

    def test_prototype_isalphas(self):
        self.count_prototype_asserts(datatypes.unicode.isalphas(), (b'fo o'.decode(), b'f Oo'.decode()), 2)

    def test_compound_isalphas(self):
        self.count_compound_asserts('unicode__isalphas', [], (b'fo o'.decode(), b'f Oo'.decode()), 2)

    def test_prototype_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.count_prototype_asserts(datatypes.unicode.isdecimal(), (decimal, decimal), 2)

    def test_compound_isdecimal(self):
        decimal = b'\xd9\xa0'.decode('utf-8')
        self.count_compound_asserts('unicode__isdecimal', [], (decimal, decimal), 2)

    def test_prototype_isdigit(self):
        self.count_prototype_asserts(datatypes.unicode.isdigit(), (b'1'.decode(), b'1'.decode()), 2)

    def test_compound_isdigit(self):
        self.count_compound_asserts('unicode__isdigit', [], (b'1'.decode(), b'1'.decode()), 2)

    def test_prototype_islower(self):
        self.count_prototype_asserts(datatypes.unicode.islower(), (self.foo, self.foo), 2)

    def test_compound_islower(self):
        self.count_compound_asserts('unicode__islower', [], (self.foo, self.foo), 2)

    def test_prototype_isupper(self):
        self.count_prototype_asserts(datatypes.unicode.isupper(), (b'FOO'.decode(), b'FOO'.decode()), 2)

    def test_compound_isupper(self):
        self.count_compound_asserts('unicode__isupper', [], (b'FOO'.decode(), b'FOO'.decode()), 2)

    def test_prototype_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.count_prototype_asserts(datatypes.unicode.isnumeric(), (numeric, numeric), 2)

    def test_compound_isnumeric(self):
        numeric = b'\xe2\x85\x95'.decode('utf-8')
        self.count_compound_asserts('unicode__isnumeric', [], (numeric, numeric), 2)

    def test_prototype_isspace(self):
        self.count_prototype_asserts(datatypes.unicode.isspace(), (b'    '.decode(), b'    '.decode()), 2)

    def test_compound_isspace(self):
        self.count_compound_asserts('unicode__isspace', [], (b'    '.decode(), b'    '.decode()), 2)

    def test_prototype_istitle(self):
        self.count_prototype_asserts(datatypes.unicode.istitle(), (b'Foo'.decode(), b'Foo'.decode()), 2)

    def test_compound_istitle(self):
        self.count_compound_asserts('unicode__istitle', [], (b'Foo'.decode(), b'Foo'.decode()), 2)


class CountCommandBytesDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = b'foo'

    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.bytes.exact(self.foo), (self.foo, self.foo), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('bytes__exact', [self.foo], (self.foo, self.foo), 2)

    def test_prototype_iexact(self):
        self.count_prototype_asserts(datatypes.bytes.iexact(b'FOO'), (self.foo, b'fOo', b'Foo'), 3)

    def test_compound_iexact(self):
        self.count_compound_asserts('bytes__iexact', [b'FOO'], (self.foo, b'fOo', b'Foo'), 3)

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.bytes.contains(b'o'), (self.foo,), 1)

    def test_compound_contains(self):
        self.count_compound_asserts('bytes__contains', [b'o'], (self.foo,), 1)

    def test_prototype_icontains(self):
        self.count_prototype_asserts(datatypes.bytes.icontains(b'O'), (self.foo, b'fOo'), 2)

    def test_compound_icontains(self):
        self.count_compound_asserts('bytes__icontains', [b'O'], (self.foo, b'fOo'), 2)

    def test_prototype_startswith(self):
        self.count_prototype_asserts(datatypes.bytes.startswith(b'f'), (self.foo, self.foo), 2)

    def test_compound_startswith(self):
        self.count_compound_asserts('bytes__startswith', [b'f'], (self.foo, self.foo), 2)

    def test_prototype_istartswith(self):
        self.count_prototype_asserts(datatypes.bytes.istartswith(b'F'), (self.foo, b'fOo'), 2)

    def test_compound_istartswith(self):
        self.count_compound_asserts('bytes__istartswith', [b'F'], (self.foo, b'fOo'), 2)

    def test_prototype_endswith(self):
        self.count_prototype_asserts(datatypes.bytes.endswith(b'oo'), (self.foo, b'bar'), 1)

    def test_compound_endswith(self):
        self.count_compound_asserts('bytes__endswith', [b'oo'], (self.foo, b'bar'), 1)

    def test_prototype_iendswith(self):
        self.count_prototype_asserts(datatypes.bytes.iendswith(b'OO'), (self.foo, b'fOo'), 2)

    def test_compound_iendswith(self):
        self.count_compound_asserts('bytes__iendswith', [b'OO'], (self.foo, b'fOo'), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.bytes.len(3), (self.foo, self.foo), 2)

    def test_compound_len(self):
        self.count_compound_asserts('bytes__len', [3], (self.foo, self.foo), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.bytes.lenlt(4), (self.foo, self.foo), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('bytes__lenlt', [4], (self.foo, self.foo), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.bytes.lenlte(3), (self.foo, self.foo), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('bytes__lenlte', [3], (self.foo, self.foo), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.bytes.lengt(2), (self.foo, self.foo), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('bytes__lengt', [2], (self.foo, self.foo), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.bytes.lengte(3), (self.foo, self.foo), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('bytes__lengte', [3], (self.foo, self.foo), 2)

    def test_prototype_isalnum(self):
        self.count_prototype_asserts(datatypes.bytes.isalnum(), (self.foo, self.foo), 2)

    def test_compound_isalnum(self):
        self.count_compound_asserts('bytes__isalnum', [], (self.foo, self.foo), 2)

    def test_prototype_isalnums(self):
        self.count_prototype_asserts(datatypes.bytes.isalnums(), (b'fo o', b'f Oo'), 2)

    def test_compound_isalnums(self):
        self.count_compound_asserts('bytes__isalnums', [], (b'fo o', b'f Oo'), 2)

    def test_prototype_isalpha(self):
        self.count_prototype_asserts(datatypes.bytes.isalpha(), (self.foo, self.foo), 2)

    def test_compound_isalpha(self):
        self.count_compound_asserts('bytes__isalpha', [], (self.foo, self.foo), 2)

    def test_prototype_isalphas(self):
        self.count_prototype_asserts(datatypes.bytes.isalphas(), (b'fo o', b'f Oo'), 2)

    def test_compound_isalphas(self):
        self.count_compound_asserts('bytes__isalphas', [], (b'fo o', b'f Oo'), 2)

    def test_prototype_isdigit(self):
        self.count_prototype_asserts(datatypes.bytes.isdigit(), (b'1', b'1'), 2)

    def test_compound_isdigit(self):
        self.count_compound_asserts('bytes__isdigit', [], (b'1', b'1'), 2)

    def test_prototype_islower(self):
        self.count_prototype_asserts(datatypes.bytes.islower(), (self.foo, self.foo), 2)

    def test_compound_islower(self):
        self.count_compound_asserts('bytes__islower', [], (self.foo, self.foo), 2)

    def test_prototype_isupper(self):
        self.count_prototype_asserts(datatypes.bytes.isupper(), (b'FOO', b'FOO'), 2)

    def test_compound_isupper(self):
        self.count_compound_asserts('bytes__isupper', [], (b'FOO', b'FOO'), 2)

    def test_prototype_isspace(self):
        self.count_prototype_asserts(datatypes.bytes.isspace(), (b'    ', b'    '), 2)

    def test_compound_isspace(self):
        self.count_compound_asserts('bytes__isspace', [], (b'    ', b'    '), 2)

    def test_prototype_istitle(self):
        self.count_prototype_asserts(datatypes.bytes.istitle(), (b'Foo', b'Foo'), 2)

    def test_compound_istitle(self):
        self.count_compound_asserts('bytes__istitle', [], (b'Foo', b'Foo'), 2)


class CountCommandBytearrayDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = bytearray(b'foo')

    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.bytearray.exact(self.foo), (self.foo, self.foo), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('bytearray__exact', [self.foo], (self.foo, self.foo), 2)

    def test_prototype_iexact(self):
        self.count_prototype_asserts(
            datatypes.bytearray.iexact(bytearray(b'FOO')),
            (self.foo, bytearray(b'fOo'), bytearray(b'Foo')), 3
        )

    def test_compound_iexact(self):
        self.count_compound_asserts(
            'bytearray__iexact', [bytearray(b'FOO')],
            (self.foo, bytearray(b'fOo'), bytearray(b'Foo')), 3
        )

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.bytearray.contains(bytearray(b'o')), (self.foo,), 1)

    def test_compound_contains(self):
        self.count_compound_asserts('bytearray__contains', [bytearray(b'o')], (self.foo,), 1)

    def test_prototype_icontains(self):
        self.count_prototype_asserts(datatypes.bytearray.icontains(bytearray(b'O')), (self.foo, bytearray(b'fOo')), 2)

    def test_compound_icontains(self):
        self.count_compound_asserts('bytearray__icontains', [bytearray(b'O')], (self.foo, bytearray(b'fOo')), 2)

    def test_prototype_startswith(self):
        self.count_prototype_asserts(datatypes.bytearray.startswith(bytearray(b'f')), (self.foo, self.foo), 2)

    def test_compound_startswith(self):
        self.count_compound_asserts('bytearray__startswith', [bytearray(b'f')], (self.foo, self.foo), 2)

    def test_prototype_istartswith(self):
        self.count_prototype_asserts(datatypes.bytearray.istartswith(bytearray(b'F')), (self.foo, bytearray(b'fOo')), 2)

    def test_compound_istartswith(self):
        self.count_compound_asserts('bytearray__istartswith', [bytearray(b'F')], (self.foo, bytearray(b'fOo')), 2)

    def test_prototype_endswith(self):
        self.count_prototype_asserts(datatypes.bytearray.endswith(bytearray(b'oo')), (self.foo, bytearray(b'bar')), 1)

    def test_compound_endswith(self):
        self.count_compound_asserts('bytearray__endswith', [bytearray(b'oo')], (self.foo, bytearray(b'bar')), 1)

    def test_prototype_iendswith(self):
        self.count_prototype_asserts(datatypes.bytearray.iendswith(bytearray(b'OO')), (self.foo, bytearray(b'fOo')), 2)

    def test_compound_iendswith(self):
        self.count_compound_asserts('bytearray__iendswith', [bytearray(b'OO')], (self.foo, bytearray(b'fOo')), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.bytearray.len(3), (self.foo, self.foo), 2)

    def test_compound_len(self):
        self.count_compound_asserts('bytearray__len', [3], (self.foo, self.foo), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.bytearray.lenlt(4), (self.foo, self.foo), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('bytearray__lenlt', [4], (self.foo, self.foo), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.bytearray.lenlte(3), (self.foo, self.foo), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('bytearray__lenlte', [3], (self.foo, self.foo), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.bytearray.lengt(2), (self.foo, self.foo), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('bytearray__lengt', [2], (self.foo, self.foo), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.bytearray.lengte(3), (self.foo, self.foo), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('bytearray__lengte', [3], (self.foo, self.foo), 2)

    def test_prototype_isalnum(self):
        self.count_prototype_asserts(datatypes.bytearray.isalnum(), (self.foo, self.foo), 2)

    def test_compound_isalnum(self):
        self.count_compound_asserts('bytearray__isalnum', [], (self.foo, self.foo), 2)

    def test_prototype_isalnums(self):
        self.count_prototype_asserts(datatypes.bytearray.isalnums(), (bytearray(b'fo o'), bytearray(b'f Oo')), 2)

    def test_compound_isalnums(self):
        self.count_compound_asserts('bytearray__isalnums', [], (bytearray(b'fo o'), bytearray(b'f Oo')), 2)

    def test_prototype_isalpha(self):
        self.count_prototype_asserts(datatypes.bytearray.isalpha(), (self.foo, self.foo), 2)

    def test_compound_isalpha(self):
        self.count_compound_asserts('bytearray__isalpha', [], (self.foo, self.foo), 2)

    def test_prototype_isalphas(self):
        self.count_prototype_asserts(datatypes.bytearray.isalphas(), (bytearray(b'fo o'), bytearray(b'f Oo')), 2)

    def test_compound_isalphas(self):
        self.count_compound_asserts('bytearray__isalphas', [], (bytearray(b'fo o'), bytearray(b'f Oo')), 2)

    def test_prototype_isdigit(self):
        self.count_prototype_asserts(datatypes.bytearray.isdigit(), (bytearray(b'1'), bytearray(b'1')), 2)

    def test_compound_isdigit(self):
        self.count_compound_asserts('bytearray__isdigit', [], (bytearray(b'1'), bytearray(b'1')), 2)

    def test_prototype_islower(self):
        self.count_prototype_asserts(datatypes.bytearray.islower(), (self.foo, self.foo), 2)

    def test_compound_islower(self):
        self.count_compound_asserts('bytearray__islower', [], (self.foo, self.foo), 2)

    def test_prototype_isupper(self):
        self.count_prototype_asserts(datatypes.bytearray.isupper(), (bytearray(b'FOO'), bytearray(b'FOO')), 2)

    def test_compound_isupper(self):
        self.count_compound_asserts('bytearray__isupper', [], (bytearray(b'FOO'), bytearray(b'FOO')), 2)

    def test_prototype_isspace(self):
        self.count_prototype_asserts(datatypes.bytearray.isspace(), (bytearray(b'    '), bytearray(b'    ')), 2)

    def test_compound_isspace(self):
        self.count_compound_asserts('bytearray__isspace', [], (bytearray(b'    '), bytearray(b'    ')), 2)

    def test_prototype_istitle(self):
        self.count_prototype_asserts(datatypes.bytearray.istitle(), (bytearray(b'Foo'), bytearray(b'Foo')), 2)

    def test_compound_istitle(self):
        self.count_compound_asserts('bytearray__istitle', [], (bytearray(b'Foo'), bytearray(b'Foo')), 2)


class CountCommandNumericDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.numeric.exact(5.5), (5.5, 5.5), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('numeric__exact', [5.5], (5.5, 5.5), 2)

    def test_prototype_gt(self):
        self.count_prototype_asserts(datatypes.numeric.gt(3), (4, 4), 2)

    def test_compound_gt(self):
        self.count_compound_asserts('numeric__gt', [3], (4, 4), 2)

    def test_prototype_gte(self):
        self.count_prototype_asserts(datatypes.numeric.gte(5), (5, 5), 2)

    def test_compound_gte(self):
        self.count_compound_asserts('numeric__gte', [5], (5, 5), 2)

    def test_prototype_lt(self):
        self.count_prototype_asserts(datatypes.numeric.lt(2), (1, 1), 2)

    def test_compound_lt(self):
        self.count_compound_asserts('numeric__lt', [2], (1, 1), 2)

    def test_prototype_lte(self):
        self.count_prototype_asserts(datatypes.numeric.lte(2), (2, 2), 2)

    def test_compound_lte(self):
        self.count_compound_asserts('numeric__lte', [2], (2, 2), 2)

    def test_prototype_between(self):
        self.count_prototype_asserts(datatypes.numeric.between(1, 2), (1, 1), 2)

    def test_compound_between(self):
        self.count_compound_asserts('numeric__between', [1, 2], (1, 1), 2)

    def test_prototype_ebetween(self):
        self.count_prototype_asserts(datatypes.numeric.ebetween(0, 2), (1, 1), 2)

    def test_compound_ebetween(self):
        self.count_compound_asserts('numeric__ebetween', [0, 2], (1, 1), 2)

    def test_prototype_isodd(self):
        self.count_prototype_asserts(datatypes.numeric.isodd(), (5, 5), 2)

    def test_compound_isodd(self):
        self.count_compound_asserts('numeric__isodd', [], (5, 5), 2)

    def test_prototype_iseven(self):
        self.count_prototype_asserts(datatypes.numeric.iseven(), (4, 4), 2)

    def test_compound_iseven(self):
        self.count_compound_asserts('numeric__iseven', [], (4, 4), 2)

    def test_prototype_divisibleby(self):
        self.count_prototype_asserts(datatypes.numeric.divisibleby(2), (4, 4), 2)

    def test_compound_divisibleby(self):
        self.count_compound_asserts('numeric__divisibleby', [2], (4, 4), 2)


class CountCommandIntDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.int.exact(5), (5, 5), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('int__exact', [5], (5, 5), 2)

    def test_prototype_gt(self):
        self.count_prototype_asserts(datatypes.int.gt(3), (4, 4), 2)

    def test_compound_gt(self):
        self.count_compound_asserts('int__gt', [3], (4, 4), 2)

    def test_prototype_gte(self):
        self.count_prototype_asserts(datatypes.int.gte(5), (5, 5), 2)

    def test_compound_gte(self):
        self.count_compound_asserts('int__gte', [5], (5, 5), 2)

    def test_prototype_lt(self):
        self.count_prototype_asserts(datatypes.int.lt(2), (1, 1), 2)

    def test_compound_lt(self):
        self.count_compound_asserts('int__lt', [2], (1, 1), 2)

    def test_prototype_lte(self):
        self.count_prototype_asserts(datatypes.int.lte(2), (2, 2), 2)

    def test_compound_lte(self):
        self.count_compound_asserts('int__lte', [2], (2, 2), 2)

    def test_prototype_between(self):
        self.count_prototype_asserts(datatypes.int.between(1, 2), (1, 1), 2)

    def test_compound_between(self):
        self.count_compound_asserts('int__between', [1, 2], (1, 1), 2)

    def test_prototype_ebetween(self):
        self.count_prototype_asserts(datatypes.int.ebetween(0, 2), (1, 1), 2)

    def test_compound_ebetween(self):
        self.count_compound_asserts('int__between', [0, 2], (1, 1), 2)

    def test_prototype_isodd(self):
        self.count_prototype_asserts(datatypes.int.isodd(), (5, 5), 2)

    def test_compound_isodd(self):
        self.count_compound_asserts('int__isodd', [], (5, 5), 2)

    def test_prototype_iseven(self):
        self.count_prototype_asserts(datatypes.int.iseven(), (4, 4), 2)

    def test_compound_iseven(self):
        self.count_compound_asserts('int__iseven', [], (4, 4), 2)

    def test_prototype_divisibleby(self):
        self.count_prototype_asserts(datatypes.int.divisibleby(2), (4, 4), 2)

    def test_compound_divisibleby(self):
        self.count_compound_asserts('int__divisibleby', [2], (4, 4), 2)


class CountCommandFloatDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.float.exact(5.5), (5.5, 5.5), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('float__exact', [5.5], (5.5, 5.5), 2)

    def test_prototype_gt(self):
        self.count_prototype_asserts(datatypes.float.gt(3), (4.2, 4.2), 2)

    def test_compound_gt(self):
        self.count_compound_asserts('float__gt', [3], (4.2, 4.2), 2)

    def test_prototype_gte(self):
        self.count_prototype_asserts(datatypes.float.gte(5), (5.5, 5.5), 2)

    def test_compound_gte(self):
        self.count_compound_asserts('float__gte', [5], (5.5, 5.5), 2)

    def test_prototype_lt(self):
        self.count_prototype_asserts(datatypes.float.lt(2), (1.1, 1.1), 2)

    def test_compound_lt(self):
        self.count_compound_asserts('float__lt', [2], (1.1, 1.1), 2)

    def test_prototype_lte(self):
        self.count_prototype_asserts(datatypes.float.lte(2), (1.8, 1.8), 2)

    def test_compound_lte(self):
        self.count_compound_asserts('float__lte', [2], (1.8, 1.8), 2)

    def test_prototype_between(self):
        self.count_prototype_asserts(datatypes.float.between(1, 2), (1.4, 1.4), 2)

    def test_compound_between(self):
        self.count_compound_asserts('float__between', [1, 2], (1.4, 1.4), 2)

    def test_prototype_ebetween(self):
        self.count_prototype_asserts(datatypes.float.ebetween(0, 2), (1.5, 1.5), 2)

    def test_compound_ebetween(self):
        self.count_compound_asserts('float__ebetween', [0, 2], (1.5, 1.5), 2)

    def test_prototype_isinteger(self):
        self.count_prototype_asserts(datatypes.float.isinteger(), (5.0, 5.0), 2)

    def test_compound_isinteger(self):
        self.count_compound_asserts('float__isinteger', [], (5.0, 5.0), 2)

    def test_prototype_isodd(self):
        self.count_prototype_asserts(datatypes.float.isodd(), (5.2, 5.2), 2)

    def test_compound_isodd(self):
        self.count_compound_asserts('float__isodd', [], (5.2, 5.2), 2)

    def test_prototype_iseven(self):
        self.count_prototype_asserts(datatypes.float.iseven(), (4.3, 4.3), 2)

    def test_compound_iseven(self):
        self.count_compound_asserts('float__iseven', [], (4.3, 4.3), 2)

    def test_prototype_divisibleby(self):
        self.count_prototype_asserts(datatypes.float.divisibleby(2), (4.7, 4.7), 2)

    def test_compound_divisibleby(self):
        self.count_compound_asserts('float__divisibleby', [2], (4.7, 4.7), 2)


class CountCommandLongDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.long.exact(2 ** 64), (2 ** 64, 2 ** 64), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('long__exact', [2 ** 64], (2 ** 64, 2 ** 64), 2)

    def test_prototype_gt(self):
        self.count_prototype_asserts(datatypes.long.gt(2 ** 63), (2 ** 64, 2 ** 64), 2)

    def test_compound_gt(self):
        self.count_compound_asserts('long__gt', [2 ** 63], (2 ** 64, 2 ** 64), 2)

    def test_prototype_gte(self):
        self.count_prototype_asserts(datatypes.long.gte(2 ** 64), (2 ** 65, 2 ** 65), 2)

    def test_compound_gte(self):
        self.count_compound_asserts('long__gte', [2 ** 64], (2 ** 65, 2 ** 65), 2)

    def test_prototype_lt(self):
        self.count_prototype_asserts(datatypes.long.lt(2 ** 64), (2 ** 63, 2 ** 63), 2)

    def test_compound_lt(self):
        self.count_compound_asserts('long__lt', [2 ** 64], (2 ** 63, 2 ** 63), 2)

    def test_prototype_lte(self):
        self.count_prototype_asserts(datatypes.long.lte(2 ** 64), (2 ** 63, 2 ** 63), 2)

    def test_compound_lte(self):
        self.count_compound_asserts('long__lte', [2 ** 64], (2 ** 63, 2 ** 63), 2)

    def test_prototype_between(self):
        self.count_prototype_asserts(datatypes.long.between(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64), 2)

    def test_compound_between(self):
        self.count_compound_asserts('long__between', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64), 2)

    def test_prototype_ebetween(self):
        self.count_prototype_asserts(datatypes.long.ebetween(2 ** 63, 2 ** 65), (2 ** 64, 2 ** 64), 2)

    def test_compound_ebetween(self):
        self.count_compound_asserts('long__ebetween', [2 ** 63, 2 ** 65], (2 ** 64, 2 ** 64), 2)

    def test_prototype_isodd(self):
        self.count_prototype_asserts(datatypes.long.isodd(), (3 ** 64, 3 ** 64), 2)

    def test_compound_isodd(self):
        self.count_compound_asserts('long__isodd', [], (3 ** 64, 3 ** 64), 2)

    def test_prototype_iseven(self):
        self.count_prototype_asserts(datatypes.long.iseven(), (2 ** 64, 2 ** 64), 2)

    def test_compound_iseven(self):
        self.count_compound_asserts('long__iseven', [], (2 ** 64, 2 ** 64), 2)

    def test_prototype_divisibleby(self):
        self.count_prototype_asserts(datatypes.long.divisibleby(2), (2 ** 64, 2 ** 64), 2)

    def test_compound_divisibleby(self):
        self.count_compound_asserts('long__divisibleby', [2], (2 ** 64, 2 ** 64), 2)


class CountCommandComplexDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.complex.exact(1j), (1j, 1j), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('complex__exact', [1j], (1j, 1j), 2)


class CountCommandIterableDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.iterable.exact(['foo']), (['foo'], ['foo']), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('iterable__exact', [['foo']], (['foo'], ['foo']), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.iterable.len(1), (['foo'], ['foo']), 2)

    def test_compound_len(self):
        self.count_compound_asserts('iterable__len', [1], (['foo'], ['foo']), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.iterable.lenlt(2), (['foo'], ['foo']), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('iterable__lenlt', [2], (['foo'], ['foo']), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.iterable.lenlte(1), (['foo'], ['foo']), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('iterable__lenlte', [1], (['foo'], ['foo']), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.iterable.lengt(0), (['foo'], ['foo']), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('iterable__lengt', [0], (['foo'], ['foo']), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.iterable.lengte(1), (['foo'], ['foo']), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('iterable__lengte', [1], (['foo'], ['foo']), 2)

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.iterable.contains('foo'), (['foo'], ('foo',)), 2)

    def test_compound_contains(self):
        self.count_compound_asserts('iterable__contains', ['foo'], (['foo'], ['foo']), 2)

    def test_prototype_contains_all(self):
        self.count_prototype_asserts(datatypes.iterable.contains_all(['f', 'o']), (['f', 'o'], ('f', 'o')), 2)

    def test_compound_contains_all(self):
        self.count_compound_asserts('iterable__contains_all', [['f', 'o']], (['f', 'o'], ('f', 'o')), 2)

    def test_prototype_contains_any(self):
        self.count_prototype_asserts(datatypes.iterable.contains_any(['f', 'z']), (['f', 'o'], ('f', 'o')), 2)

    def test_compound_contains_any(self):
        self.count_compound_asserts('iterable__contains_any', [['f', 'z']], (['f', 'o'], ('f', 'o')), 2)

    def test_prototype_str_contains_str(self):
        self.count_prototype_asserts(datatypes.iterable.str_contains_str('f'), (['fo'], ('fo',)), 2)

    def test_compound_str_contains_str(self):
        self.count_compound_asserts('iterable__str_contains_str', ['f'], (['fo'], ('fo',)), 2)


class CountCommandListDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.list.exact(['foo']), (['foo'], ['foo']), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('list__exact', [['foo']], (['foo'], ['foo']), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.list.len(1), (['foo'], ['foo']), 2)

    def test_compound_len(self):
        self.count_compound_asserts('list__len', [1], (['foo'], ['foo']), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.list.lenlt(2), (['foo'], ['foo']), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('list__lenlt', [2], (['foo'], ['foo']), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.list.lenlte(1), (['foo'], ['foo']), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('list__lenlte', [1], (['foo'], ['foo']), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.list.lengt(0), (['foo'], ['foo']), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('list__lengt', [0], (['foo'], ['foo']), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.list.lengte(1), (['foo'], ['foo']), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('list__lengte', [1], (['foo'], ['foo']), 2)

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.list.contains('foo'), (['foo'], ['foo']), 2)

    def test_compound_contains(self):
        self.count_compound_asserts('list__contains', ['foo'], (['foo'], ['foo']), 2)

    def test_prototype_contains_all(self):
        self.count_prototype_asserts(datatypes.list.contains_all(['f', 'o']), (['f', 'o'], ['f', 'o']), 2)

    def test_compound_contains_all(self):
        self.count_compound_asserts('list__contains_all', [['f', 'o']], (['f', 'o'], ['f', 'o']), 2)

    def test_prototype_contains_any(self):
        self.count_prototype_asserts(datatypes.list.contains_any(['f', 'z']), (['f', 'o'], ['f', 'o']), 2)

    def test_compound_contains_any(self):
        self.count_compound_asserts('list__contains_any', [['f', 'z']], (['f', 'o'], ['f', 'o']), 2)

    def test_prototype_str_contains_str(self):
        self.count_prototype_asserts(datatypes.list.str_contains_str('f'), (['fo'], ['fo']), 2)

    def test_compound_str_contains_str(self):
        self.count_compound_asserts('list__str_contains_str', ['f'], (['fo'], ['fo']), 2)


class CountCommandTupleDatatypeTestCase(AssertsCollection, unittest.TestCase):
    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.tuple.exact(('foo',)), (('foo',), ('foo',)), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('tuple__exact', [('foo',)], (('foo',), ('foo',)), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.tuple.len(1), (('foo',), ('foo',)), 2)

    def test_compound_len(self):
        self.count_compound_asserts('tuple__len', [1], (('foo',), ('foo',)), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.tuple.lenlt(2), (('foo',), ('foo',)), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('tuple__lenlt', [2], (('foo',), ('foo',)), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.tuple.lenlte(1), (('foo',), ('foo',)), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('tuple__lenlte', [1], (('foo',), ('foo',)), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.tuple.lengt(0), (('foo',), ('foo',)), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('tuple__lengt', [0], (('foo',), ('foo',)), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.tuple.lengte(1), (('foo',), ('foo',)), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('tuple__lengte', [1], (('foo',), ('foo',)), 2)

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.tuple.contains('foo'), (('foo',), ('foo',)), 2)

    def test_compound_contains(self):
        self.count_compound_asserts('tuple__contains', ['foo'], (('foo',), ('foo',)), 2)

    def test_prototype_contains_all(self):
        self.count_prototype_asserts(datatypes.tuple.contains_all(('f', 'o')), (('f', 'o'), ('f', 'o')), 2)

    def test_compound_contains_all(self):
        self.count_compound_asserts('tuple__contains_all', [('f', 'o')], (('f', 'o'), ('f', 'o')), 2)

    def test_prototype_contains_any(self):
        self.count_prototype_asserts(datatypes.tuple.contains_any(('f', 'z')), (('f', 'o'), ('f', 'o')), 2)

    def test_compound_contains_any(self):
        self.count_compound_asserts('tuple__contains_any', [('f', 'z')], (('f', 'o'), ('f', 'o')), 2)

    def test_prototype_str_contains_str(self):
        self.count_prototype_asserts(datatypes.tuple.str_contains_str('f'), (('fo',), ('fo',)), 2)

    def test_compound_str_contains_str(self):
        self.count_compound_asserts('tuple__str_contains_str', ['f'], (('fo',), ('fo',)), 2)


class CountCommandSetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = set(['foo'])

    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.set.exact(self.foo), (self.foo, self.foo), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('set__exact', [self.foo], (self.foo, self.foo), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.set.len(1), (self.foo, self.foo), 2)

    def test_compound_len(self):
        self.count_compound_asserts('set__len', [1], (self.foo, self.foo), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.set.lenlt(2), (self.foo, self.foo), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('set__lenlt', [2], (self.foo, self.foo), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.set.lenlte(1), (self.foo, self.foo), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('set__lenlte', [1], (self.foo, self.foo), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.set.lengt(0), (self.foo, self.foo), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('set__lengt', [0], (self.foo, self.foo), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.set.lengte(1), (self.foo, self.foo), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('set__lengte', [1], (self.foo, self.foo), 2)

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.set.contains('foo'), (self.foo, self.foo), 2)

    def test_compound_contains(self):
        self.count_compound_asserts('set__contains', ['foo'], (self.foo, self.foo), 2)

    def test_prototype_contains_all(self):
        self.count_prototype_asserts(datatypes.set.contains_all(['f', 'o']), (set(['f', 'o']), set(['f', 'o'])), 2)

    def test_compound_contains_all(self):
        self.count_compound_asserts('set__contains_all', [['f', 'o']], (set(['f', 'o']), set(['f', 'o'])), 2)

    def test_prototype_contains_any(self):
        self.count_prototype_asserts(datatypes.set.contains_any(['f', 'z']), (set(['f', 'o']), set(['f', 'o'])), 2)

    def test_compound_contains_any(self):
        self.count_compound_asserts('set__contains_any', [['f', 'z']], (set(['f', 'o']), set(['f', 'o'])), 2)

    def test_prototype_str_contains_str(self):
        self.count_prototype_asserts(datatypes.set.str_contains_str('f'), (set(['fo']), set(['fo'])), 2)

    def test_compound_str_contains_str(self):
        self.count_compound_asserts('set__str_contains_str', ['f'], (set(['fo']), set(['fo'])), 2)

    def test_prototype_isdisjoint(self):
        self.count_prototype_asserts(datatypes.set.isdisjoint(set(['bar'])), (self.foo, self.foo), 2)

    def test_compound_isdisjoint(self):
        self.count_compound_asserts('set__isdisjoint', [set(['bar'])], (self.foo, self.foo), 2)

    def test_prototype_issubset(self):
        self.count_prototype_asserts(datatypes.set.issubset(set(['foo'])), (self.foo, self.foo), 2)

    def test_compound_issubset(self):
        self.count_compound_asserts('set__issubset', [set(['foo'])], (self.foo, self.foo), 2)

    def test_prototype_eissubset(self):
        foo = set(['foo', 'bar'])
        self.count_prototype_asserts(datatypes.set.eissubset(foo), (self.foo, self.foo), 2)

    def test_compound_eissubset(self):
        self.count_compound_asserts('set__eissubset', [set(['foo', 'bar'])], (self.foo, self.foo), 2)

    def test_prototype_issuperset(self):
        self.count_prototype_asserts(datatypes.set.issuperset(set(['foo'])), (self.foo, self.foo), 2)

    def test_compound_issuperset(self):
        self.count_compound_asserts('set__issuperset', [set(['foo'])], (self.foo, self.foo), 2)

    def test_prototype_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.count_prototype_asserts(datatypes.set.eissuperset(set(['foo'])), (foo, foo), 2)

    def test_compound_eissuperset(self):
        foo = set(['foo', 'bar'])
        self.count_compound_asserts('set__eissuperset', [set(['foo'])], (foo, foo), 2)


class CountCommandFrozensetDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = frozenset(['foo'])

    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.frozenset.exact(self.foo), (self.foo, self.foo), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('frozenset__exact', [self.foo], (self.foo, self.foo), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.frozenset.len(1), (self.foo, self.foo), 2)

    def test_compound_len(self):
        self.count_compound_asserts('frozenset__len', [1], (self.foo, self.foo), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.frozenset.lenlt(2), (self.foo, self.foo), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('frozenset__lenlt', [2], (self.foo, self.foo), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.frozenset.lenlte(1), (self.foo, self.foo), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('frozenset__lenlte', [1], (self.foo, self.foo), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.frozenset.lengt(0), (self.foo, self.foo), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('frozenset__lengt', [0], (self.foo, self.foo), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.frozenset.lengte(1), (self.foo, self.foo), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('frozenset__lengte', [1], (self.foo, self.foo), 2)

    def test_prototype_contains(self):
        self.count_prototype_asserts(datatypes.frozenset.contains('foo'), (self.foo, self.foo), 2)

    def test_compound_contains(self):
        self.count_compound_asserts('frozenset__contains', ['foo'], (self.foo, self.foo), 2)

    def test_prototype_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.count_prototype_asserts(datatypes.frozenset.contains_all(['f', 'o']), (foo, foo), 2)

    def test_compound_contains_all(self):
        foo = frozenset(['f', 'o'])
        self.count_compound_asserts('frozenset__contains_all', [['f', 'o']], (foo, foo), 2)

    def test_prototype_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.count_prototype_asserts(datatypes.frozenset.contains_any(['f', 'z']), (foo, foo), 2)

    def test_compound_contains_any(self):
        foo = frozenset(['f', 'o'])
        self.count_compound_asserts('frozenset__contains_any', [['f', 'z']], (foo, foo), 2)

    def test_prototype_str_contains_str(self):
        foo = frozenset(['fo'])
        self.count_prototype_asserts(datatypes.frozenset.str_contains_str('f'), (foo, foo), 2)

    def test_compound_str_contains_str(self):
        foo = frozenset(['fo'])
        self.count_compound_asserts('frozenset__str_contains_str', ['f'], (foo, foo), 2)

    def test_prototype_isdisjoint(self):
        self.count_prototype_asserts(datatypes.frozenset.isdisjoint(frozenset(['bar'])), (self.foo, self.foo), 2)

    def test_compound_isdisjoint(self):
        self.count_compound_asserts('frozenset__isdisjoint', [frozenset(['bar'])], (self.foo, self.foo), 2)

    def test_prototype_issubset(self):
        self.count_prototype_asserts(datatypes.frozenset.issubset(frozenset(['foo'])), (self.foo, self.foo), 2)

    def test_compound_issubset(self):
        self.count_compound_asserts('frozenset__issubset', [frozenset(['foo'])], (self.foo, self.foo), 2)

    def test_prototype_eissubset(self):
        foo = frozenset(['foo', 'bar'])
        self.count_prototype_asserts(datatypes.frozenset.eissubset(foo), (self.foo, self.foo), 2)

    def test_compound_eissubset(self):
        self.count_compound_asserts('frozenset__eissubset', [frozenset(['foo', 'bar'])], (self.foo, self.foo), 2)

    def test_prototype_issuperset(self):
        self.count_prototype_asserts(datatypes.frozenset.issuperset(frozenset(['foo'])), (self.foo, self.foo), 2)

    def test_compound_issuperset(self):
        self.count_compound_asserts('frozenset__issuperset', [frozenset(['foo'])], (self.foo, self.foo), 2)

    def test_prototype_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.count_prototype_asserts(datatypes.frozenset.eissuperset(frozenset(['foo'])), (foo, foo), 2)

    def test_compound_eissuperset(self):
        foo = frozenset(['foo', 'bar'])
        self.count_compound_asserts('frozenset__eissuperset', [frozenset(['foo'])], (foo, foo), 2)


class CountCommandDictDatatypeTestCase(AssertsCollection, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.foo = {'foo': 'bar'}

    def test_prototype_exact(self):
        self.count_prototype_asserts(datatypes.dict.exact(self.foo), (self.foo, self.foo), 2)

    def test_compound_exact(self):
        self.count_compound_asserts('dict__exact', [self.foo], (self.foo, self.foo), 2)

    def test_prototype_len(self):
        self.count_prototype_asserts(datatypes.dict.len(1), (self.foo, self.foo), 2)

    def test_compound_len(self):
        self.count_compound_asserts('dict__len', [1], (self.foo, self.foo), 2)

    def test_prototype_lenlt(self):
        self.count_prototype_asserts(datatypes.dict.lenlt(2), (self.foo, self.foo), 2)

    def test_compound_lenlt(self):
        self.count_compound_asserts('dict__lenlt', [2], (self.foo, self.foo), 2)

    def test_prototype_lenlte(self):
        self.count_prototype_asserts(datatypes.dict.lenlte(1), (self.foo, self.foo), 2)

    def test_compound_lenlte(self):
        self.count_compound_asserts('dict__lenlte', [1], (self.foo, self.foo), 2)

    def test_prototype_lengt(self):
        self.count_prototype_asserts(datatypes.dict.lengt(0), (self.foo, self.foo), 2)

    def test_compound_lengt(self):
        self.count_compound_asserts('dict__lengt', [0], (self.foo, self.foo), 2)

    def test_prototype_lengte(self):
        self.count_prototype_asserts(datatypes.dict.lengte(1), (self.foo, self.foo), 2)

    def test_compound_lengte(self):
        self.count_compound_asserts('dict__lengte', [1], (self.foo, self.foo), 2)

    def test_prototype_contains_key(self):
        self.count_prototype_asserts(datatypes.dict.contains_key('foo'), (self.foo, self.foo), 2)

    def test_compound_contains_key(self):
        self.count_compound_asserts('dict__contains_key', ['foo'], (self.foo, self.foo), 2)

    def test_prototype_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.count_prototype_asserts(datatypes.dict.contains_all_keys(['foo', 'bar']), (foo, foo), 2)

    def test_compound_contains_all_keys(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.count_compound_asserts('dict__contains_all_keys', [['foo', 'bar']], (foo, foo), 2)

    def test_prototype_contains_any_keys(self):
        self.count_prototype_asserts(datatypes.dict.contains_any_keys(['foo', 'z']), (self.foo, self.foo), 2)

    def test_compound_contains_any_keys(self):
        self.count_compound_asserts('dict__contains_any_keys', [['foo', 'z']], (self.foo, self.foo), 2)

    def test_prototype_key_contains_str(self):
        self.count_prototype_asserts(datatypes.dict.key_contains_str('f'), (self.foo, self.foo), 2)

    def test_compound_key_contains_str(self):
        self.count_compound_asserts('dict__key_contains_str', ['f'], (self.foo, self.foo), 2)

    def test_prototype_contains_value(self):
        self.count_prototype_asserts(datatypes.dict.contains_value('bar'), (self.foo, self.foo), 2)

    def test_compound_contains_value(self):
        self.count_compound_asserts('dict__contains_value', ['bar'], (self.foo, self.foo), 2)

    def test_prototype_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.count_prototype_asserts(datatypes.dict.contains_all_values(['baz', 'bar']), (foo, foo), 2)

    def test_compound_contains_all_values(self):
        foo = {'foo': 'bar', 'bar': 'baz'}
        self.count_compound_asserts('dict__contains_all_values', [['baz', 'bar']], (foo, foo), 2)

    def test_prototype_contains_any_values(self):
        self.count_prototype_asserts(datatypes.dict.contains_any_values(['bar', 'z']), (self.foo, self.foo), 2)

    def test_compound_contains_any_values(self):
        self.count_compound_asserts('dict__contains_any_values', [['bar', 'z']], (self.foo, self.foo), 2)

    def test_prototype_value_contains_str(self):
        self.count_prototype_asserts(datatypes.dict.value_contains_str('b'), (self.foo, self.foo), 2)

    def test_compound_value_contains_str(self):
        self.count_compound_asserts('dict__value_contains_str', ['b'], (self.foo, self.foo), 2)
