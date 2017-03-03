from comanage_nacha import NachaFile
from comanage_nacha.entries import FileControl, EntryDetail
from comanage_nacha.parser import Parser

parser = Parser()
confirmation_parser = Parser(confirmation_file=True)
rejection_parser = Parser(rejection_file=True)

simple = ("101  9100001912737206971506161208A094101WELLSFARGO             COMANAGELLC\n"
          "5225COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001\n"
          "6271221052785005486880       0000082100               JANE DOE                0001237370000001\n"
          "822500000100122105270000000821000000000000001234567890                         001237370000001\n"
          "9000001000001000000010012210527000000082100000000000000\n"
          "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
          "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
          "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
          "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
          "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999")


def test_parse_lines_simple():
    # Just test it doesnt throw exceptions basically
    list(parser.parse_lines(simple))


def test_parse_simple():
    nacha = parser.parse(simple)
    nacha.include_blocking_lines = False
    assert isinstance(nacha, NachaFile)
    assert len(list(nacha.lines)) == 5


large = """101  9100001912737206971506161217A094101WELLSFARGO             COMANAGELLC
5200COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001
6271221052785005486880       0000082100               JANE DOE                0001237370000001
6271221052786886896684       0000864107               JANE DOE                0001237370000002
6223221747951228713          0000220000               SOME CLEANERS           0001237370000003
622122100024785323353        0000020125               SOME HVAC COMPANY       0001237370000004
820000000400688485350000009462070000002401251234567890                         001237370000001
5220COMANAGELLC     ACH SETTLEMENT      1234567890PPDPAYMENT         150616   1001237370000002
6221221052789886521146       0000101832               HANDYMAN                0001237370000001
6221221052789886521146       0000069863               HANDYMAN                0001237370000002
822000000200244210540000000000000000001716951234567890                         001237370000002
9000002000002000000060093269589000000946207000000411820"""


def test_parse_lines_large():
    # Just test it doesnt throw exceptions basically
    list(parser.parse_lines(large))


def test_parse_large():
    nacha = parser.parse(large)
    nacha.include_blocking_lines = False
    assert isinstance(nacha, NachaFile)
    assert len(list(nacha.lines)) == 12


with_addenda = """101 091000019          1702161755A094101WELLS FARGO            COMANAGE LLC
5200COMANAGE LLC                        0123456789                   170216   1091000010000001
6220910000100123456789       0000010000123            FRANK                   1091000010000001
705                                                                                00010000001
820000000200091000010000000000000000000100000123456789                         091000010000000
9000001000001000000020009100001000000000000000000010000                                       """


def test_parse_lines_addenda():
    list(parser.parse_lines(with_addenda))


def test_parse_addenda():
    nacha = parser.parse(with_addenda)
    nacha.include_blocking_lines = False
    assert isinstance(nacha, NachaFile)
    assert len(list(nacha.lines)) == 6


confirmation = """101  9100001912737206971506161208A094101WELLSFARGO             COMANAGELLC
5225COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001
822500000100122105270000000821000000000000001234567890                         001237370000001
9000001000001000000010012210527000000082100000000000000"""


def test_parse_lines_confirmation():
    (file_header,
     batch_header,
     batch_control,
     file_control) = confirmation_parser.parse_lines(confirmation)
    assert isinstance(file_control, FileControl)
    assert file_control.message_codes == []


def test_parse_confirmation():
    confirmation_parser.parse(confirmation)


confirmation_message_codes = """101  9100001912737206971506161217A094101WELLSFARGO             COMANAGELLC
5200COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001
820000000400688485350000009462070000002401251234567890                         001237370000001
5220COMANAGELLC     ACH SETTLEMENT      1234567890PPDPAYMENT         150616   1001237370000002
822000000200244210540000000000000000001716951234567890                         001237370000002
9000002000002000000060093269589000000946207000000411820 0102TT"""


def test_confirmation_message_codes():
    (file_header,
     batch_header_1,
     batch_control_1,
     batch_header_2,
     batch_control_2,
     file_control) = confirmation_parser.parse_lines(confirmation_message_codes)
    assert isinstance(file_control, FileControl)
    assert file_control.message_codes == ['01', '02', 'TT']


entry_reject = """101  9100001912737206971506161217A094101WELLSFARGO             COMANAGELLC
5200COMANAGELLC     ACH SETTLEMENT      1234567890CCDPAYMENT         150616   1001237370000001
622122100024785323353        0000020125               SOME HVAC COMPANY       0REJ060010000004
820000000400688485350000009462070000002401251234567890                         001237370000001
9000002000002000000060093269589000000946207000000411820"""


def test_entry_reject():
    (file_header,
     batch_header,
     rejected_entry,
     batch_control,
     file_control) = rejection_parser.parse_lines(entry_reject)
    assert isinstance(rejected_entry, EntryDetail)
    assert rejected_entry.error_code == '6001'


def test_empty_reject_only_zero_items():
    # "empty" reject-only
    (file_header,
     file_control) = rejection_parser.parse_lines(
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP                       \n"
        "9000000000101000000000000000000000000000000000000000000                                       \n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999"
    )


