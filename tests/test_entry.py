from comanage_nacha.entry import Entry


def test_add_addenda():
    entry = Entry(1)
    assert entry.entry_detail.addenda_record_indicator == 0
    addenda = entry.add_addenda()
    assert entry.entry_detail.addenda_record_indicator == 1
    assert entry.addenda == [addenda]


def test_is_credit():
    entry = Entry(1, transaction_code='23')
    assert entry.is_credit


def test_is_debit():
    entry = Entry(1, transaction_code='27')
    assert entry.is_debit


def test_addenda_count():
    entry = Entry(1)
    assert entry.addenda_count == 0
    entry.add_addenda()
    assert entry.addenda_count == 1
    entry.add_addenda()
    entry.add_addenda()
    assert entry.addenda_count == 3


def test_lines():
    entry = Entry(1,
                  transaction_code=22,
                  receiving_dfi_routing_number='07640125',
                  routing_number_check_digit=1,
                  receiving_dfi_account_number='1234567890',
                  amount=55050,
                  individual_id='472727272',
                  individual_name='JOHN DOE',
                  addenda_record_indicator=0)
    assert len(list(entry.lines)) == 1
    entry.add_addenda()
    assert len(list(entry.lines)) == 2
