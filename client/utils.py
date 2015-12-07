def map_break(items, condition, f):
    """Calls function f on the item where a condition is satisfied"""
    for item in items:
        if condition(item):
            f(item)
            break

def split(string, divider):
    """Splits a string according at the first instance of a divider."""
    pieces = string.split(divider)
    return [pieces[0].strip(), divider.join(pieces[1:])]
