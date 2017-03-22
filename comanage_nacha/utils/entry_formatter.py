import string


class EntryFormatter(string.Formatter):
    def _get_len_from_format_spec(self, format_spec):
        toks = list(reversed(format_spec))
        while toks:
            c, toks = toks[0], toks[1:]
            if not toks or str.isalpha(c) and str.isdigit(toks[0]):
                break
        else:
            return None

        digits = ''
        while toks:
            c, toks = toks[0], toks[1:]
            digits = c + digits
            if not toks or not str.isdigit(toks[0]):
                break

        if digits:
            return int(digits)

    def format_field(self, value, format_spec):
        formatted = super(EntryFormatter, self).format_field(value, format_spec)
        maxlen = self._get_len_from_format_spec(format_spec)
        if maxlen and len(formatted) > maxlen:
            return formatted[:maxlen]
        return formatted

    def convert_field(self, value, conversion):
        if conversion == 'd':
            return int(value)
        if value is None and conversion == 's':
            return ''
        return super(EntryFormatter, self).convert_field(value, conversion)
