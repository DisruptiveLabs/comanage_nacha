from unittest2 import TestCase

from comanage_nacha.entries.entry_detail import EntryDetail


class EntryDetailTestCase(TestCase):
    def test_create_dump(self):
        entry_detail = EntryDetail()
        entry_detail.transactionCode = 22
        entry_detail.receivingDFIRoutingNumber = '07640125'
        entry_detail.routingNumberCheckDigit = 1
        entry_detail.receivingDFIAccountNumber = '1234567890'
        entry_detail.amount = 55050
        entry_detail.individualId = '472727272'
        entry_detail.individualName = 'JOHN DOE'
        entry_detail.addendaRecordIndicator = 0
        entry_detail.traceNumber = 1

        self.assertEqual(
            '6220764012511234567890       0000055050472727272      JOHN DOE                0091000010000001',
            entry_detail.dumps()
        )

    def test_loads(self):
        entry_detail = EntryDetail.from_text(
            '6220764012511234567890       0000055050472727272      JOHN DOE                0091000010000001'
        )

        self.assertEqual(22, entry_detail.transactionCode)
        self.assertEqual('07640125', entry_detail.receivingDFIRoutingNumber)
        self.assertEqual(1, entry_detail.routingNumberCheckDigit)
        self.assertEqual('1234567890', entry_detail.receivingDFIAccountNumber)
        self.assertEqual(55050, entry_detail.amount)
        self.assertEqual('472727272', entry_detail.individualId)
        self.assertEqual('JOHN DOE', entry_detail.individualName)
        self.assertEqual(0, entry_detail.addendaRecordIndicator)
        self.assertEqual(1, entry_detail.traceNumber)
        a, b = entry_detail.validate_routing_number_check_digit()
        self.assertEqual(a, b)

    def test_reject(self):
        entry_detail = EntryDetail.from_text(
            "622507003908999999           0000010000               CUSTOMER ONE            0REJ060300000001"
        )

        self.assertTrue(entry_detail.rejected)
        self.assertEqual('6030', entry_detail.errorCode)
