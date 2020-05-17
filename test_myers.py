from unittest import TestCase
import myers


def diff(a, b):
    diff = myers.myers(a, b)
    return [(a + b).rstrip() for (a, b) in diff]


class TestDiff(TestCase):
    def test_diff(self):
        actual = diff(INPUT.splitlines(), OUTPUT.splitlines())
        expected = DIFF.splitlines()
        assert actual == expected

    def DONT_test_short_diff(self):
        actual = diff(INPUT.splitlines(), OUTPUT.splitlines(), 3)
        expected = SHORT_DIFF.splitlines()
        print(*actual, sep='\n')
        assert actual == expected


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
"""

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
"""

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
"""

SHORT_DIFF = """\
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
[...2 lines skipped...]
"""
