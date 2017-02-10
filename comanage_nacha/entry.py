from comanage_nacha.entries import EntryDetail, EntryAddenda


class Entry(object):
    """A high-level representation of a NACHA entry and its addenda"""

    def __init__(self, trace_number, **kwargs):
        self.entry_detail = EntryDetail(trace_number=trace_number, **kwargs)
        self.addenda = []

    def add_addenda(self, **kwargs):
        addenda = EntryAddenda(self.entry_detail.trace_number, **kwargs)
        self.entry_detail.addenda_record_indicator = 1
        self.addenda.append(addenda)
        return addenda

    @property
    def is_credit(self):
        return self.entry_detail.transaction_code in ('22', '23', '32', '33')

    @property
    def is_debit(self):
        return self.entry_detail.transaction_code in ('27', '28', '37', '38')

    @property
    def addenda_count(self):
        return len(self.addenda)

    @property
    def lines(self):
        yield self.entry_detail
        for addenda in self.addenda:
            yield addenda
