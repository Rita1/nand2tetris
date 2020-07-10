import unittest
import os
import xml.etree.ElementTree as ET
from .. import compile_jack as C
import xml_helper as XML_H

class TestMain(unittest.TestCase):

    def check_answers(self, file_name, answ_string):
        pass

    def test_class(self):

        c = C.Compiler()
        file_path = os.getcwd() + '/tests/files/ClassT.xml'
        c.tag_generator = XML_H.XMLHelper.read_xml_tags(file_path)
        answ_string = '<class><keyword>class</keyword><identifier>Main</identifier><symbol>{</symbol><symbol>}</symbol></class>'
        xml = c.compile_class()
        str_xml = ET.tostring(xml, encoding='unicode')
        self.assertEqual(str_xml, answ_string)

    # def test_subroutine(self):
    #
    #     c = C.Compiler()
    #     file_path = os.getcwd() + '/tests/files/Subroutine_simpleT.xml'
    #     c.tag_generator = XML_H.XMLHelper.read_xml_tags(file_path)
    #
    #     answ_string = '<class><keyword>class</keyword><identifier>Main</identifier><symbol>{</symbol><symbol>}</symbol></class>'
