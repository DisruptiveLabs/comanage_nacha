class Entry:
    code = '0'
    format = '0'

    def loads(self, line):
        pass

    def dumps(self):
        dikt = self.__class__.__dict__.copy()
        dikt.update(self.__dict__)
        return self.format.format(**dikt)

    def __str__(self):
        return self.dumps()

    @classmethod
    def from_text(cls, text):
        instance = cls()
        instance.loads(text)
        return instance


__all__ = ['Entry']
