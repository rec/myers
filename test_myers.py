from __future__ import print_function
from tempfile import NamedTemporaryFile
from unittest import TestCase
import functools
import myers

diff = functools.partial(myers.diff, format=True)


class TestDiff(TestCase):
    def test_diff(self):
        actual = diff(FILE_A, FILE_B)
        assert actual == DIFF

    def test_compact0(self):
        actual = diff(FILE_A, FILE_B, context=0)
        assert actual == DIFF_COMPACT_0

    def test_compact1(self):
        actual = diff(FILE_A, FILE_B, context=1)
        assert actual == DIFF_COMPACT_1

    def test_compact3(self):
        actual = diff(FILE_A, FILE_B, context=3)
        assert actual == DIFF_COMPACT_3

    def test_empty0(self):
        actual = diff([], [])
        expected = []
        assert actual == expected

    def test_empty1(self):
        actual = diff(FILE_A, [])
        expected = ['-' + i for i in FILE_A]
        assert actual == expected

    def test_empty2(self):
        actual = diff([], FILE_A)
        expected = ['+' + i for i in FILE_A]
        assert actual == expected

    def test_reverse(self):
        n = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
        actual = diff(n, n[::-1])
        last = n.pop()
        minus = ['-' + i for i in n]
        plus = ['+' + i for i in n[::-1]]
        expected = minus + [' ' + last] + plus

        assert actual == expected

    def test_main(self):
        results = []
        with NamedTemporaryFile('w+') as a, NamedTemporaryFile('w+') as b:
            a.writelines(i + '\n' for i in FILE_A)
            b.writelines(i + '\n' for i in FILE_B)
            a.flush()
            b.flush()
            myers._main([a.name, b.name], print=results.append)

        assert results == DIFF


FILE_A = """\
# something
# something else

from a import b
import foo
# comment goes ABOVE

from d import f
import foo.bar

# comment goes BELOW

END = 'here'
""".splitlines()

FILE_B = """\
# something
# something else

# comment goes ABOVE

from a import b
from d import f
import foo
import foo.bar

# comment goes BELOW

END = 'here'
""".splitlines()

DIFF = """\
 # something
 # something else

-from a import b
-import foo
 # comment goes ABOVE

+from a import b
 from d import f
+import foo
 import foo.bar

 # comment goes BELOW

 END = 'here'
""".splitlines()

DIFF_COMPACT_0 = """\
(...3 skipped...)
-from a import b
-import foo
(...2 skipped...)
+from a import b
(...1 skipped...)
+import foo
(...5 skipped...)
""".splitlines()

DIFF_COMPACT_1 = """\
(...2 skipped...)

-from a import b
-import foo
(...1 skipped...)

+from a import b
 from d import f
+import foo
 import foo.bar
(...4 skipped...)
""".splitlines()

DIFF_COMPACT_3 = (
    DIFF[:-2]
    + """\
(...2 skipped...)
""".splitlines()
)
