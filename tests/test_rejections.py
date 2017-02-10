from comanage_nacha.nacha_file import NachaFile


def test_file_rejections():
    nacha = NachaFile()
    batch = nacha.add_batch()
    entry = batch.add_entry()
    addenda = entry.add_addenda()
    assert nacha.file_header.error_code is None
    assert batch.batch_header.error_code is None
    assert entry.entry_detail.error_code is None
    assert addenda.entry_addenda.error_code is None
    nacha.set_error_code('0010')
    assert nacha.file_header.error_code == '0010'
    assert batch.batch_header.error_code == '0010'
    assert entry.entry_detail.error_code == '0010'
    assert addenda.entry_addenda.error_code == '0010'
    new_batch = nacha.add_batch()
    assert new_batch.batch_header.error_code == '0010'


def test_batch_rejections():
    nacha = NachaFile()
    batch = nacha.add_batch()
    entry = batch.add_entry()
    addenda = entry.add_addenda()
    assert nacha.file_header.error_code is None
    assert batch.batch_header.error_code is None
    assert entry.entry_detail.error_code is None
    assert addenda.entry_addenda.error_code is None
    batch.set_error_code('0010')
    assert nacha.file_header.error_code is None
    assert batch.batch_header.error_code == '0010'
    assert entry.entry_detail.error_code == '0010'
    assert addenda.entry_addenda.error_code == '0010'
    new_batch = nacha.add_batch()
    assert new_batch.batch_header.error_code is None


def test_entry_rejections():
    nacha = NachaFile()
    batch = nacha.add_batch()
    entry = batch.add_entry()
    addenda = entry.add_addenda()
    assert nacha.file_header.error_code is None
    assert batch.batch_header.error_code is None
    assert entry.entry_detail.error_code is None
    assert addenda.entry_addenda.error_code is None
    entry.set_error_code('0010')
    assert nacha.file_header.error_code is None
    assert batch.batch_header.error_code is None
    assert entry.entry_detail.error_code == '0010'
    assert addenda.entry_addenda.error_code == '0010'
    new_entry = batch.add_entry()
    assert new_entry.entry_detail.error_code is None
    new_batch = nacha.add_batch()
    assert new_batch.batch_header.error_code is None
