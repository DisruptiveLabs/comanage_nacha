import datetime
import math

from comanage_nacha.exceptions import EntryClosedError
from .batch import Batch
from .entries import BlockingFileControl, FileHeader, FileControl


class NachaFile(object):
    """
    @type batches: list[Batch]
    @type file_header: FileHeader
    @type file_control: FileControl
    """

    def __init__(self, file_header=None, file_control=None, batches=None, include_blocking_lines=True, **kwargs):
        kwargs.setdefault('file_creation_date', datetime.date.today())
        kwargs.setdefault('file_creation_time', datetime.datetime.utcnow().time())
        self.include_blocking_lines = include_blocking_lines
        self.file_header = file_header or FileHeader(**kwargs)  # type: FileHeader
        self.file_control = file_control  # type: FileControl
        self.batches = batches or []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def add_batch(self, **kwargs):
        if self.file_control is not None:
            raise EntryClosedError("This file has already been closed")
        kwargs.setdefault('error_code', self.file_header.error_code)
        batch = Batch(self.batch_count + 1, **kwargs)
        self.batches.append(batch)
        return batch

    @property
    def error_code(self):
        return self.file_header.error_code

    @error_code.setter
    def error_code(self, value):
        self.set_error_code(value)

    def set_error_code(self, error_code):
        self.file_header.error_code = error_code
        for batch in self.batches:
            batch.set_error_code(error_code)

    def calculate_entry_addenda_record_count(self):
        return sum(batch.entry_count + sum(entry.addenda_count for entry in batch.entries)
                   for batch in self.batches)

    def calculate_block_count(self):
        return int(math.ceil((
                                 1 +  # File Header
                                 len(self.batches) * 2 +  # Batch Headers and Controls
                                 self.calculate_entry_addenda_record_count() +
                                 1  # File Control
                             ) / 10.0))

    @property
    def batch_count(self):
        return len(self.batches)

    def close(self):
        self.file_control = FileControl(
            batch_count=len(self.batches),
            block_count=self.calculate_block_count(),
            entry_addenda_record_count=self.calculate_entry_addenda_record_count(),
            entry_hash_total=str(sum(int(batch.entry_hash) for batch in self.batches))[-10:],
            total_file_debit_entry_amount=sum(batch.calculate_total_batch_debit_entry() for batch in self.batches),
            total_file_credit_entry_amount=sum(batch.calculate_total_batch_credit_entry() for batch in self.batches),
        )

    @property
    def lines(self):
        line_count = 1
        yield self.file_header
        for batch in self.batches:
            for line in batch.lines:
                line_count += 1
                yield line
        line_count += 1
        yield self.file_control

        if self.include_blocking_lines:
            for _ in range(line_count % 10, 10):
                yield BlockingFileControl()

    def render_to_string(self):
        return '\n'.join(line.dumps() for line in self.lines)
