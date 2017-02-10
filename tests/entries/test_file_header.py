import datetime

from comanage_nacha.entries.file_header import FileHeader


def test_create_dump():
    file_header = FileHeader()
    file_header.priority_code = 1
    file_header.file_id = '1123456789'
    file_header.file_creation_date = datetime.date(2011, 9, 13)
    file_header.file_creation_time = datetime.time(13, 30)
    file_header.file_id_modifier = 'A'
    file_header.record_size = 94
    file_header.blocking_factor = 10
    file_header.format_code = 1
    file_header.origination_bank = 'WELLS FARGO'
    file_header.company_name = 'COMANAGE'
    file_header.reference_code = ''
    test = file_header.dumps()
    assert '101 09100001911234567891109131330A094101WELLS FARGO            COMANAGE                       ' == test


def test_parse():
    file_header = FileHeader.from_text(
        '101 09100001911234567891109131330A094101WELLS FARGO            COMANAGE                       '
    )
    assert 1 == file_header.priority_code
    assert '091000019' == file_header.wells_fargo_routing_number
    assert '1123456789' == file_header.file_id
    assert datetime.date(2011, 9, 13) == file_header.file_creation_date
    assert datetime.time(13, 30) == file_header.file_creation_time
    assert 'A' == file_header.file_id_modifier
    assert 94 == file_header.record_size
    assert 10 == file_header.blocking_factor
    assert 1 == file_header.format_code
    assert 'WELLS FARGO' == file_header.origination_bank
    assert 'COMANAGE' == file_header.company_name
    assert '' == file_header.reference_code


def test_rejected():
    file_header = FileHeader.from_text(
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP        REJ00010       "
    )
    assert file_header.rejected
    assert '0010' == file_header.error_code
    assert 'Duplicate file or batch' == file_header.error_reason
    assert "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP        REJ00010       " == file_header.dumps()


def test_rejecting():
    file_header = FileHeader.from_text(
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP                       "
    )
    file_header.error_code = '0010'
    assert "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP        REJ00010       " == file_header.dumps()
