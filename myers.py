#!/usr/bin/env python3
"""
Myers diff of two lists

Inspired by
https://gist.github.com/adamnew123456/37923cf53f51d6b9af32a539cdfa7cc4
"""
KEEP, INSERT, REMOVE, OMIT = range(4)

__version__ = '0.9.0'
__all__ = ('myers',)

_DEFAULT_FORMATS = {
    KEEP: ' %s',
    INSERT: '+%s',
    REMOVE: '-%s',
    OMIT: '(...%s removed...)',
}


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

    def omit():
        omitted = len(queue) - context
        if omitted > 0:
            yield OMIT, str(omitted)

    for line in diff:
        if line[0] is KEEP:
            queue.append(line)
        else:
            if queue:
                yield from omit()
                if context > 0:
                    yield from queue[-context:]
                queue.clear()
            yield line

    if queue:
        yield from queue[:context]
        yield from omit()


def myers(a, b, context=None, format=False):
    diff = _myers(a, b)

    if context is not None:
        diff = list(_compact(diff, context))

    if format:
        fmt = dict(_DEFAULT_FORMATS)
        if format is not True:
            fmt.update(format)

        diff = [(fmt[d] % e).rstrip() for d, e in diff]

    return diff
