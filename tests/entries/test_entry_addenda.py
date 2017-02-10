from comanage_nacha.entries.entry_addenda import EntryAddenda


def test_loads():
    addenda = EntryAddenda.from_text(
        '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00201000040000001'
    )
    assert 5 == addenda.addenda_type_code
    assert 4 == addenda.addenda_sequence_number
    assert 1 == addenda.entry_detail_sequence_number
    assert '0*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*002010' == addenda.payment_information


def test_dumps():
    addenda = EntryAddenda()
    addenda.addenda_type_code = 5
    addenda.addenda_sequence_number = 4
    addenda.entry_detail_sequence_number = 1
    addenda.payment_information = '0*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*002010'
    assert '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00201000040000001' == addenda.dumps()


def test_reject():
    addenda = EntryAddenda.from_text(
        '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00REJ060300000001')
    assert addenda.rejected
    assert '6030' == addenda.error_code
    assert '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00REJ060300000001' == addenda.dumps()


def test_rejecting():
    addenda = EntryAddenda.from_text(
        '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00201000040000001')
    addenda.error_code = '1234'
    assert '7050*U*00307*000000183*0*P*:\GS*RA*9133131313*6126127272*20000888*0830*183*T*00REJ012340000001' == addenda.dumps()
