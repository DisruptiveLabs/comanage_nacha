from comanage_nacha import Parser
from comanage_nacha.entries import EntryAddendaNotificationOfChange, EntryAddendaReturned

empty_returns_file = (
    "10112345678   0910000190909140528A094101WELLS FARGO            WELLS FARGO BANK\n"
    "9000000000001000000000000000000000000000000000000000000"
)

large_returns_file = (
    "1011234567890 0910000190909140559A094101ABC COMPANY            WELLS FARGO BANK\n"
    "5200ABC COMPANY                         2222222222PPDPREMIUM   SEP 120909120001091000017000001\n"
    "6260515012990123456          00000018130001234        BOB B BROWN SR          1091000010111111\n"
    "799R08091000010111111      05150129                                            091000010001234\n"
    "820000000200051501290000000018130000000000002222222222                         091000010000001\n"
    "5200ABC COMPANY               (R)       2222222222PPDPREMIUM   SEP 120909120001091000019000002\n"
    "6262642790914321123443       00000050000001333        RONALD REED             1091000010222222\n"
    "799R01091000010222222      26427909                                            091000010002345\n"
    "820000000200264279090000000050000000000000002222222222                         091000010000002\n"
    "5200ABC COMPANY                         1111111111PPDPREMIUM   SEP 120909120001091000017000003\n"
    "6260841006385656565          00000039920001357        SHERYL S SMITH          1091000010333333\n"
    "799R07091000010333333      08410063                                            091000010003456\n"
    "820000000200084100630000000039920000000000001111111111                         091000010000003\n"
    "5200ABC COMPANY                         1111111111PPDPREMIUM   SEP 120909120001091000017000004\n"
    "6261211330050120120120       00000000000001579        WAYNE WILSON            1091000010444444\n"
    "798C02091000010444444      12113300121140218                                   091000010004567\n"
    "820000000200121133000000000000000000000000001111111111                         091000010000004\n"
    "5200ABC COMPANY                         2222222222PPDPREMIUM   SEP 120909120001091000017000005\n"
    "6260653054369898989898       00000000000002345        GEORGE GONZALES         1091000010555555\n"
    "798C05091000010555555      0653054337                                          091000010005678\n"
    "820000000200065305430000000000000000000000002222222221                         091000010000005\n"
    "9000005000003000000100058631944000000010805000000000000"
)

returns_parser = Parser(returns_file=True)


def test_parse_lines_return_file():
    assert list(returns_parser.parse_lines(large_returns_file))


def test_parse_return_file():
    nacha = returns_parser.parse(large_returns_file)
    assert nacha.batch_count == 5
    assert all(batch.entry_count == 1 for batch in nacha.batches)
    addenda_1 = nacha.batches[0].entries[0].addenda[0].entry_addenda
    addenda_2 = nacha.batches[1].entries[0].addenda[0].entry_addenda
    addenda_3 = nacha.batches[2].entries[0].addenda[0].entry_addenda
    addenda_4 = nacha.batches[3].entries[0].addenda[0].entry_addenda
    addenda_5 = nacha.batches[4].entries[0].addenda[0].entry_addenda
    assert isinstance(addenda_1, EntryAddendaReturned)
    assert isinstance(addenda_2, EntryAddendaReturned)
    assert isinstance(addenda_3, EntryAddendaReturned)
    assert isinstance(addenda_4, EntryAddendaNotificationOfChange)
    assert isinstance(addenda_5, EntryAddendaNotificationOfChange)
    assert addenda_1.return_reason_code == 'R08'
    assert addenda_2.return_reason_code == 'R01'
    assert addenda_3.return_reason_code == 'R07'
    assert addenda_4.return_reason_code == 'C02'
    assert addenda_5.return_reason_code == 'C05'
    assert addenda_1.return_reason
    assert addenda_2.return_reason
    assert addenda_3.return_reason
    assert addenda_4.return_reason
    assert addenda_5.return_reason


def test_parse_lines_empty_file():
    assert list(returns_parser.parse_lines(empty_returns_file))


def test_parse_empty_file():
    nacha = returns_parser.parse(empty_returns_file)
    assert nacha.batch_count == 0
