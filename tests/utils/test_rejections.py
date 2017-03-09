from comanage_nacha import Parser
from comanage_nacha.utils import rejection

large_file_with_addenda = (
    "101  9100001912737206971506161217A094101WELLSFARGO             COMANAGELLC\n"
    "5200COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001\n"
    "6271221052785005486880       0000082100               JANE DOE                0001237370000001\n"
    "6271221052786886896684       0000864107               JANE DOE                0001237370000002\n"
    "6223221747951228713          0000220000               SOME CLEANERS           0001237370000003\n"
    "622122100024785323353        0000020125               SOME HVAC COMPANY       0001237370000004\n"
    "820000000400688485350000009462070000002401251234567890                         001237370000001\n"
    "5220COMANAGELLC     ACH SETTLEMENT      1234567890PPDPAYMENT         150616   1001237370000002\n"
    "6221221052789886521146       0000101832               HANDYMAN                0001237370000001\n"
    "6221221052789886521146       0000069863               HANDYMAN                1001237370000002\n"
    "705                                                                                00010000002\n"
    "822000000300244210540000000000000000001716951234567890                         001237370000002\n"
    "9000002000002000000070093269589000000946207000000411820"
)


def test_file_rejection():
    nacha = Parser().parse(large_file_with_addenda)
    rejection.file_rejection(nacha)
    assert nacha.error_code
    assert all(batch.error_code is not None
               for batch in nacha.batches)
    assert all(entry.error_code is not None
               for batch in nacha.batches
               for entry in batch.entries)
    assert all(addenda.error_code is not None
               for batch in nacha.batches
               for entry in batch.entries
               for addenda in entry.addenda)

    rejected_lines = list(rejection.filter_rejection_lines(nacha.lines))
    nacha = Parser.lines_to_nacha_file(rejected_lines)
    assert all(batch.error_code is not None for batch in nacha.batches)
    assert len(list(nacha.lines))


def test_batch_rejection():
    nacha = Parser().parse(large_file_with_addenda)
    rejection.batch_rejection(nacha)

    assert not nacha.error_code
    assert any(batch.error_code is not None
               for batch in nacha.batches)
    rejected_batches = filter(lambda batch: batch.error_code is not None, nacha.batches)
    assert all(entry.error_code is not None
               for batch in rejected_batches
               for entry in batch.entries)
    assert all(addenda.error_code is not None
               for batch in rejected_batches
               for entry in batch.entries
               for addenda in entry.addenda)

    rejected_lines = list(rejection.filter_rejection_lines(nacha.lines))
    nacha = Parser.lines_to_nacha_file(rejected_lines)
    assert all(batch.error_code is not None for batch in nacha.batches)


def test_entry_rejection():
    nacha = Parser().parse(large_file_with_addenda)
    rejection.entry_rejection(nacha)
    assert not nacha.error_code
    assert not any(batch.error_code is not None
                   for batch in nacha.batches)
    rejected_entries = filter(lambda entry: entry.error_code is not None,
                              [entry
                               for batch in nacha.batches
                               for entry in batch.entries])
    assert all(entry.error_code is not None
               for entry in rejected_entries)
    assert all(addenda.error_code is not None
               for entry in rejected_entries
               for addenda in entry.addenda)

    rejected_lines = list(rejection.filter_rejection_lines(nacha.lines))
    nacha = Parser.lines_to_nacha_file(rejected_lines)
    assert all(entry.error_code is not None
               for batch in nacha.batches
               for entry in batch.entries)


def test_addenda_rejection():
    nacha = Parser().parse(large_file_with_addenda)
    rejection.addenda_rejection(nacha)
    assert not nacha.error_code
    assert all(batch.error_code is None
               for batch in nacha.batches)
    assert all(entry.error_code is None
               for batch in nacha.batches
               for entry in batch.entries)
    assert any(addenda.error_code is not None
               for batch in nacha.batches
               for entry in batch.entries
               for addenda in entry.addenda)

    rejected_lines = list(rejection.filter_rejection_lines(nacha.lines))
    nacha = Parser.lines_to_nacha_file(rejected_lines)
    assert all(addenda.error_code is not None
               for batch in nacha.batches
               for entry in batch.entries
               for addenda in entry.addenda)


def test_filtering_non_rejected_file_has_header_and_control():
    nacha = Parser().parse(large_file_with_addenda)
    rejected_lines = list(rejection.filter_rejection_lines(nacha.lines))
    assert 2 == len(rejected_lines)


def test_random_rejection():
    for _ in range(100):
        # Run this a bunch of times since its random
        nacha = Parser().parse(large_file_with_addenda)
        rejection.random_reject(nacha)

        assert nacha.error_code or \
               any(batch.error_code is not None
                   for batch in nacha.batches) or \
               any(entry.error_code is not None
                   for batch in nacha.batches
                   for entry in batch.entries) or \
               any(addenda.error_code is not None
                   for batch in nacha.batches
                   for entry in batch.entries
                   for addenda in entry.addenda)
