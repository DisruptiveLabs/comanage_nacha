import string


class EntryFormatter(string.Formatter):
    def convert_field(self, value, conversion):
        # do any conversion on the resulting object
        if conversion is None:
            return value
        elif conversion == 'd':
            return int(value)
        elif conversion == 's':
            return str(value)
        raise ValueError("Unknown conversion specifier {0!s}".format(conversion))
