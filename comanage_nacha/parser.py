from .entries import entry_types


class Parser(object):
    _blocking_file_control_record = '9' * 94

    def __init__(self, confirmation_file=False, rejection_file=False):
        self.confirmation_file = confirmation_file
        self.rejection_file = rejection_file

    def parse(self, file_data):
        lines = file_data.split('\n')

        for line in lines:
            if line.strip() == Parser._blocking_file_control_record:
                # There shouldn't be any content after a blocking control record
                break

            code = line[0]
            entry = entry_types[code].from_text(line)
            yield entry


parser = Parser()
parse = parser.parse
