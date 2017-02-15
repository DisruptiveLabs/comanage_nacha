import six


class EnumMeta(type):
    def __new__(cls, what, bases, dikt):
        for k, v in list(dikt.items()):
            dikt[v] = k
        return type(what, bases, dikt)(dikt)


Enum = six.with_metaclass(EnumMeta, dict)


class ConfirmationMessageCodes(Enum):
    NO_MESSAGE = ''
    FILE_RECEIVED = '01'
    FILE_INVALID_ENTRY_DATES = '02'
    FILE_CONTROL_TOTALS_INCORRECT = '03'
    FILE_FAILED_SECONDARY_EDIT = '04'
    FILE_SEVERE_ERRORS = '05'
    FILE_DUPLICATE_QUALIFIER = '06'
    FILE_NEW_QUAILIFIER_ASSIGNED = '07'
    FILE_TEST_NOT_PROCESSED = 'TT'


class ServiceClassCodes(Enum):
    MIXED_DEBITS_CREDITS = 200
    CREDITS = 220
    DEBITS = 225


class StandardEntryClasses(Enum):
    ARC = 'ARC'  # Accounts Receivable Entry
    CIE = 'CIE'  # Customer Initiated Entry
    MTE = 'MTE'  # Machine Transfer Entry
    PBR = 'PBR'  # Consumer Cross-Border Payment
    POP = 'POP'  # Point-of-Purchase
    PPD = 'PPD'  # Prearranged Payment & Deposit
    POS = 'POS'  # Point of Sale Entry/Shared Network Transaction
    SHR = 'SHR'  # Point of Sale Entry/Shared Network Transaction
    RCK = 'RCK'  # Re-presented Check Entry
    TEL = 'TEL'  # Telephone-Initiated Entry
    WEB = 'WEB'  # Internet-Initiated Entry
    CBR = 'CBR'  # Corporate Cross-Border Payment
    CCD = 'CCD'  # Cash Concentration or Disbursement
    CTX = 'CTX'  # Corporate Trade Exchange
    ACK = 'ACK'  # Acknowledgment Entries
    ATX = 'ATX'  # Acknowledgment Entries
    ADV = 'ADV'  # Automated Accounting Advice
    COR = 'COR'  # Automated Notification of Change or Refused Notification of Change
    DNE = 'DNE'  # Death Notification Entry
    ENR = 'ENR'  # Automated Enrollment Entry
    TRC = 'TRC'  # Truncated Entries
    TRX = 'TRX'  # Truncated Entries
    XCK = 'XCK'  # Destroyed Check Entry'


class TransactionCodes(Enum):
    # credit checking
    CHECKING_RETURNED_CREDIT = 21
    CHECKING_CREDIT = 22
    CHECKING_PRE_NOTE_CREDIT = 23

    # debit checking
    CHECKING_RETURNED_DEBIT = 26
    CHECKING_DEBIT = 27
    CHECKING_PRE_NOTE_DEBIT = 28

    # credit savings
    SAVINGS_RETURNED_CREDIT = 31
    SAVINGS_CREDIT = 32
    SAVINGS_PRE_NOTE_CREDIT = 33

    # debit savings
    SAVINGS_RETURNED_DEBIT = 36
    SAVINGS_DEBIT = 37
    SAVINGS_PRE_NOTE_DEBIT = 38
