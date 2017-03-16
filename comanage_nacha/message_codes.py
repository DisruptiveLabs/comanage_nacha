MESSAGE_CODES = {
    '01': 'Your file has been received by Wells Fargo. It will be processed subject to standard ACH validation.',
    '02': 'Your file contains invalid effective entry dates. If you have questions,'
          ' please contact Wells Fargo ACH Services immediately.',
    '03': 'Your control totals do not agree with the total of your detail items.'
          ' Wells Fargo will process the transactions we have received.'
          ' If you do not want this file to be processed, please contact Wells Fargo ACH Services immediately.',
    '04': 'Your file failed a secondary edit. Wells Fargo cannot process your ACH file as received.'
          ' Please contact Wells Fargo ACH Services immediately.',
    '05': 'Severe error while trying to store your file on Wells Fargo\'s Transaction Depository.'
          ' Please contact Wells Fargo ACH Services immediately. Your file failed our initial edit.'
          ' Wells Fargo cannot process your ACH file as received.'
          ' Please contact Wells Fargo ACH Services immediately.',
    '06': 'A file with a duplicate qualifier was received.'
          ' This file and any previous files will continue through normal processing.'
          ' If this file or an earlier file was sent in error, please contact Wells Fargo ACH Services immediately.',
    '07': 'A file with a duplicate qualifier was received and a new qualifier xxxxxx has been assigned'
          ' based on time of file receipt. This file and any previous files will continue through normal processing.'
          ' If this file or an earlier file was sent in error, please contact Wells Fargo ACH Services immediately.',
    'TT': 'This is a test file and will not be processed in production.',
}

FAILURE_MESSAGE_CODES = set(['04', '05'])
