from .entry import Entry


class FileControl(Entry):
    code = '9'
    format = (
        '9'
        '{batchCount:06d}'
        '{blockCount:06d}'
        '{entryAddendaRecordCount:08d}'
        '{entryHashTotal:010d}'
        '{totalFileDebitEntryAmount:012d}'
        '{totalFileCreditEntryAmount:012d}'
        ' '
        '{messageCode1: <2s}'
        '{messageCode2: <2s}'
        '{messageCode3: <2s}'
        '                                '
    )

    batchCount = None
    blockCount = None
    entryAddendaRecordCount = None
    entryHashTotal = None
    totalFileDebitEntryAmount = None
    totalFileCreditEntryAmount = None
    messageCode1 = ''
    messageCode2 = ''
    messageCode3 = ''

    def loads(self, line):
        self.batchCount = int(line[1:1 + 6])
        self.blockCount = int(line[7:7 + 6])
        self.entryAddendaRecordCount = int(line[13:13 + 8])
        self.entryHashTotal = int(line[21:21 + 10])
        self.totalFileDebitEntryAmount = int(line[31:31 + 12])
        self.totalFileCreditEntryAmount = int(line[43:43 + 12])

        self.messageCode1 = line[56:56 + 2].strip()
        self.messageCode2 = line[58:58 + 2].strip()
        self.messageCode3 = line[60:60 + 2].strip()

    @property
    def messageCodes(self):
        return [i for i in [self.messageCode1, self.messageCode2, self.messageCode3] if i]
