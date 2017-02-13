from comanage_nacha.entries.entrybase import EntryBase


class EntryAddenda(EntryBase):
    code = '7'
    format = (
        '7'
        '{addenda_type_code!d:02d}'
        '{payment_information!s: >80s}'
        '{addenda_sequence_number!d:04d}'
        '{entry_detail_sequence_number!d:07d}'
    )

    def __init__(self,
                 addenda_type_code=5,
                 payment_information='',
                 addenda_sequence_number=1,
                 entry_detail_sequence_number=1,
                 error_code=None,
                 ):
        self.addenda_type_code = addenda_type_code
        self.payment_information = payment_information
        self.addenda_sequence_number = addenda_sequence_number
        self.entry_detail_sequence_number = entry_detail_sequence_number
        self.error_code = error_code

    def loads(self, line):
        self.addenda_type_code = int(line[1:1 + 2])
        self.payment_information = line[3:3 + 80].rstrip()
        self.addenda_sequence_number = int(line[83:83 + 4])
        self.entry_detail_sequence_number = int(line[87:87 + 7])

        if line[79:79 + 4] == 'REJ0':
            self.error_code = line[83:83 + 4]
