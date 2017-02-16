import string


class EntryFormatter(string.Formatter):

    def format_field(self, value, format_spec):
        return super(EntryFormatter, self).format_field(value, format_spec)

    def convert_field(self, value, conversion):
        if conversion == 'd':
            return int(value)
        if value is None and conversion == 's':
            return ''
        return super(EntryFormatter, self).convert_field(value, conversion)
