import datetime

from comanage_nacha.entries.company_batch_header import CompanyBatchHeader


def test_create_dump():
    batch_header = CompanyBatchHeader()
    batch_header.service_class_code = 200
    batch_header.company_name = 'ABC COMPANY'
    batch_header.company_id = '1123456789'
    batch_header.standard_entry_class = 'PPD'
    batch_header.company_entry_description = 'PAYROLL'
    batch_header.company_descriptive_date = 'SEP 15'
    batch_header.effective_entry_date = datetime.date(2011, 9, 15)
    batch_header.batch_number = 1
    assert "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1091000010000001" == batch_header.dumps()


def test_loads():
    batch_header = CompanyBatchHeader.from_text(
        "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1091000010000001"
    )
    assert 200 == batch_header.service_class_code
    assert 'ABC COMPANY' == batch_header.company_name
    assert '1123456789' == batch_header.company_id
    assert 'PPD' == batch_header.standard_entry_class
    assert 'PAYROLL' == batch_header.company_entry_description
    assert 'SEP 15' == batch_header.company_descriptive_date
    assert datetime.date(2011, 9, 15) == batch_header.effective_entry_date
    assert 1 == batch_header.batch_number


def test_rejected():
    batch_header = CompanyBatchHeader.from_text(
        "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1REJ000103841231"
    )
    assert batch_header.rejected
    assert '0010' == batch_header.error_code
    assert "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1REJ000103841231" == batch_header.dumps()


def test_rejecting():
    batch_header = CompanyBatchHeader.from_text(
        "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1091000010000001"
    )
    batch_header.error_code = '1234'
    assert "5200ABC COMPANY                         1123456789PPDPAYROLL   SEP 15110915   1REJ012340000001" == batch_header.dumps()


def test_simple_header():
    source_data = "5225COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001"
    batch_header = CompanyBatchHeader.from_text(source_data)
    assert source_data == batch_header.dumps()
