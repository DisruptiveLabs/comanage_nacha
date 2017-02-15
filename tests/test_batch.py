import pytest
from comanage_nacha import ServiceClassCodes
from comanage_nacha import TransactionCodes, Batch
from comanage_nacha.exceptions import EntryClosedError


def test_add_entry():
    batch = Batch(1)
    assert len(batch.entries) == 0

    entry = batch.add_entry()

    assert len(batch.entries) == 1
    assert batch.entries == [entry]


def test_calculate_total_batch_debit_entry():
    batch = Batch(1)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_DEBIT, amount=1234)
    batch.add_entry(transaction_code=TransactionCodes.SAVINGS_DEBIT, amount=4321)

    assert batch.calculate_total_batch_debit_entry() == 5555
    assert batch.calculate_total_batch_credit_entry() == 0


def test_calculate_total_batch_credit_entry():
    batch = Batch(1)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_CREDIT, amount=1234)
    batch.add_entry(transaction_code=TransactionCodes.SAVINGS_CREDIT, amount=4321)

    assert batch.calculate_total_batch_credit_entry() == 5555
    assert batch.calculate_total_batch_debit_entry() == 0


def test_entry_count():
    batch = Batch(1)
    assert batch.entry_count == 0
    batch.add_entry()
    assert batch.entry_count == 1
    batch.add_entry()
    batch.add_entry()
    assert batch.entry_count == 3
    assert [entry.entry_detail.trace_number for entry in batch.entries] == [1, 2, 3]


def test_entry_hash():
    batch = Batch(1)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_CREDIT, receiving_dfi_routing_number=123, amount=10000)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_DEBIT, receiving_dfi_routing_number=345, amount=20000)
    assert batch.entry_hash == '468'


def test_generate_control():
    batch = Batch(1)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_CREDIT, receiving_dfi_routing_number=123, amount=10000)
    entry = batch.add_entry(transaction_code=TransactionCodes.CHECKING_DEBIT, receiving_dfi_routing_number=345,
                            amount=20000)
    entry.add_addenda()
    batch.batch_number = 1
    batch.close()
    assert batch.batch_control.batch_number == 1
    assert batch.batch_control.total_batch_credit_entry_dollar_amount == 10000
    assert batch.batch_control.total_batch_debit_entry_dollar_amount == 20000
    assert batch.batch_control.entry_hash == '468'
    assert batch.batch_control.entry_addenda_count == 3


def test_auto_calculate_service_class_code_debits():
    batch = Batch(1)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_DEBIT, receiving_dfi_routing_number=123, amount=10000)
    batch.close()
    assert batch.batch_header.service_class_code == ServiceClassCodes.DEBITS


def test_auto_calculate_service_class_code_credits():
    batch = Batch(1)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_CREDIT, receiving_dfi_routing_number=123, amount=10000)
    batch.close()
    assert batch.batch_header.service_class_code == ServiceClassCodes.CREDITS


def test_auto_calculate_service_class_code_mixed():
    batch = Batch(1)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_DEBIT, receiving_dfi_routing_number=123, amount=10000)
    batch.add_entry(transaction_code=TransactionCodes.CHECKING_CREDIT, receiving_dfi_routing_number=123, amount=10000)
    batch.close()
    assert batch.batch_header.service_class_code == ServiceClassCodes.MIXED_DEBITS_CREDITS


def test_cannot_add_entry_after_close():
    batch = Batch(1)
    batch.close()
    with pytest.raises(EntryClosedError):
        batch.add_entry()


def test_lines():
    batch = Batch(1)
    assert len(list(batch.lines)) == 2
    batch.add_entry(receiving_dfi_routing_number='1')
    assert len(list(batch.lines)) == 3
