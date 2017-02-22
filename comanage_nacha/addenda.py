from .entries import addenda_types


class Addenda(object):
    def __init__(self, entry_addenda=None, **kwargs):
        self.entry_addenda = entry_addenda or addenda_types[kwargs.pop('addenda_type_code', 5)](**kwargs)

    @property
    def error_code(self):
        return self.entry_addenda.error_code

    @error_code.setter
    def error_code(self, value):
        self.set_error_code(value)

    def set_error_code(self, error_code):
        self.entry_addenda.error_code = error_code
