from comanage_nacha.entries.entrybase import EntryBase


class CompanyBatchControl(EntryBase):
    code = '8'
    format = (
        '8'
        '{service_class_code!d:03d}'
        '{entry_addenda_count!d:06d}'
        '{entry_hash!d:010d}'
        '{total_batch_debit_entry_dollar_amount!d:012d}'
        '{total_batch_credit_entry_dollar_amount!d:012d}'
        '{company_id!s: >10s}'
        '                   '  # Message Authentication Code (19 spaces)
        '      '  # Blank (6 spaces)
        '{wells_fargo_routing_number!s: >8s}'
        '{batch_number!d:07d}'
    )

    def __init__(self,
                 service_class_code=None,
                 entry_addenda_count=None,
                 entry_hash=None,
                 total_batch_debit_entry_dollar_amount=None,
                 total_batch_credit_entry_dollar_amount=None,
                 company_id=None,
                 wells_fargo_routing_number='09100001',
                 batch_number=None,
                 error_code=None,
                 ):
        self.service_class_code = service_class_code
        self.entry_addenda_count = entry_addenda_count
        self.entry_hash = entry_hash
        self.total_batch_debit_entry_dollar_amount = total_batch_debit_entry_dollar_amount
        self.total_batch_credit_entry_dollar_amount = total_batch_credit_entry_dollar_amount
        self.company_id = company_id
        self.wells_fargo_routing_number = wells_fargo_routing_number
        self.batch_number = batch_number
        self.error_code = error_code

    def loads(self, line):
        self.service_class_code = int(line[1: 1 + 3])
        self.entry_addenda_count = int(line[4: 4 + 6])
        self.entry_hash = int(line[10: 10 + 10])
        self.total_batch_debit_entry_dollar_amount = int(line[20: 20 + 12])
        self.total_batch_credit_entry_dollar_amount = int(line[32: 32 + 12])
        self.company_id = line[44: 44 + 10].rstrip()
        self.wells_fargo_routing_number = line[79: 79 + 8]
        self.batch_number = int(line[87: 87 + 7])

        if line[79:79 + 4] == 'REJ0':
            self.error_code = line[83:83 + 4]
