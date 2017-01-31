from unittest2 import TestCase

from comanage_nacha.entries import FileControl


class FileControlTestCase(TestCase):
    def test_loads(self):
        file_control = FileControl.from_text(
            "9000001000001000000050043383527000000000000000000238890                                       "
        )

        self.assertEqual(1, file_control.batchCount)
        self.assertEqual(1, file_control.blockCount)
        self.assertEqual(5, file_control.entryAddendaRecordCount)
        self.assertEqual(43383527, file_control.entryHashTotal)
        self.assertEqual(0, file_control.totalFileDebitEntryAmount)
        self.assertEqual(238890, file_control.totalFileCreditEntryAmount)

    def test_dumps(self):
        file_control = FileControl()

        file_control.batchCount = 1
        file_control.blockCount = 1
        file_control.entryAddendaRecordCount = 5
        file_control.entryHashTotal = 43383527
        file_control.totalFileDebitEntryAmount = 0
        file_control.totalFileCreditEntryAmount = 238890

        self.assertEqual(
            "9000001000001000000050043383527000000000000000000238890                                       ",
            file_control.dumps()
        )

    def test_dumps_message_codes(self):
        file_control = FileControl()

        file_control.batchCount = 1
        file_control.blockCount = 1
        file_control.entryAddendaRecordCount = 5
        file_control.entryHashTotal = 43383527
        file_control.totalFileDebitEntryAmount = 0
        file_control.totalFileCreditEntryAmount = 238890
        file_control.messageCode1 = '01'
        self.assertEqual(
            "9000001000001000000050043383527000000000000000000238890 01                                    ",
            file_control.dumps()
        )
        file_control.messageCode2 = '02'
        self.assertEqual(
            "9000001000001000000050043383527000000000000000000238890 0102                                  ",
            file_control.dumps()
        )
        file_control.messageCode3 = '03'
        self.assertEqual(
            "9000001000001000000050043383527000000000000000000238890 010203                                ",
            file_control.dumps()
        )
        self.assertListEqual(['01', '02', '03'], file_control.messageCodes)

    def test_loads_message_codes(self):
        file_control = FileControl.from_text(
            "9000001000000000000007154810898000000000000000158848838 0102TT                                "
        )

        self.assertEqual('01', file_control.messageCode1)
        self.assertEqual('02', file_control.messageCode2)
        self.assertEqual('TT', file_control.messageCode3)
        self.assertListEqual(['01', '02', 'TT'], file_control.messageCodes)
