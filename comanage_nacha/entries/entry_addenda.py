from collections import defaultdict

from comanage_nacha.return_codes import RETURN_CODES
from comanage_nacha.entries.entrybase import EntryBase


class EntryAddendaBase(EntryBase):
    code = '7'

    @classmethod
    def from_text(cls, text):
        instance = addenda_types[text[1:3]]()
        instance.loads(text)
        return instance


class EntryAddenda(EntryAddendaBase):
    addenda_type_code = '05'
    format = (
        '705'
        '{payment_information!s: >80s}'
        '{addenda_sequence_number!d:04d}'
        '{entry_detail_sequence_number!d:07d}'
    )

    def __init__(self,
                 payment_information='',
                 addenda_sequence_number=1,
                 entry_detail_sequence_number=1,
                 error_code=None,
                 ):
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


class EntryAddendaNotificationOfChange(EntryAddendaBase):
    addenda_type_code = '98'
    format = (
        '798'
        '{return_reason_code!s: >3s}'
        '{wells_fargo_routing_number!s:>8s}'
        '{original_entry_trace_number!d:07d}'
        '{date_of_death:%y%m%d}'
        '{original_receiving_dfi_routing_number!s:0>8s}'
        '{addenda_information!s: <44s}'
        '{wells_fargo_routing_number!s:>8s}'
        '{return_entry_trace_number!d:07d}'
    )

    def __init__(self,
                 return_reason_code=None,
                 wells_fargo_routing_number=None,
                 original_entry_trace_number=None,
                 date_of_death=None,
                 original_receiving_dfi_routing_number=None,
                 addenda_information=None,
                 return_entry_trace_number=None,
                 ):
        self.return_reason_code = return_reason_code
        self.wells_fargo_routing_number = wells_fargo_routing_number
        self.original_entry_trace_number = original_entry_trace_number
        self.date_of_death = date_of_death
        self.original_receiving_dfi_routing_number = original_receiving_dfi_routing_number
        self.addenda_information = addenda_information
        self.return_entry_trace_number = return_entry_trace_number

    def loads(self, line):
        self.return_reason_code = line[3:3 + 3]
        self.wells_fargo_routing_number = line[6:6 + 8]
        self.original_entry_trace_number = line[14:14 + 7]
        self.date_of_death = line[21:21 + 6]
        self.original_receiving_dfi_routing_number = line[27:27 + 8]
        self.addenda_information = line[35:35 + 44].strip()
        # Its there twice most likely, we'll ignore for now
        # self.wells_fargo_routing_number = line[79:79 + 8]
        self.return_entry_trace_number = line[87:87 + 7]

    @property
    def return_reason(self):
        if self.return_reason_code:
            return RETURN_CODES[self.return_reason_code]


class EntryAddendaReturned(EntryAddendaNotificationOfChange):
    addenda_type_code = '99'
    format = '799' + EntryAddendaNotificationOfChange.format[3:]


addenda_types = defaultdict(lambda: EntryAddenda, **{
    EntryAddendaNotificationOfChange.addenda_type_code: EntryAddendaNotificationOfChange,
    EntryAddendaReturned.addenda_type_code: EntryAddendaReturned,
})
