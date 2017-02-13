import datetime

from comanage_nacha.nacha_file import NachaFile


def test_context_manager():
    with NachaFile(company_name='COMANAGE LLC',
                   file_id_modifier='A',
                   file_creation_date=datetime.date.today(),
                   file_creation_time=datetime.datetime.utcnow()) as nacha:
        with nacha.add_batch(service_class_code=200,
                             company_name='COMANAGE LLC',
                             company_id='0123456789',
                             effective_entry_date=datetime.date.today()) as batch:
            batch.add_entry(transaction_code=22,
                            receiving_dfi_routing_number='09100001',
                            routing_number_check_digit=0,
                            receiving_dfi_account_number='0123456789',
                            amount=10000,
                            individual_id='123',
                            individual_name='FRANK')
    print(nacha.render_to_string())
