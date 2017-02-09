class Entry:
    code = '0'
    format = '0'
    errorCode = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise KeyError("{} has no attribute {}".format(self.__class__.__name__, key))
            setattr(self, key, value)

    def __str__(self):
        return self.dumps()

    def loads(self, line):
        pass

    def dumps(self):
        dikt = self.__class__.__dict__.copy()
        dikt.update(self.__dict__)
        dumped = self.format.format(**dikt)

        if self.rejected:
            return (
                dumped[:79] +
                'REJ0' +
                self.errorCode +
                dumped[87:]
            )
        return dumped

    @classmethod
    def from_text(cls, text):
        instance = cls()
        instance.loads(text)
        return instance

    @property
    def rejected(self):
        return hasattr(self, 'errorCode') and self.errorCode is not None


__all__ = ['Entry']
