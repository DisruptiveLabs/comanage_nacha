from comanage_nacha.enums import ServiceClassCodes
from comanage_nacha.exceptions import EntryClosedError
from .entry import Entry
from .entries import CompanyBatchHeader, CompanyBatchControl


class Batch(object):
    """
    @type entries: list[Entry]
    """

    def __init__(self, batch_number, batch_header=None, **kwargs):
        self.batch_number = batch_number
        self.batch_header = batch_header or CompanyBatchHeader(batch_number=batch_number, **kwargs)
        self.batch_control = None
        self.entries = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def add_entry(self, **kwargs):
        if self.batch_control is not None:
            raise EntryClosedError("This batch has already been closed")
        kwargs.setdefault('error_code', self.batch_header.error_code)
        kwargs.setdefault('trace_number', self.entry_count + 1)
        entry = Entry(**kwargs)
        self.entries.append(entry)
        return entry

    @property
    def error_code(self):
        return self.batch_header.error_code

    @error_code.setter
    def error_code(self, value):
        self.set_error_code(value)

    def set_error_code(self, error_code):
        self.batch_header.error_code = error_code
        for entry in self.entries:
            entry.set_error_code(error_code)

    @property
    def entry_hash(self):
        return str(sum(int(entry.entry_detail.receiving_dfi_routing_number) for entry in self.entries))[-10:]

    def calculate_total_batch_debit_entry(self):
        return sum(entry.entry_detail.amount for entry in self.entries if entry.is_debit)

    def calculate_total_batch_credit_entry(self):
        return sum(entry.entry_detail.amount for entry in self.entries if entry.is_credit)

    def close(self):
        if not self.batch_header.service_class_code:
            is_credit = any(entry.is_credit for entry in self.entries)
            is_debit = any(entry.is_debit for entry in self.entries)
            if is_credit and is_debit:
                self.batch_header.service_class_code = ServiceClassCodes.MIXED_DEBITS_CREDITS
            elif is_credit:
                self.batch_header.service_class_code = ServiceClassCodes.CREDITS
            elif is_debit:
                self.batch_header.service_class_code = ServiceClassCodes.DEBITS

        self.batch_control = CompanyBatchControl(
            service_class_code=self.batch_header.service_class_code,
            entry_addenda_count=sum(1 + entry.addenda_count for entry in self.entries),
            entry_hash=self.entry_hash,
            total_batch_debit_entry_dollar_amount=self.calculate_total_batch_debit_entry(),
            total_batch_credit_entry_dollar_amount=self.calculate_total_batch_credit_entry(),
            company_id=self.batch_header.company_id,
            wells_fargo_routing_number='09100001',
            batch_number=self.batch_number,
            error_code=self.batch_header.error_code,
        )

    @property
    def entry_count(self):
        return len(self.entries)

    @property
    def lines(self):
        yield self.batch_header
        for entry in self.entries:
            for line in entry.lines:
                yield line
        yield self.batch_control
