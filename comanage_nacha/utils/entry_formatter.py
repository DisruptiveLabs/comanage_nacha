import string


class EntryFormatter(string.Formatter):
    def convert_field(self, value, conversion):
        if conversion == 'd':
            return int(value)
        return super(EntryFormatter, self).convert_field(value, conversion)
