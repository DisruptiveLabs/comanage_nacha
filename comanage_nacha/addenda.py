from .entries import EntryAddenda


class Addenda(object):
    def __init__(self, **kwargs):
        self.entry_addenda = EntryAddenda(**kwargs)

    def set_error_code(self, error_code):
        self.entry_addenda.error_code = error_code

    def lines(self):
        yield self.entry_addenda