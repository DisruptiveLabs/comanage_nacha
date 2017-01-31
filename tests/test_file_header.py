import datetime

from unittest2 import TestCase

from comanage_nacha.entries.file_header import FileHeader


class FileHeaderTestCase(TestCase):
    def test_create_dump(self):
        file_header = FileHeader()
        file_header.priorityCode = 1
        # file_header.wellsFargoRoutingNumber = '091000019'
        file_header.fileId = '1123456789'
        file_header.fileCreationDate = datetime.date(2011, 9, 13)
        file_header.fileCreationTime = datetime.time(13, 30)
        file_header.fileIdModifier = 'A'
        file_header.recordSize = 94
        file_header.blockingFactor = 10
        file_header.formatCode = 1
        file_header.originationBank = 'WELLS FARGO'
        file_header.companyName = 'COMANAGE'
        file_header.referenceCode = ''

        test = file_header.dumps()
        self.assertEqual(
            '101 09100001911234567891109131330A094101WELLS FARGO            COMANAGE                       ',
            test
        )

    def test_parse(self):
        file_header = FileHeader.from_text(
            '101 09100001911234567891109131330A094101WELLS FARGO            COMANAGE                       '
        )

        self.assertEqual(1, file_header.priorityCode)
        self.assertEqual('091000019', file_header.wellsFargoRoutingNumber)
        self.assertEqual('1123456789', file_header.fileId)
        self.assertEqual(datetime.date(2011, 9, 13), file_header.fileCreationDate)
        self.assertEqual(datetime.time(13, 30), file_header.fileCreationTime)
        self.assertEqual('A', file_header.fileIdModifier)
        self.assertEqual(94, file_header.recordSize)
        self.assertEqual(10, file_header.blockingFactor)
        self.assertEqual(1, file_header.formatCode)
        self.assertEqual('WELLS FARGO', file_header.originationBank)
        self.assertEqual('COMANAGE', file_header.companyName)
        self.assertEqual('', file_header.referenceCode)

    def test_rejected(self):
        file_header = FileHeader.from_text(
            "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP        REJ00010       \n"
        )
        self.assertTrue(file_header.rejected)
        self.assertEqual('0010', file_header.errorCode)
