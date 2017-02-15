from comanage_nacha import NachaFile, TransactionCodes
from comanage_nacha.utils.confirmation_file import filter_confirmation_lines


def test_build_confirmation_file():
    with NachaFile() as nacha:
        with  nacha.add_batch() as     batch:
            batch.add_entry(receiving_dfi_routing_number='12345678',
                            transaction_code=TransactionCodes.CHECKING_CREDIT,
                            amount=10000)
            batch.add_entry(receiving_dfi_routing_number='12345678',
                            transaction_code=TransactionCodes.CHECKING_CREDIT,
                            amount=10000)
            batch.add_entry(receiving_dfi_routing_number='12345678',
                            transaction_code=TransactionCodes.CHECKING_DEBIT,
                            amount=33300)
    lines = nacha.lines
    confirmation_lines = filter_confirmation_lines(lines)
    assert {'1', '5', '8', '9'} == set(line.code for line in confirmation_lines)
