# returns empty string for a null, None or empty/blank string
# otherwise it returns the string itself
def to_empty(string):
    if is_empty(string):
        # myString is not None AND myString is not empty or blank
        return ""
    # myString is None or empty or blank
    return string

def to_none(string):
    if is_empty(string):
        # myString is not None AND myString is not empty or blank
        return None
    # myString is None or empty or blank
    return string

def is_empty(string):
    if string is not None and string and string.strip():
        return False
    else:
        return True