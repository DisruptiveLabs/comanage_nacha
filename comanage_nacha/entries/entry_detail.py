from comanage_nacha.entries.entrybase import EntryBase
from comanage_nacha.utils.check_digit import validate_check_digit


class EntryDetail(EntryBase):
    code = '6'
    format = (
        '6'
        '{transaction_code!d:02d}'
        '{receiving_dfi_routing_number!s:0>8s}'
        '{routing_number_check_digit!d:1d}'
        '{receiving_dfi_account_number!s: <17s}'
        '{amount!d:010d}'
        '{individual_id!s: <15s}'
        '{individual_name!s: <22s}'
        '{discretionary_data!s: <2s}'
        '{addenda_record_indicator!d:1d}'
        '{wells_fargo_routing_number!s:>8s}'
        '{trace_number!d:07d}'
    )

    def __init__(self,
                 transaction_code=None,
                 receiving_dfi_routing_number=None,
                 routing_number_check_digit=None,
                 receiving_dfi_account_number=None,
                 amount=None,
                 individual_id=None,
                 individual_name=None,
                 discretionary_data='',
                 addenda_record_indicator=0,
                 wells_fargo_routing_number='09100001',
                 trace_number=None,
                 error_code=None,
                 ):
        self.transaction_code = transaction_code
        self.receiving_dfi_routing_number = receiving_dfi_routing_number
        self.routing_number_check_digit = routing_number_check_digit
        self.receiving_dfi_account_number = receiving_dfi_account_number
        self.amount = amount
        self.individual_id = individual_id
        self.individual_name = individual_name
        self.discretionary_data = discretionary_data
        self.addenda_record_indicator = addenda_record_indicator
        self.wells_fargo_routing_number = wells_fargo_routing_number
        self.trace_number = trace_number
        self.error_code = error_code

    def loads(self, line):
        self.transaction_code = int(line[1: 1 + 2])
        self.receiving_dfi_routing_number = line[3: 3 + 8]
        self.routing_number_check_digit = int(line[11: 11 + 1])
        self.receiving_dfi_account_number = line[12: 12 + 17].rstrip()
        self.amount = int(line[29: 29 + 10])
        self.individual_id = line[39: 39 + 15].rstrip()
        self.individual_name = line[54: 54 + 22].rstrip()
        self.discretionary_data = line[76: 76 + 2].strip()
        self.addenda_record_indicator = int(line[78: 78 + 1])
        self.wells_fargo_routing_number = line[79: 79 + 8]
        self.trace_number = int(line[87:87 + 7])

        if line[79:79 + 4] == 'REJ0':
            self.error_code = line[83:83 + 4]

    def validate_routing_number_check_digit(self):
        return validate_check_digit(self.receiving_dfi_routing_number, self.routing_number_check_digit)
