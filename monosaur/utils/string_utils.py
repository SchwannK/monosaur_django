# returns empty string for a null, None or empty/blank string
# otherwise it returns the string itself
def to_empty(string):
    if string and string.strip():
        #myString is not None AND myString is not empty or blank
        return string
    #myString is None OR myString is empty or blank
    return ""