import datetime

from comanage_nacha.entries.entry import Entry


class CompanyBatchHeader(Entry):
    format = (
        "5"
        "{serviceClassCode:03d}"
        "{companyName: <16s}"
        "{companyDiscretionaryData: <20s}"
        "{companyId: >10s}"
        "{standardEntryClass: >3s}"
        "{companyEntryDescription: <10s}"
        "{companyDescriptiveDate: >6s}"
        "{effectiveEntryDate:%y%m%d}"
        "{settlementDate: >3s}"
        "{originatorStatusCode:1d}"
        "{wellsFargoRoutingNumber:8s}"
        "{batchNumber:07d}"
    )

    code = '5'
    serviceClassCode = None
    companyName = None
    companyDiscretionaryData = ''
    companyId = None
    standardEntryClass = None
    companyEntryDescription = None
    companyDescriptiveDate = None
    effectiveEntryDate = None
    settlementDate = ''
    originatorStatusCode = 1
    wellsFargoRoutingNumber = '09100001'
    batchNumber = None
    rejected = None
    errorCode = None

    def loads(self, line):
        self.serviceClassCode = int(line[1:1 + 3])
        self.companyName = line[4:4 + 16].rstrip()
        self.companyDiscretionaryData = line[20:20 + 20].strip()
        self.companyId = line[40:40 + 10]
        self.standardEntryClass = line[50:50 + 3]
        self.companyEntryDescription = line[53:53 + 10].rstrip()
        self.companyDescriptiveDate = line[63:63 + 6].rstrip()
        self.effectiveEntryDate = datetime.datetime.strptime(line[69:69 + 6], '%y%m%d').date()
        self.settlementDate = line[75:75 + 3]
        self.originatorStatusCode = int(line[78:78 + 1])
        self.wellsFargoRoutingNumber = line[79:79 + 8]
        self.batchNumber = int(line[87:87 + 7])

        if line[79:79 + 4] == 'REJ0':
            self.rejected = True
            self.errorCode = line[83:83 + 4]
