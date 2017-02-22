from comanage_nacha.enums import TransactionCodes
from .addenda import Addenda
from .entries import EntryDetail


class Entry(object):
    """
    A high-level representation of a NACHA entry and its addenda

    @type addenda: list[Addenda]
    """

    def __init__(self, trace_number, entry_detail=None, **kwargs):
        self.entry_detail = entry_detail or EntryDetail(trace_number=trace_number, **kwargs)
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

    @property
    def error_code(self):
        return self.entry_detail.error_code

    @error_code.setter
    def error_code(self, value):
        self.set_error_code(value)

    def set_error_code(self, error_code):
        self.entry_detail.error_code = error_code
        for addenda in self.addenda:
            addenda.set_error_code(error_code)

    @property
    def is_credit(self):
        return self.entry_detail.transaction_code in (TransactionCodes.CHECKING_CREDIT,
                                                      TransactionCodes.SAVINGS_CREDIT,
                                                      TransactionCodes.CHECKING_PRE_NOTE_CREDIT,
                                                      TransactionCodes.SAVINGS_PRE_NOTE_CREDIT)

    @property
    def is_debit(self):
        return self.entry_detail.transaction_code in (TransactionCodes.CHECKING_DEBIT,
                                                      TransactionCodes.SAVINGS_DEBIT,
                                                      TransactionCodes.CHECKING_PRE_NOTE_DEBIT,
                                                      TransactionCodes.SAVINGS_PRE_NOTE_DEBIT)

    @property
    def addenda_count(self):
        return len(self.addenda)

    @property
    def lines(self):
        yield self.entry_detail
        for addenda in self.addenda:
            yield addenda.entry_addenda
