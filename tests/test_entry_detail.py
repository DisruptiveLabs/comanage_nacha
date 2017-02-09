from comanage_nacha.entries.entry_detail import EntryDetail


def test_create_dump():
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
    assert '6220764012511234567890       0000055050472727272      JOHN DOE                0091000010000001' == entry_detail.dumps()


def test_loads():
    entry_detail = EntryDetail.from_text(
        '6220764012511234567890       0000055050472727272      JOHN DOE                0091000010000001')
    assert 22 == entry_detail.transactionCode
    assert '07640125' == entry_detail.receivingDFIRoutingNumber
    assert 1 == entry_detail.routingNumberCheckDigit
    assert '1234567890' == entry_detail.receivingDFIAccountNumber
    assert 55050 == entry_detail.amount
    assert '472727272' == entry_detail.individualId
    assert 'JOHN DOE' == entry_detail.individualName
    assert 0 == entry_detail.addendaRecordIndicator
    assert 1 == entry_detail.traceNumber
    assert entry_detail.validate_routing_number_check_digit()


def test_reject():
    entry_detail = EntryDetail.from_text(
        "622507003908999999           0000010000               CUSTOMER ONE            0REJ060300000001")
    assert entry_detail.rejected
    assert '6030' == entry_detail.errorCode
    assert "622507003908999999           0000010000               CUSTOMER ONE            0REJ060300000001" == entry_detail.dumps()
