from unittest2 import TestCase

from comanage_nacha.parser import Parser
from tests.lib import with_fixture


class ParserTestCase(TestCase):
    @with_fixture('simple.ach')
    def test_parse(self, data):
        parser = Parser()
        list(parser.parse(data))

    @with_fixture('large.ach')
    def test_large(self, data):
        parser = Parser()
        list(parser.parse(data))
