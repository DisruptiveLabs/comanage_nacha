from comanage_nacha.entries.entrybase import EntryBase


class BlockingFileControl(EntryBase):
    code = '9'
    format = (
        '9' * 94
    )

    def loads(self, line):
        raise NotImplementedError
