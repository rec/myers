#!/usr/bin/env python
"""
Myers diff of two lists or files

Inspired by
https://gist.github.com/adamnew123456/37923cf53f51d6b9af32a539cdfa7cc4
"""
from __future__ import print_function
import argparse

KEEP, INSERT, REMOVE, OMIT = 'kiro'

__version__ = '0.9.2'
__all__ = ('diff',)

_DEFAULT_FORMATS = {
    KEEP: ' %s',
    INSERT: '+%s',
    REMOVE: '-%s',
    OMIT: '(...%s skipped...)',
}


def diff(a, b, context=None, format=None):
    """
    Return the Myers diff of two lists.

    The result is a list of (action, line) pairs,
    where ``action`` is one of ``'kiro'``, for keep,
    insert, remove, or omit.

    ARGUMENTS:
       a, b:
         The two files to compare

       context:
         How many lines of context to keep between blocks of changes?
         ``None``, the default, means keep all unchanged lines.
         ``0`` means throw away all the unchanged lines

       format: if a dictionary, it is used to format
         each diff entry.  If true, the default dictionary above is
         used to format the diff entries.  Otherwise they are returned as-is.

    """
    diff = _myers(a, b)

    if context is not None:
        diff = list(_compact(diff, context))

    if format:
        fmt = dict(_DEFAULT_FORMATS)
        if format is not True:
            fmt.update(format)

        diff = [(fmt[d] % e).rstrip() for d, e in diff]

    return diff


def _myers(a, b):
    front = {1: (0, [])}

    for d in range(0, len(a) + len(b) + 1):
        for k in range(-d, d + 1, 2):
            go_down = k == -d or (k != d and front[k - 1][0] < front[k + 1][0])

            if go_down:
                old_x, history = front[k + 1]
                x = old_x
            else:
                old_x, history = front[k - 1]
                x = old_x + 1
            y = x - k

            history = history[:]

            if 1 <= y <= len(b) and go_down:
                history.append((INSERT, b[y - 1]))
            elif 1 <= x <= len(a):
                history.append((REMOVE, a[x - 1]))

            while x < len(a) and y < len(b) and a[x] == b[y]:
                x += 1
                y += 1
                history.append((KEEP, a[x - 1]))

            if x >= len(a) and y >= len(b):
                return history

            front[k] = x, history

    # TODO: is this possible to reach?
    raise ValueError('Unable to compute diff')


def _compact(diff, context):
    queue = []
    results = []

    def omit():
        omitted = len(queue) - context
        if omitted > 0:
            results.append((OMIT, str(omitted)))

    for line in diff:
        if line[0] is KEEP:
            queue.append(line)
        else:
            if queue:
                omit()
                if context > 0:
                    results.extend(queue[-context:])
                queue[:] = []
            results.append(line)

    if queue:
        results.extend(queue[:context])
        omit()

    return results


def _parse_args(args=None):
    p = argparse.ArgumentParser(description=_DESCRIPTION)

    p.add_argument('file_a', help=_FILE_A_HELP)
    p.add_argument('file_b', help=_FILE_B_HELP)
    p.add_argument('--context', '-c', default=None, help=_CONTEXT_HELP)

    return p.parse_args(args)


_DESCRIPTION = 'Print a Myers diff between two text files'

_CONTEXT_HELP = """If set, print only this many lines of context around
each actual diff.  If not set, print the entire diff, which includes the full
text of both files."""

_FILE_A_HELP = """File A - the file to be compared from"""
_FILE_B_HELP = """File B - the file to be compared to"""


def _main(args=None, format=True, print=print):
    args = _parse_args(args)
    with open(args.file_a) as a, open(args.file_b) as b:
        for line in diff(list(a), list(b), args.context, format):
            print(line)


if __name__ == '__main__':
    _main()
