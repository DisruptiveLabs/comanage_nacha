from comanage_nacha.entries.company_batch_control import CompanyBatchControl


def test_loads():
    company_batch_control = CompanyBatchControl.from_text(
        "820000000500433835270000000000000000002388901123456789                         091000010000001")
    assert 200 == company_batch_control.serviceClassCode
    assert 5 == company_batch_control.entryAddendaCount
    assert 43383527 == company_batch_control.entryHash
    assert 0 == company_batch_control.totalBatchDebitEntryDollarAmount
    assert 238890 == company_batch_control.totalBatchCreditEntryDollarAmount
    assert '1123456789' == company_batch_control.companyId
    assert '09100001' == company_batch_control.wellsFargoRoutingNumber
    assert 1 == company_batch_control.batchNumber


def test_dumps():
    company_batch_control = CompanyBatchControl()
    company_batch_control.serviceClassCode = 200
    company_batch_control.entryAddendaCount = 5
    company_batch_control.entryHash = 43383527
    company_batch_control.totalBatchDebitEntryDollarAmount = 0
    company_batch_control.totalBatchCreditEntryDollarAmount = 238890
    company_batch_control.companyId = '1123456789'
    company_batch_control.batchNumber = 1
    assert "820000000500433835270000000000000000002388901123456789                         091000010000001" == company_batch_control.dumps()


def test_reject():
    company_batch_control = CompanyBatchControl.from_text(
        "820000002000182000020000000000000000000300009999999999                         REJ000103841231")
    assert company_batch_control.rejected
    assert '0010' == company_batch_control.errorCode
    assert "820000002000182000020000000000000000000300009999999999                         REJ000103841231" == company_batch_control.dumps()


def test_rejecting():
    company_batch_control = CompanyBatchControl.from_text(
        "820000000500433835270000000000000000002388901123456789                         091000010000001")
    company_batch_control.errorCode = '1234'
    assert "820000000500433835270000000000000000002388901123456789                         REJ012340000001" == company_batch_control.dumps()
