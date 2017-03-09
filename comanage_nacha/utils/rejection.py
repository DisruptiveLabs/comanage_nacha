import random

from comanage_nacha import Parser
from ..error_codes import REJECTION_REASONS


def filter_rejection_lines(lines):
    """
    Filter lines to create a rejection only file.

    All parents or children of a rejected line are returned,

    :param lines:
    :return:
    """
    nacha = Parser.lines_to_nacha_file(lines)

    if not nacha.error_code:
        for batch in list(nacha.batches):
            if not batch.error_code:
                for entry in list(batch.entries):
                    if not entry.error_code:
                        for addenda in list(entry.addenda):
                            if not addenda.error_code:
                                entry.addenda.remove(addenda)
                        if not entry.addenda:
                            batch.entries.remove(entry)
                if not batch.entries:
                    nacha.batches.remove(batch)
        if not nacha.batches:
            return [nacha.file_header,
                    nacha.file_control]

    return nacha.lines


def file_rejection(nacha, error_code=None):
    if not error_code:
        error_code = filter(lambda code: code[0] in '019', REJECTION_REASONS.keys())
    nacha.set_error_code(error_code)


def batch_rejection(nacha, error_code=None):
    if not error_code:
        error_code = filter(lambda code: code[0] in '58', REJECTION_REASONS.keys())
    random.choice(nacha.batches).set_error_code(error_code)


def entry_rejection(nacha, error_code=None):
    if not error_code:
        error_code = filter(lambda code: code[0] in '6', REJECTION_REASONS.keys())
    all_entries = [entry
                   for batch in nacha.batches
                   for entry in batch.entries]
    random.choice(all_entries).set_error_code(error_code)


def addenda_rejection(nacha, error_code=None):
    if not error_code:
        error_code = filter(lambda code: code[0] in '7', REJECTION_REASONS.keys())
    all_addenda = [addenda
                   for batch in nacha.batches
                   for entry in batch.entries
                   for addenda in entry.addenda]
    random.choice(all_addenda).set_error_code(error_code)


weighted_methods = sum(([method] * weight for weight, method in [
    (10, file_rejection),
    (20, batch_rejection),
    (40, entry_rejection),
]), [])


def random_reject(nacha):
    return random.choice(weighted_methods)(nacha)
