from .entries import entry_types
from .nacha_file import NachaFile


class Parser(object):
    _blocking_file_control_record = '9' * 94

    def __init__(self, confirmation_file=False, rejection_file=False, returns_file=False):
        self.confirmation_file = confirmation_file
        self.rejection_file = rejection_file

    def parse_lines(self, file_data):
        lines = file_data.split('\n')

        for line in lines:
            if line.strip() == Parser._blocking_file_control_record:
                # There shouldn't be any content after a blocking control record
                break

            code = line[0]
            entry = entry_types[code].from_text(line)
            yield entry

    def parse(self, file_data):
        """
        {'1': entries.FileHeader,
         '5': entries.CompanyBatchHeader,
         '6': entries.EntryDetail,
         '7': entries.EntryAddenda,
         '8': entries.CompanyBatchControl,
         '9': entries.FileControl}
        :param file_data:
        :return:
        """
        return self.lines_to_nacha_file(self.parse_lines(file_data))

    @staticmethod
    def lines_to_nacha_file(lines):
        nacha_file = None

        for line in lines:
            assert line.code in entry_types.keys(), 'Line code {} not known'.format(line.code)

            if line.code == '1':
                nacha_file = NachaFile(file_header=line)
            elif line.code == '5':
                nacha_file.add_batch(batch_header=line)
            elif line.code == '6':
                nacha_file \
                    .batches[-1].add_entry(entry_detail=line)
            elif line.code == '7':
                nacha_file \
                    .batches[-1] \
                    .entries[-1].add_addenda(entry_addenda=line)
            elif line.code == '8':
                nacha_file \
                    .batches[-1].batch_control = line
            elif line.code == '9':
                nacha_file.file_control = line

        return nacha_file


parser = Parser()
parse_lines = parser.parse_lines
parse = parser.parse
