from unittest import TestCase
import myers


class TestDiff(TestCase):
    def test_diff(self):
        actual = myers.myers(INPUT, OUTPUT, format=True)
        assert actual == DIFF

    def test_compact0(self):
        actual = myers.myers(INPUT, OUTPUT, context=0, format=True)
        assert actual == DIFF_COMPACT_0

    def test_compact1(self):
        actual = myers.myers(INPUT, OUTPUT, context=1, format=True)
        print('-' * 80)
        print(*actual, sep='\n')
        print('-' * 80)

        assert actual == DIFF_COMPACT_1

    def test_compact3(self):
        actual = myers.myers(INPUT, OUTPUT, context=3, format=True)
        print('-' * 80)
        print(*actual, sep='\n')
        print('-' * 80)

        assert actual == DIFF_COMPACT_3


INPUT = """\
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

OUTPUT = """\
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
(...3 removed...)
-from a import b
-import foo
(...2 removed...)
+from a import b
(...1 removed...)
+import foo
(...5 removed...)
""".splitlines()

DIFF_COMPACT_1 = """\
(...2 removed...)

-from a import b
-import foo
(...1 removed...)

+from a import b
 from d import f
+import foo
 import foo.bar
(...4 removed...)
""".splitlines()

DIFF_COMPACT_3 = (
    DIFF[:-2]
    + """\
(...2 removed...)
""".splitlines()
)