def test_reject_only_file_five_rejected_items():
    (file_header,
     batch_header,
     entry_1,
     entry_2,
     entry_3,
     entry_4,
     entry_5,
     batch_control,
     file_control) = rejection_parser.parse_lines(
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP                       \n"
        "5200ABC CORP                     DEPOSIT9999999999PPDPAYABLES  091509090915   1091000012381268\n"
        "622771045912999999           00000125000116           C CHANG                 0REJ060300000002\n"
        "6225072003909999999999       00000233500485           D DAVIDSON              0REJ060300000019\n"
        "622541210032199999999999     00000100000989           E EDWARDS               0REJ060300000027\n"
        "622580101814499999           00000200001022           F FREEMAN               0REJ060300000030\n"
        "622507206213499999999        00000150001177           G GONZALES              0REJ060300000037\n"
        "820000000502906764350000000000000000000808509999999999                         091000012381356\n"
        "9000001000010000000050290676435000000000000000000080850                                       "
    )


def test_item_level_reject_origination():
    (file_header,
     batch_header,
     entry_1,
     entry_2,
     entry_3,
     entry_4,
     entry_5,
     batch_control,
     file_control) = rejection_parser.parse_lines(
        # Item-level reject
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP                       \n"
        "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1091000013841231\n"
        "622507003908999999           0000010000               CUSTOMER ONE            0REJ060300000001\n"
        "632091000019999999999        0000015000               CUSTOMER TWO            0091000014412012\n"
        "6221210002489999999999       0000020000               CUSTOMER THREE          0091000014412013\n"
        "6220910000199999999          0000012500               CUSTOMER FOUR           0091000014412014\n"
        "62209100001999999            0000017500               CUSTOMER FIVE           0091000014412015\n"
        "820000000509010041700000000000000000000650009999999999                         009100013841231\n"
        "900000100000100000050090100417000000000000000000065000                                        \n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999"
    )


def test_batch_level_reject_with_origination():
    (file_header,
     batch_header_1,
     entry_1,
     entry_2,
     batch_control_1,
     batch_header_2,
     entry_3,
     entry_4,
     batch_control_2,
     file_control) = rejection_parser.parse_lines(
        # Batch-level reject
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP                       \n"
        "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1REJ055803841231\n"
        "622507003908999999           0000010000               CUSTOMER ONE            0REJ055800000001\n"
        "632091000019999999999        0000015000               CUSTOMER TWO            0REJ055804412012\n"
        "820000002000598003910000000000000000000250009999999999                         REJ055803841231\n"
        "5200ABC CORP                            9999999999PPDPAYROLL   091509090915   1091000013841231\n"
        "6230910000199999999          0000012500               EMPLOYEE A              0009100014412014\n"
        "62309100001999999            0000017500               EMPLOYEE B              0009100014412015\n"
        "820000002000182000020000000000000000000300009999999999                         009100013841231\n"
        "900000200000100000040000780003930000000000000000055000                                        "
    )


def test_file_level_reject_with_origination():
    (file_header,
     batch_header_1,
     entry_1,
     entry_2,
     batch_control_1,
     batch_header_2,
     entry_3,
     entry_4,
     batch_control_2,
     file_control) = rejection_parser.parse_lines(
        # File-level reject
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP        REJ00010       \n"
        "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1REJ000103841231\n"
        "622507003908999999           0000010000               CUSTOMER ONE            0REJ000100000001\n"
        "632091000019999999999        0000015000               CUSTOMER TWO            0REJ000104412012\n"
        "820000002000598003910000000000000000000250009999999999                         REJ000103841231\n"
        "5200ABC CORP                            9999999999PPDPAYROLL   091509090915   1REJ000103841231\n"
        "6230910000199999999          0000012500               EMPLOYEE A              0REJ000104412014\n"
        "62309100001999999            0000017500               EMPLOYEE B              0REJ000104412015\n"
        "820000002000182000020000000000000000000300009999999999                         REJ000103841231\n"
        "900000200000100000040000780003930000000000000000055000                                        "
    )


def test_micr_split_item_with_origination():
    (file_header,
     batch_header,
     entry_1,
     entry_2,
     entry_3,
     entry_4,
     entry_5,
     batch_control,
     file_control) = rejection_parser.parse_lines(
        # MICR-Split item
        "101 09100001999999999990609141125A094101WELLS FARGO            ABC CORP                       \n"
        "5200ABC CORP                            9999999999PPDPAYABLES  091509090915   1091000013841231\n"
        "622507003908999999           0000010000               CUSTOMER ONE            0MICR60300000001\n"
        "632091000019999999999        0000015000               CUSTOMER TWO            0091000014412012\n"
        "6221210002489999999999       0000020000               CUSTOMER THREE          0091000014412013\n"
        "6220910000199999999          0000012500               CUSTOMER FOUR           0091000014412014\n"
        "62209100001999999            0000017500               CUSTOMER FIVE           0091000014412015\n"
        "820000005009010041700000000000000000000650009999999999                         009100013841231\n"
        "900000100000100000050090100417000000000000000000065000                                        \n"
        "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999"
    )
