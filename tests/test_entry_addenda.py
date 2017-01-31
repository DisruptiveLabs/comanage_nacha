from unittest2 import TestCase

from comanage_nacha.entries.entry_addenda import EntryAddenda


class EntryAddendaTestCase(TestCase):
    def test_loads(self):
        addenda = EntryAddenda.from_text(
            '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00201000040000001'
        )

        self.assertEqual(5, addenda.addendaTypeCode)
        self.assertEqual(4, addenda.addendaSequenceNumber)
        self.assertEqual(1, addenda.entryDetailSequenceNumber)
        self.assertEqual(
            '0*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*002010',
            addenda.paymentInformation
        )

    def test_dumps(self):
        addenda = EntryAddenda()
        addenda.addendaTypeCode = 5
        addenda.addendaSequenceNumber = 4
        addenda.entryDetailSequenceNumber = 1
        addenda.paymentInformation = '0*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*002010'

        self.assertEqual(
            '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00201000040000001',
            addenda.dumps()
        )

    def test_reject(self):
        addenda = EntryAddenda.from_text(
            '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00REJ060300000001'
        )

        self.assertTrue(addenda.rejected)
        self.assertEqual('6030', addenda.errorCode)
