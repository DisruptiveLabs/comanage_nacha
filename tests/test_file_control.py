from comanage_nacha.entries import FileControl


def test_loads():
    file_control = FileControl.from_text(
        "9000001000001000000050043383527000000000000000000238890                                       ")
    assert 1 == file_control.batchCount
    assert 1 == file_control.blockCount
    assert 5 == file_control.entryAddendaRecordCount
    assert 43383527 == file_control.entryHashTotal
    assert 0 == file_control.totalFileDebitEntryAmount
    assert 238890 == file_control.totalFileCreditEntryAmount


def test_dumps():
    file_control = FileControl()
    file_control.batchCount = 1
    file_control.blockCount = 1
    file_control.entryAddendaRecordCount = 5
    file_control.entryHashTotal = 43383527
    file_control.totalFileDebitEntryAmount = 0
    file_control.totalFileCreditEntryAmount = 238890
    assert "9000001000001000000050043383527000000000000000000238890                                       " == file_control.dumps()


def test_dumps_message_codes():
    file_control = FileControl()
    file_control.batchCount = 1
    file_control.blockCount = 1
    file_control.entryAddendaRecordCount = 5
    file_control.entryHashTotal = 43383527
    file_control.totalFileDebitEntryAmount = 0
    file_control.totalFileCreditEntryAmount = 238890
    file_control.messageCode1 = '01'
    assert "9000001000001000000050043383527000000000000000000238890 01                                    " == file_control.dumps()
    file_control.messageCode2 = '02'
    assert "9000001000001000000050043383527000000000000000000238890 0102                                  " == file_control.dumps()
    file_control.messageCode3 = '03'
    assert "9000001000001000000050043383527000000000000000000238890 010203                                " == file_control.dumps()
    assert ['01', '02', '03'] == file_control.messageCodes


def test_loads_message_codes():
    file_control = FileControl.from_text(
        "9000001000000000000007154810898000000000000000158848838 0102TT                                ")
    assert '01' == file_control.messageCode1
    assert '02' == file_control.messageCode2
    assert 'TT' == file_control.messageCode3
    assert ['01', '02', 'TT'] == file_control.messageCodes
