import datetime

from comanage_nacha.entries.company_batch_header import CompanyBatchHeader


def test_create_dump():
    batch_header = CompanyBatchHeader()
    batch_header.serviceClassCode = 200
    batch_header.companyName = 'ABC COMPANY'
    batch_header.companyId = '1123456789'
    batch_header.standardEntryClass = 'PPD'
    batch_header.companyEntryDescription = 'PAYROLL'
    batch_header.companyDescriptiveDate = 'SEP 15'
    batch_header.effectiveEntryDate = datetime.date(2011, 9, 15)
    batch_header.batchNumber = 1
    assert "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1091000010000001" == batch_header.dumps()


def test_loads():
    batch_header = CompanyBatchHeader.from_text(
        "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1091000010000001"
    )
    assert 200 == batch_header.serviceClassCode
    assert 'ABC COMPANY' == batch_header.companyName
    assert '1123456789' == batch_header.companyId
    assert 'PPD' == batch_header.standardEntryClass
    assert 'PAYROLL' == batch_header.companyEntryDescription
    assert 'SEP 15' == batch_header.companyDescriptiveDate
    assert datetime.date(2011, 9, 15) == batch_header.effectiveEntryDate
    assert 1 == batch_header.batchNumber


def test_rejected():
    batch_header = CompanyBatchHeader.from_text(
        "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1REJ000103841231"
    )
    assert batch_header.rejected
    assert '0010' == batch_header.errorCode
    assert "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1REJ000103841231" == batch_header.dumps()


def test_rejecting():
    batch_header = CompanyBatchHeader.from_text(
        "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1091000010000001"
    )
    batch_header.errorCode = '1234'
    assert "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1REJ012340000001" == batch_header.dumps()


def test_simple_header():
    source_data = "5225COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001"
    batch_header = CompanyBatchHeader.from_text(source_data)
    assert source_data == batch_header.dumps()
