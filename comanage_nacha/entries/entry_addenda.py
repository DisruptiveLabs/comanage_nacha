from comanage_nacha.entries.entry import Entry


class EntryAddenda(Entry):
    code = '7'
    format = (
        '7'
        '{addendaTypeCode:02d}'
        '{paymentInformation: >80s}'
        '{addendaSequenceNumber:04d}'
        '{entryDetailSequenceNumber:07d}'
    )

    addendaTypeCode = 5
    paymentInformation = ''
    addendaSequenceNumber = 1
    entryDetailSequenceNumber = 1
    rejected = False
    errorCode = None

    def loads(self, line):
        self.addendaTypeCode = int(line[1:1 + 2])
        self.paymentInformation = line[3:3 + 80].rstrip()
        self.addendaSequenceNumber = int(line[83:83 + 4])
        self.entryDetailSequenceNumber = int(line[87:87 + 7])

        if line[79:79 + 4] == 'REJ0':
            self.rejected = True
            self.errorCode = line[83:83 + 4]
