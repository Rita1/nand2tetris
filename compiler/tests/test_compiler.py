import unittest
import os
import xml.etree.ElementTree as ET
from .. import compile_jack as C
import xml_helper as XML_H
from .. import main

class TestMain(unittest.TestCase):


    def answers(self, parsed_file, answer):

        file_result = os.getcwd() + parsed_file
        file_answer = os.getcwd() + answer
        f_result = open(file_result, 'r')
        f_answer = open(file_answer, 'r')

        for line in f_result:
            ln = f_answer.readline()
            ln = ln.split("//")[0]
            ln = ln.strip() + '\n'
            self.assertEqual(line, ln)

        for line in f_answer:
            ln = f_result.readline()
            ln = ln.split("//")[0]
            ln = ln.strip() + '\n'
            self.assertEqual(line, ln)

        f_result.close()
        f_answer.close()

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
        print("C", c)
        self.assertEquals(c.symbol_table,[])

        c1 = main.Main().main('ClassVar.jack')
        self.assertEquals(len(c1.symbol_table), 3)
        print("C1", c1)
        answ = [{"name": "x", "type": "int", "kind": "field", "no": 0},
                {"name": "y", "type": "int", "kind": "field", "no": 1},
                {"name": "size", "type": "int", "kind": "field", "no": 2}]
        self.assertEquals(c1.symbol_table, answ)

    def test_symbol_table_var(self):

        c2 = main.Main().main('Var_dec2.jack')
        # self.assertEquals(len(c2.symbol_table), 4)

        answ = [{"name": "a", "type": "Array", "kind": "local", "no": 0},
                {"name": "length", "type": "int", "kind": "local", "no": 1},
                {"name": "i", "type": "int", "kind": "local", "no": 2},
                {"name": "sum", "type": "int", "kind": "local", "no": 3}]
        self.assertEquals(c2.symbol_table_method, answ)

    def test_symbol_table_arg(self):

        c3 = main.Main().main('Subroutine_let.jack')
        self.assertEquals(len(c3.symbol_table_method), 3)
        print("C3", c3)
        answ = [{"name": "Ax", "type": "int", "kind": "argument", "no": 0},
                {"name": "Ay", "type": "int", "kind": "argument", "no": 1},
                {"name": "Asize", "type": "int", "kind": "argument", "no": 2}]
        self.assertEquals(c3.symbol_table_method, answ)

    def test_symbol_table_full(self):

        c = main.Main().main('Square/Main.jack')
        answ = [{"name": "test", "type": "boolean", "kind": "static", "no": 0}]
        answ_method = [{"name": "i", "type": "int", "kind": "local", "no": 0},
                       {"name": "j", "type": "int", "kind": "local", "no": 1},
                       {"name": "s", "type": "String", "kind": "local", "no": 2},
                       {"name": "a", "type": "Array", "kind": "local", "no": 3}]

        self.assertEquals(c.symbol_table, answ)
        self.assertEquals(c.symbol_table_method, answ_method)

    def test_seven(self):
        c = main.Main().main('Seven')

        self.answers("/tests/files/Seven/Main.vm", "/tests/files/Seven/Main_answ.vm")

        