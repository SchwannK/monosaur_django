# returns empty string for a null, None or empty/blank string
# otherwise it returns the string itself
def to_empty(string):
    if is_empty(string):
        # myString is not None AND myString is not empty or blank
        return string
    # myString is None or empty or blank
    return ""

def is_empty(string):
    if string and string.strip() and string is not None:
        return True
    else:
        return False
