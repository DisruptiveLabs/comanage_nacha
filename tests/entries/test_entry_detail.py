from comanage_nacha.entries.entry_detail import EntryDetail


def test_create_dump():
    entry_detail = EntryDetail()
    entry_detail.transaction_code = 22
    entry_detail.receiving_dfi_routing_number = '07640125'
    entry_detail.routing_number_check_digit = 1
    entry_detail.receiving_dfi_account_number = '1234567890'
    entry_detail.amount = 55050
    entry_detail.individual_id = '472727272'
    entry_detail.individual_name = 'JOHN DOE'
    entry_detail.addenda_record_indicator = 0
    entry_detail.trace_number = 1
    assert '6220764012511234567890       0000055050472727272      JOHN DOE                0091000010000001' == entry_detail.dumps()


def test_loads():
    entry_detail = EntryDetail.from_text(
        '6220764012511234567890       0000055050472727272      JOHN DOE                0091000010000001')
    assert 22 == entry_detail.transaction_code
    assert '07640125' == entry_detail.receiving_dfi_routing_number
    assert 1 == entry_detail.routing_number_check_digit
    assert '1234567890' == entry_detail.receiving_dfi_account_number
    assert 55050 == entry_detail.amount
    assert '472727272' == entry_detail.individual_id
    assert 'JOHN DOE' == entry_detail.individual_name
    assert 0 == entry_detail.addenda_record_indicator
    assert 1 == entry_detail.trace_number
    assert entry_detail.validate_routing_number_check_digit()


def test_reject():
    entry_detail = EntryDetail.from_text(
        "622507003908999999           0000010000               CUSTOMER ONE            0REJ060300000001")
    assert entry_detail.rejected
    assert '6030' == entry_detail.error_code
    assert "622507003908999999           0000010000               CUSTOMER ONE            0REJ060300000001" == entry_detail.dumps()


def test_long_name():
    entry_detail = EntryDetail()
    entry_detail.transaction_code = 22
    entry_detail.receiving_dfi_routing_number = '07640125'
    entry_detail.routing_number_check_digit = 1
    entry_detail.receiving_dfi_account_number = '1234567890'
    entry_detail.amount = 55050
    entry_detail.individual_id = '472727272'
    entry_detail.individual_name = 'Saguaro Property Management'
    entry_detail.addenda_record_indicator = 0
    entry_detail.trace_number = 1

    assert '6220764012511234567890       0000055050472727272      Saguaro Property Manag  0091000010000001' == entry_detail.dumps()