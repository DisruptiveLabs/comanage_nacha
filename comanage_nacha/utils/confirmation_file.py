confirmation_file_entry_codes = ('1', '5', '8', '9')


def filter_confirmation_lines(lines):
    return filter(lambda line: line.code in confirmation_file_entry_codes, lines)
