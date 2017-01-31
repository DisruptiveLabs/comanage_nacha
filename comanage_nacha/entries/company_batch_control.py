from comanage_nacha.entries.entry import Entry


class CompanyBatchControl(Entry):
    code = '8'
    format = (
        '8'
        '{serviceClassCode:03d}'
        '{entryAddendaCount:06d}'
        '{entryHash:010d}'
        '{totalBatchDebitEntryDollarAmount:012d}'
        '{totalBatchCreditEntryDollarAmount:012d}'
        '{companyId: >10s}'
        '                   '  # Message Authentication Code (19 spaces)
        '      '  # Blank (6 spaces)
        '{wellsFargoRoutingNumber: >8s}'
        '{batchNumber:07d}'
    )

    serviceClassCode = None
    entryAddendaCount = None
    entryHash = None
    totalBatchDebitEntryDollarAmount = None
    totalBatchCreditEntryDollarAmount = None
    companyId = None
    wellsFargoRoutingNumber = '09100001'
    batchNumber = None
    companyBatchRecord = None
    rejected = False
    errorCode = None

    def loads(self, line):
        self.serviceClassCode = int(line[1: 1 + 3])
        self.entryAddendaCount = int(line[4: 4 + 6])
        self.entryHash = int(line[10: 10 + 10])
        self.totalBatchDebitEntryDollarAmount = int(line[20: 20 + 12])
        self.totalBatchCreditEntryDollarAmount = int(line[32: 32 + 12])
        self.companyId = line[44: 44 + 10].rstrip()
        self.wellsFargoRoutingNumber = line[79: 79 + 8]
        self.batchNumber = int(line[87: 87 + 7])

        if line[79:79 + 4] == 'REJ0':
            self.rejected = True
            self.errorCode = line[83:83 + 4]
