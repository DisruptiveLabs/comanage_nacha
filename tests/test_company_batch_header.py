import datetime

from unittest2 import TestCase

from comanage_nacha.entries.company_batch_header import CompanyBatchHeader


class CompanyBatchHeaderTestCase(TestCase):
    def test_create_dump(self):
        batch_header = CompanyBatchHeader()
        batch_header.serviceClassCode = 200
        batch_header.companyName = 'ABC COMPANY'
        batch_header.companyId = '1123456789'
        batch_header.standardEntryClass = 'PPD'
        batch_header.companyEntryDescription = 'PAYROLL'
        batch_header.companyDescriptiveDate = 'SEP 15'
        batch_header.effectiveEntryDate = datetime.date(2011, 9, 15)
        batch_header.batchNumber = 1

        self.assertEqual(
            "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1091000010000001",
            batch_header.dumps()
        )

    def test_loads(self):
        batch_header = CompanyBatchHeader.from_text(
            "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1091000010000001"
        )

        self.assertEqual(200, batch_header.serviceClassCode)
        self.assertEqual('ABC COMPANY', batch_header.companyName)
        self.assertEqual('1123456789', batch_header.companyId)
        self.assertEqual('PPD', batch_header.standardEntryClass)
        self.assertEqual('PAYROLL', batch_header.companyEntryDescription)
        self.assertEqual('SEP 15', batch_header.companyDescriptiveDate)
        self.assertEqual(datetime.date(2011, 9, 15), batch_header.effectiveEntryDate)
        self.assertEqual(1, batch_header.batchNumber)

    def test_rejected(self):
        batch_header = CompanyBatchHeader.from_text(
            "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1REJ000103841231"
        )

        self.assertTrue(batch_header.rejected)
        self.assertEqual('0010', batch_header.errorCode)

    def test_simple_header(self):
        source_data = "5225COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001"
        batch_header = CompanyBatchHeader.from_text(source_data)
        self.assertEqual(source_data, batch_header.dumps())
