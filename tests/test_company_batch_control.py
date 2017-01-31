from unittest2 import TestCase

from comanage_nacha.entries.company_batch_control import CompanyBatchControl


class CompanyBatchControlTestCase(TestCase):
    def test_loads(self):
        company_batch_control = CompanyBatchControl.from_text(
            "820000000500433835270000000000000000002388901123456789                         091000010000001"
        )

        self.assertEqual(200, company_batch_control.serviceClassCode)
        self.assertEqual(5, company_batch_control.entryAddendaCount)
        self.assertEqual(43383527, company_batch_control.entryHash)
        self.assertEqual(0, company_batch_control.totalBatchDebitEntryDollarAmount)
        self.assertEqual(238890, company_batch_control.totalBatchCreditEntryDollarAmount)
        self.assertEqual('1123456789', company_batch_control.companyId)
        self.assertEqual('09100001', company_batch_control.wellsFargoRoutingNumber)
        self.assertEqual(1, company_batch_control.batchNumber)

    def test_dumps(self):
        company_batch_control = CompanyBatchControl()

        company_batch_control.serviceClassCode = 200
        company_batch_control.entryAddendaCount = 5
        company_batch_control.entryHash = 43383527
        company_batch_control.totalBatchDebitEntryDollarAmount = 0
        company_batch_control.totalBatchCreditEntryDollarAmount = 238890
        company_batch_control.companyId = '1123456789'
        company_batch_control.batchNumber = 1

        self.assertEqual(
            "820000000500433835270000000000000000002388901123456789                         091000010000001",
            company_batch_control.dumps()
        )

    def test_reject(self):
        company_batch_control = CompanyBatchControl.from_text(
            "820000002000182000020000000000000000000300009999999999                         REJ000103841231"
        )

        self.assertTrue(company_batch_control.rejected)
        self.assertEqual('0010', company_batch_control.errorCode)
