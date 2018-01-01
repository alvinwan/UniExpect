def split(string, divider):
    """Splits a string according at the first instance of a divider."""
    pieces = string.split(divider)
    return [pieces[0].strip(), divider.join(pieces[1:])]
