from comanage_nacha.entries import FileControl


def test_loads():
    file_control = FileControl.from_text(
        "9000001000001000000050043383527000000000000000000238890                                       ")
    assert 1 == file_control.batch_count
    assert 1 == file_control.block_count
    assert 5 == file_control.entry_addenda_record_count
    assert 43383527 == file_control.entry_hash_total
    assert 0 == file_control.total_file_debit_entry_amount
    assert 238890 == file_control.total_file_credit_entry_amount


def test_dumps():
    file_control = FileControl()
    file_control.batch_count = 1
    file_control.block_count = 1
    file_control.entry_addenda_record_count = 5
    file_control.entry_hash_total = 43383527
    file_control.total_file_debit_entry_amount = 0
    file_control.total_file_credit_entry_amount = 238890
    assert "9000001000001000000050043383527000000000000000000238890                                       " == file_control.dumps()


def test_dumps_message_codes():
    file_control = FileControl()
    file_control.batch_count = 1
    file_control.block_count = 1
    file_control.entry_addenda_record_count = 5
    file_control.entry_hash_total = 43383527
    file_control.total_file_debit_entry_amount = 0
    file_control.total_file_credit_entry_amount = 238890
    file_control.message_code1 = '01'
    assert "9000001000001000000050043383527000000000000000000238890 01                                    " == file_control.dumps()
    file_control.message_code2 = '02'
    assert "9000001000001000000050043383527000000000000000000238890 0102                                  " == file_control.dumps()
    file_control.message_code3 = '03'
    assert "9000001000001000000050043383527000000000000000000238890 010203                                " == file_control.dumps()
    assert ['01', '02', '03'] == file_control.message_codes


def test_loads_message_codes():
    file_control = FileControl.from_text(
        "9000001000000000000007154810898000000000000000158848838 0102TT                                ")
    assert '01' == file_control.message_code1
    assert '02' == file_control.message_code2
    assert 'TT' == file_control.message_code3
    assert ['01', '02', 'TT'] == file_control.message_codes
