import unittest
import os
import xml.etree.ElementTree as ET
from .. import compile_jack as C
import xml_helper as XML_H
from .. import main

class TestMain(unittest.TestCase):



    def test_class(self):

        c = C.Compiler()
        file_path = os.getcwd() + '/tests/files/ClassT.xml'
        c.tag_generator = XML_H.XMLHelper.read_xml_tags(file_path)
        answ_string = '<class><keyword>class</keyword><identifier>Main</identifier><symbol>{</symbol><symbol>}</symbol></class>'
        xml = c.compile_class()
        str_xml = ET.tostring(xml, encoding='unicode')
        self.assertEqual(str_xml, answ_string)


    def test_symbol_table_class(self):

        c = main.Main().main('Class.jack')
        self.assertEquals(c.symbol_table,[])

        c = main.Main().main('ClassVar.jack')
        self.assertEquals(len(c.symbol_table), 3)

        answ = [{"name": "x", "type": "int", "kind": "field", "no": 0},
                {"name": "y", "type": "int", "kind": "field", "no": 1},
                {"name": "size", "type": "int", "kind": "field", "no": 2}]
        self.assertEquals(c.symbol_table, answ)

    def test_symbol_table_var(self):

        c = main.Main().main('Var_dec2.jack')
        self.assertEquals(len(c.symbol_table), 4)

        answ = [{"name": "a", "type": "Array", "kind": "local", "no": 0},
                {"name": "length", "type": "int", "kind": "local", "no": 1},
                {"name": "i", "type": "int", "kind": "local", "no": 2},
                {"name": "sum", "type": "int", "kind": "local", "no": 3}]
        self.assertEquals(c.symbol_table, answ)

    def test_symbol_table_arg(self):

        c = main.Main().main('Subroutine_let.jack')
        self.assertEquals(len(c.symbol_table), 3)

        answ = [{"name": "Ax", "type": "int", "kind": "argument", "no": 0},
                {"name": "Ay", "type": "int", "kind": "argument", "no": 1},
                {"name": "Asize", "type": "int", "kind": "argument", "no": 2}]
        self.assertEquals(c.symbol_table, answ)
