from .addenda import Addenda
from .entries import EntryDetail


class Entry(object):
    """A high-level representation of a NACHA entry and its addenda"""

    def __init__(self, trace_number, **kwargs):
        self.entry_detail = EntryDetail(trace_number=trace_number, **kwargs)
        self.addenda = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_addenda(self, **kwargs):
        kwargs.setdefault('entry_detail_sequence_number', self.entry_detail.trace_number)
        kwargs.setdefault('error_code', self.entry_detail.error_code)
        addenda = Addenda(**kwargs)
        self.entry_detail.addenda_record_indicator = 1
        self.addenda.append(addenda)
        return addenda

    def set_error_code(self, error_code):
        self.entry_detail.error_code = error_code
        for addenda in self.addenda:
            addenda.set_error_code(error_code)

    @property
    def is_credit(self):
        return self.entry_detail.transaction_code in (22, 23, 32, 33)

    @property
    def is_debit(self):
        return self.entry_detail.transaction_code in (27, 28, 37, 38)

    @property
    def addenda_count(self):
        return len(self.addenda)

    @property
    def lines(self):
        yield self.entry_detail
        for addenda in self.addenda:
            yield addenda.entry_addenda
