from comanage_nacha import NachaFile


def test_file_rejections():
    nacha = NachaFile()
    batch = nacha.add_batch()
    entry = batch.add_entry()
    addenda = entry.add_addenda()
    assert nacha.error_code is None
    assert batch.error_code is None
    assert entry.error_code is None
    assert addenda.error_code is None
    nacha.error_code = '0010'
    assert nacha.error_code == '0010'
    assert batch.error_code == '0010'
    assert entry.error_code == '0010'
    assert addenda.error_code == '0010'
    new_batch = nacha.add_batch()
    assert new_batch.error_code == '0010'


def test_batch_rejections():
    nacha = NachaFile()
    batch = nacha.add_batch()
    entry = batch.add_entry()
    addenda = entry.add_addenda()
    assert nacha.error_code is None
    assert batch.error_code is None
    assert entry.error_code is None
    assert addenda.error_code is None
    batch.error_code = '0010'
    assert nacha.error_code is None
    assert batch.error_code == '0010'
    assert entry.error_code == '0010'
    assert addenda.error_code == '0010'
    new_batch = nacha.add_batch()
    assert new_batch.error_code is None


def test_entry_rejections():
    nacha = NachaFile()
    batch = nacha.add_batch()
    entry = batch.add_entry()
    addenda = entry.add_addenda()
    assert nacha.error_code is None
    assert batch.error_code is None
    assert entry.error_code is None
    assert addenda.error_code is None
    entry.error_code = '0010'
    assert nacha.error_code is None
    assert batch.error_code is None
    assert entry.error_code == '0010'
    assert addenda.error_code == '0010'
    new_entry = batch.add_entry()
    assert new_entry.error_code is None
    new_batch = nacha.add_batch()
    assert new_batch.error_code is None


def test_addenda_rejection():
    nacha = NachaFile()
    batch = nacha.add_batch()
    entry = batch.add_entry()
    addenda = entry.add_addenda()
    assert nacha.error_code is None
    assert batch.error_code is None
    assert entry.error_code is None
    assert addenda.error_code is None
    addenda.error_code = '0010'
    assert nacha.error_code is None
    assert batch.error_code is None
    assert entry.error_code is None
    assert addenda.error_code == '0010'
    new_entry = batch.add_entry()
    assert new_entry.error_code is None
    new_batch = nacha.add_batch()
    assert new_batch.error_code is None

