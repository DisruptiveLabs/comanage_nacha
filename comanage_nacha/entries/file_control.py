from .entrybase import EntryBase


class FileControl(EntryBase):
    code = '9'
    format = (
        '9'
        '{batch_count!d:06d}'
        '{block_count!d:06d}'
        '{entry_addenda_record_count!d:08d}'
        '{entry_hash_total!d:010d}'
        '{total_file_debit_entry_amount!d:012d}'
        '{total_file_credit_entry_amount!d:012d}'
        ' '
        '{message_code1!s: <2s}'
        '{message_code2!s: <2s}'
        '{message_code3!s: <2s}'
        '                                '
    )

    def __init__(self,
                 batch_count=None,
                 block_count=None,
                 entry_addenda_record_count=None,
                 entry_hash_total=None,
                 total_file_debit_entry_amount=None,
                 total_file_credit_entry_amount=None,
                 message_code1='',
                 message_code2='',
                 message_code3='',
                 ):
        self.batch_count = batch_count
        self.block_count = block_count
        self.entry_addenda_record_count = entry_addenda_record_count
        self.entry_hash_total = entry_hash_total
        self.total_file_debit_entry_amount = total_file_debit_entry_amount
        self.total_file_credit_entry_amount = total_file_credit_entry_amount
        self.message_code1 = message_code1
        self.message_code2 = message_code2
        self.message_code3 = message_code3

    def loads(self, line):
        self.batch_count = int(line[1:1 + 6])
        self.block_count = int(line[7:7 + 6])
        self.entry_addenda_record_count = int(line[13:13 + 8])
        self.entry_hash_total = int(line[21:21 + 10])
        self.total_file_debit_entry_amount = int(line[31:31 + 12])
        self.total_file_credit_entry_amount = int(line[43:43 + 12])

        self.message_code1 = line[56:56 + 2].strip()
        self.message_code2 = line[58:58 + 2].strip()
        self.message_code3 = line[60:60 + 2].strip()

    @property
    def message_codes(self):
        return [i for i in [self.message_code1, self.message_code2, self.message_code3] if i]
