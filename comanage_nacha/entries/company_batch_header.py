import datetime

from comanage_nacha.entries.entrybase import EntryBase


class CompanyBatchHeader(EntryBase):
    code = '5'
    format = (
        "5"
        "{service_class_code!d:03d}"
        "{company_name!s: <16s}"
        "{company_discretionary_data!s: <20s}"
        "{company_id!s: >10s}"
        "{standard_entry_class!s: >3s}"
        "{company_entry_description!s: <10s}"
        "{company_descriptive_date!s: >6s}"
        "{effective_entry_date:%y%m%d}"
        "{settlement_date!s: >3s}"
        "{originator_status_code!d:1d}"
        "{wells_fargo_routing_number!s:8s}"
        "{batch_number!d:07d}"
    )

    def __init__(self,
                 service_class_code=None,
                 company_name=None,
                 company_discretionary_data='',
                 company_id=None,
                 standard_entry_class=None,
                 company_entry_description=None,
                 company_descriptive_date=None,
                 effective_entry_date=None,
                 settlement_date='',
                 originator_status_code=1,
                 wells_fargo_routing_number='09100001',
                 batch_number=None,
                 error_code=None,
                 ):
        self.service_class_code = service_class_code
        self.company_name = company_name
        self.company_discretionary_data = company_discretionary_data
        self.company_id = company_id
        self.standard_entry_class = standard_entry_class
        self.company_entry_description = company_entry_description
        self.company_descriptive_date = company_descriptive_date
        self.effective_entry_date = effective_entry_date
        self.settlement_date = settlement_date
        self.originator_status_code = originator_status_code
        self.wells_fargo_routing_number = wells_fargo_routing_number
        self.batch_number = batch_number
        self.error_code = error_code

    def loads(self, line):
        self.service_class_code = int(line[1:1 + 3])
        self.company_name = line[4:4 + 16].rstrip()
        self.company_discretionary_data = line[20:20 + 20].strip()
        self.company_id = line[40:40 + 10]
        self.standard_entry_class = line[50:50 + 3]
        self.company_entry_description = line[53:53 + 10].rstrip()
        self.company_descriptive_date = line[63:63 + 6].rstrip()
        self.effective_entry_date = datetime.datetime.strptime(line[69:69 + 6], '%y%m%d').date()
        self.settlement_date = line[75:75 + 3]
        self.originator_status_code = int(line[78:78 + 1])
        self.wells_fargo_routing_number = line[79:79 + 8]
        self.batch_number = int(line[87:87 + 7])

        if line[79:79 + 4] == 'REJ0':
            self.error_code = line[83:83 + 4]
