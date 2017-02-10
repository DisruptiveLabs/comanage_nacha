from .entry import Entry
from .entries import CompanyBatchHeader, CompanyBatchControl


class Batch:
    def __init__(self, batch_number, **kwargs):
        self.batch_header = CompanyBatchHeader(batch_number=batch_number, **kwargs)
        self.batch_number = 0
        self.entries = []

    def add_entry(self, **kwargs):
        kwargs.setdefault('error_code', self.batch_header.error_code)
        entry = Entry(self.entry_count + 1, **kwargs)
        self.entries.append(entry)
        return entry

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

    @property
    def batch_control(self):
        return CompanyBatchControl(
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
