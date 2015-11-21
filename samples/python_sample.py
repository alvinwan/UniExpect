"""
Expect Utility
--------------

Regardless of comment type, all tests in this file will be detected. We will
demonstrate that expect can handle several edge cases, accommodate regular
doctest formats, and detect inline tests.

>>> x = 4

>>> x
4
>>> 3+5 # comments
8
>>> 6+x  # wrong!
5
>>> is_proper('()')
True
"""

# > () + () => ()
# > [] + [] => []

def is_proper(str):
    """Tests if a set of parentheses are properly closed.

    >>> is_proper('()(())')  # regular doctests
    True
    >>> is_proper('(()()')  # too many open parens
    False
    >>> is_proper('())')  # too many close parens
    False
    >>> is_proper('())(')  # parens don't match
    False
    """
    try:
        parens = []
        for c in str:
            if c == '(':
                parens.append(c)  # > [1, 2, 3].pop() => 3  # also a test!
            else:
                parens.pop()  # > [1, 2, 3].pop(0) => 3  # wrong!
        return len(parens) == 0
    except IndexError:
        return False
