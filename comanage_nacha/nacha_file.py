from .batch import Batch
from .entries import FileHeader, FileControl


class NachaFile:
    def __init__(self, file_header=None, **kwargs):
        self.file_header = file_header or FileHeader(**kwargs)
        self.batches = []

    def add_batch(self, **kwargs):
        kwargs.setdefault('error_code', self.file_header.error_code)
        batch = Batch(self.batch_count + 1, **kwargs)
        self.batches.append(batch)
        return batch

    def set_error_code(self, error_code):
        self.file_header.error_code = error_code
        for batch in self.batches:
            batch.set_error_code(error_code)

    def calculate_entry_addenda_record_count(self):
        return sum(batch.entry_count + sum(entry.addenda_count for entry in batch.entries)
                   for batch in self.batches)

    def calculate_block_count(self):
        return (
            1 +  # File Header
            len(self.batches) * 2 +  # Batch Headers and Controls
            self.calculate_entry_addenda_record_count() +
            1  # File Control
        )

    @property
    def batch_count(self):
        return len(self.batches)

    @property
    def file_control(self):
        return FileControl(
            batch_count=len(self.batches),
            block_count=self.calculate_block_count(),
            entry_addenda_record_count=self.calculate_entry_addenda_record_count(),
            entry_hash_total=str(sum(int(batch.entry_hash) for batch in self.batches))[-10:],
            total_file_debit_entry_amount=sum(batch.calculate_total_batch_debit_entry() for batch in self.batches),
            total_file_credit_entry_amount=sum(batch.calculate_total_batch_credit_entry() for batch in self.batches),
        )

    @property
    def lines(self):
        yield self.file_header
        for batch in self.batches:
            for line in batch.lines:
                yield line
        yield self.file_control
