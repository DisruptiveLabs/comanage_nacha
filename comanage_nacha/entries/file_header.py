import datetime

from comanage_nacha.entries.entry import Entry


class FileHeader(Entry):
    format = (
        "1"
        "{priorityCode:02d}"
        "{wellsFargoRoutingNumber: >10s}"
        "{fileId:10s}"
        "{fileCreationDate:%y%m%d}"
        "{fileCreationTime:%H%M}"
        "{fileIdModifier:1s}"
        "{recordSize:0>3d}"
        "{blockingFactor:0>2d}"
        "{formatCode:1d}"
        "{originationBank: <23s}"
        "{companyName: <23s}"
        "{referenceCode: >8s}"
    )

    code = '1'
    priorityCode = None
    wellsFargoRoutingNumber = '091000019'
    fileId = None
    fileCreationDate = None
    fileCreationTime = None
    fileCreationDateTime = None
    fileIdModifier = None
    recordSize = 94
    blockingFactor = 10
    formatCode = 1
    originationBank = 'WELLS FARGO'
    companyName = None
    referenceCode = None
    rejected = None
    errorCode = None

    def loads(self, line):
        self.priorityCode = int(line[1: 1 + 2])
        self.wellsFargoRoutingNumber = line[3: 3 + 10].strip()
        self.fileId = line[13: 13 + 10]
        self.fileCreationDate = datetime.datetime.strptime(line[23: 23 + 6], '%y%m%d').date()
        self.fileCreationTime = datetime.datetime.strptime(line[29: 29 + 4], '%H%M').time()
        self.fileIdModifier = line[33: 33 + 1]
        self.recordSize = int(line[34: 34 + 3])
        self.blockingFactor = int(line[37: 37 + 2])
        self.formatCode = int(line[39: 39 + 1])
        self.originationBank = line[40: 40 + 23].rstrip()
        self.companyName = line[63: 63 + 23].rstrip()
        self.referenceCode = line[86: 86 + 8].rstrip()
        if line[79:79 + 4] == 'REJ0':
            self.rejected = True
            self.errorCode = line[83: 83 + 4]
