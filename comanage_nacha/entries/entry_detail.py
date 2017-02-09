from comanage_nacha.entries.entry import Entry


class EntryDetail(Entry):
    code = '6'
    format = (
        '6'
        '{transactionCode:02d}'
        '{receivingDFIRoutingNumber:0>8s}'
        '{routingNumberCheckDigit:1d}'
        '{receivingDFIAccountNumber: <17s}'
        '{amount:010d}'
        '{individualId: <15s}'
        '{individualName: <22s}'
        '{discretionaryData: <2s}'
        '{addendaRecordIndicator:1d}'
        '{wellsFargoRoutingNumber:>8s}'
        '{traceNumber:07d}'
    )

    def __init__(self,
                 transactionCode=None,
                 receivingDFIRoutingNumber=None,
                 routingNumberCheckDigit=None,
                 receivingDFIAccountNumber=None,
                 amount=None,
                 individualId=None,
                 individualName=None,
                 discretionaryData='',
                 addendaRecordIndicator=0,
                 wellsFargoRoutingNumber='09100001',
                 traceNumber=None,
                 companyBatchRecord=None,
                 errorCode=None,
                 ):
        self.transactionCode = transactionCode
        self.receivingDFIRoutingNumber = receivingDFIRoutingNumber
        self.routingNumberCheckDigit = routingNumberCheckDigit
        self.receivingDFIAccountNumber = receivingDFIAccountNumber
        self.amount = amount
        self.individualId = individualId
        self.individualName = individualName
        self.discretionaryData = discretionaryData
        self.addendaRecordIndicator = addendaRecordIndicator
        self.wellsFargoRoutingNumber = wellsFargoRoutingNumber
        self.traceNumber = traceNumber
        self.companyBatchRecord = companyBatchRecord
        self.errorCode = errorCode

    def loads(self, line):
        self.transactionCode = int(line[1: 1 + 2])
        self.receivingDFIRoutingNumber = line[3: 3 + 8]
        self.routingNumberCheckDigit = int(line[11: 11 + 1])
        self.receivingDFIAccountNumber = line[12: 12 + 17].rstrip()
        self.amount = int(line[29: 29 + 10])
        self.individualId = line[39: 39 + 15].rstrip()
        self.individualName = line[54: 54 + 22].rstrip()
        self.discretionaryData = line[76: 76 + 2].strip()
        self.addendaRecordIndicator = int(line[78: 78 + 1])
        self.wellsFargoRoutingNumber = line[79: 79 + 8]
        self.traceNumber = int(line[87:87 + 7])

        if line[79:79 + 4] == 'REJ0':
            self.errorCode = line[83:83 + 4]

    def validate_routing_number_check_digit(self):
        digits = [int(c) for c in self.receivingDFIRoutingNumber]
        weights = [3, 7, 1, 3, 7, 1, 3, 7]

        assert len(digits) == len(weights)
        check_digit = 10 - (sum([a * b for a, b in zip(digits, weights)]) % 10)
        return check_digit == self.routingNumberCheckDigit
