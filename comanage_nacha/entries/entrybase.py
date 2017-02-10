import abc
import six

from comanage_nacha.error_codes import REJECTION_REASONS


class EntryBase(six.with_metaclass(abc.ABCMeta)):
    code = '0'
    format = '0'
    error_code = None

    @abc.abstractmethod
    def loads(self, line):
        raise NotImplementedError

    def dumps(self):
        dikt = self.__class__.__dict__.copy()
        dikt.update(self.__dict__)
        dumped = self.format.format(**dikt)

        if self.rejected:
            return (
                dumped[:79] +
                'REJ0' +
                self.error_code +
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
        return hasattr(self, 'error_code') and self.error_code is not None

    @property
    def error_reason(self):
        return hasattr(self, 'error_code') and REJECTION_REASONS.get(self.error_code, None)


__all__ = ['EntryBase']
