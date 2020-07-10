import unittest
import os
from os import path
from .. import xml_helper as x

class TestMain(unittest.TestCase):

    def test_xml(self):

        file_path = os.getcwd() + '/tests/files/Xml.xml'
        gen = x.XMLHelper.read_xml_tags(file_path)
        tag = next(gen)
        answ = ('keyword', 'var')
        self.assertEqual(tag, answ)

        tag = next(gen)
        answ = ('keyword', 'int')
        self.assertEqual(tag, answ)

        tag = next(gen)
        answ = ('identifier', 'i')
        self.assertEqual(tag, answ)