import datetime

from comanage_nacha.entries.entrybase import EntryBase


class FileHeader(EntryBase):
    code = '1'
    format = (
        "1"
        "{priority_code!d:02d}"
        "{wells_fargo_routing_number!s: >10s}"
        "{file_id!s:10s}"
        "{file_creation_date:%y%m%d}"
        "{file_creation_time:%H%M}"
        "{file_id_modifier!s:1s}"
        "{record_size!d:0>3d}"
        "{blocking_factor!d:0>2d}"
        "{format_code!d:1d}"
        "{origination_bank!s: <23s}"
        "{company_name!s: <23s}"
        "{reference_code!s: >8s}"
    )

    def __init__(self,
                 priority_code=1,
                 wells_fargo_routing_number='091000019',
                 file_id=None,
                 file_creation_date=None,
                 file_creation_time=None,
                 file_id_modifier='A',
                 record_size=94,
                 blocking_factor=10,
                 format_code=1,
                 origination_bank='WELLS FARGO',
                 company_name=None,
                 reference_code=None,
                 error_code=None,
                 ):
        self.priority_code = priority_code
        self.wells_fargo_routing_number = wells_fargo_routing_number
        self.file_id = file_id
        self.file_creation_date = file_creation_date
        self.file_creation_time = file_creation_time
        self.file_id_modifier = file_id_modifier
        self.record_size = record_size
        self.blocking_factor = blocking_factor
        self.format_code = format_code
        self.origination_bank = origination_bank
        self.company_name = company_name
        self.reference_code = reference_code
        self.error_code = error_code

    def loads(self, line):
        self.priority_code = int(line[1: 1 + 2])
        self.wells_fargo_routing_number = line[3: 3 + 10].strip()
        self.file_id = line[13: 13 + 10]
        self.file_creation_date = datetime.datetime.strptime(line[23: 23 + 6], '%y%m%d').date()
        self.file_creation_time = datetime.datetime.strptime(line[29: 29 + 4], '%H%M').time()
        self.file_id_modifier = line[33: 33 + 1]
        self.record_size = int(line[34: 34 + 3])
        self.blocking_factor = int(line[37: 37 + 2])
        self.format_code = int(line[39: 39 + 1])
        self.origination_bank = line[40: 40 + 23].rstrip()
        self.company_name = line[63: 63 + 23].rstrip()
        self.reference_code = line[86: 86 + 8].lstrip()
        if line[79:79 + 4] == 'REJ0':
            self.error_code = line[83: 83 + 4]
