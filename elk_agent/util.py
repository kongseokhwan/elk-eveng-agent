__author__ = 'kongseokhwan'


def diff(a, b, callback):
    a_missing_in_b = []
    b_missing_in_a = []
    ai = 0
    bi = 0

    a = sorted(a, callback)
    b = sorted(b, callback)

    while (ai < len(a)) and (bi < len(b)):
        cmp = callback(a[ai], b[bi])
        if cmp < 0:
            a_missing_in_b.append(a[ai])
            ai += 1
        elif cmp > 0:
            # Item b is missing in a
            b_missing_in_a.append(b[bi])
            bi += 1
        else:
            # a and b intersecting on this item
            ai += 1
            bi += 1

    # if a and b are not of same length, we need to add the remaining items
    for ai in xrange(ai, len(a)):
        a_missing_in_b.append(a[ai])

    for bi in xrange(bi, len(b)):
        b_missing_in_a.append(b[bi])

    return {'removed':a_missing_in_b, 'added':b_missing_in_a}

