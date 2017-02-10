from comanage_nacha.entries.company_batch_control import CompanyBatchControl


def test_loads():
    company_batch_control = CompanyBatchControl.from_text(
        "820000000500433835270000000000000000002388901123456789                         091000010000001")
    assert 200 == company_batch_control.service_class_code
    assert 5 == company_batch_control.entry_addenda_count
    assert 43383527 == company_batch_control.entry_hash
    assert 0 == company_batch_control.total_batch_debit_entry_dollar_amount
    assert 238890 == company_batch_control.total_batch_credit_entry_dollar_amount
    assert '1123456789' == company_batch_control.company_id
    assert '09100001' == company_batch_control.wells_fargo_routing_number
    assert 1 == company_batch_control.batch_number


def test_dumps():
    company_batch_control = CompanyBatchControl()
    company_batch_control.service_class_code = 200
    company_batch_control.entry_addenda_count = 5
    company_batch_control.entry_hash = 43383527
    company_batch_control.total_batch_debit_entry_dollar_amount = 0
    company_batch_control.total_batch_credit_entry_dollar_amount = 238890
    company_batch_control.company_id = '1123456789'
    company_batch_control.batch_number = 1
    assert "820000000500433835270000000000000000002388901123456789                         091000010000001" == company_batch_control.dumps()


def test_reject():
    company_batch_control = CompanyBatchControl.from_text(
        "820000002000182000020000000000000000000300009999999999                         REJ000103841231")
    assert company_batch_control.rejected
    assert '0010' == company_batch_control.error_code
    assert "820000002000182000020000000000000000000300009999999999                         REJ000103841231" == company_batch_control.dumps()


def test_rejecting():
    company_batch_control = CompanyBatchControl.from_text(
        "820000000500433835270000000000000000002388901123456789                         091000010000001")
    company_batch_control.error_code = '1234'
    assert "820000000500433835270000000000000000002388901123456789                         REJ012340000001" == company_batch_control.dumps()
