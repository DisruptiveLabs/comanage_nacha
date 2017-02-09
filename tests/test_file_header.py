import datetime

from comanage_nacha.entries.file_header import FileHeader


def test_create_dump():
    file_header = FileHeader()
    file_header.priorityCode = 1
    file_header.fileId = '1123456789'
    file_header.fileCreationDate = datetime.date(2011, 9, 13)
    file_header.fileCreationTime = datetime.time(13, 30)
    file_header.fileIdModifier = 'A'
    file_header.recordSize = 94
    file_header.blockingFactor = 10
    file_header.formatCode = 1
    file_header.originationBank = 'WELLS FARGO'
    file_header.companyName = 'COMANAGE'
    file_header.referenceCode = ''
    test = file_header.dumps()
    assert '101 09100001911234567891109131330A094101WELLS FARGO            COMANAGE                       ' == test


def test_parse():
    file_header = FileHeader.from_text(
        '101 09100001911234567891109131330A094101WELLS FARGO            COMANAGE                       '
    )
    assert 1 == file_header.priorityCode
    assert '091000019' == file_header.wellsFargoRoutingNumber
    assert '1123456789' == file_header.fileId
    assert datetime.date(2011, 9, 13) == file_header.fileCreationDate
    assert datetime.time(13, 30) == file_header.fileCreationTime
    assert 'A' == file_header.fileIdModifier
    assert 94 == file_header.recordSize
    assert 10 == file_header.blockingFactor
    assert 1 == file_header.formatCode
    assert 'WELLS FARGO' == file_header.originationBank
    assert 'COMANAGE' == file_header.companyName
    assert '' == file_header.referenceCode


def test_rejected():
    file_header = FileHeader.from_text(
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP        REJ00010       "
    )
    assert file_header.rejected
    assert '0010' == file_header.errorCode
    assert "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP        REJ00010       " == file_header.dumps()


def test_rejecting():
    file_header = FileHeader.from_text(
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP                       "
    )
    file_header.errorCode = '0010'
    assert "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP        REJ00010       " == file_header.dumps()
