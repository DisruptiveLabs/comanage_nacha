import datetime

from comanage_nacha import TransactionCodes, ServiceClassCodes
from comanage_nacha.nacha_file import NachaFile


def test_context_manager():
    with NachaFile(company_name='COMANAGE LLC',
                   file_id_modifier='A',
                   file_creation_date=datetime.date.today(),
                   file_creation_time=datetime.datetime.utcnow()) as nacha:
        with nacha.add_batch(service_class_code=ServiceClassCodes.MIXED_DEBITS_CREDITS,
                             company_name='COMANAGE LLC',
                             company_id='0123456789',
                             effective_entry_date=datetime.date.today()) as batch:
            with batch.add_entry(transaction_code=TransactionCodes.CHECKING_CREDIT,
                                 receiving_dfi_routing_number='09100001',
                                 routing_number_check_digit=0,
                                 receiving_dfi_account_number='0123456789',
                                 amount=10000,
                                 individual_id='123',
                                 individual_name='FRANK') as entry:
                pass
    print(nacha.render_to_string())
    assert '\n'.join(map(str, nacha.lines))
