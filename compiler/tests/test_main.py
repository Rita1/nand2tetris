import unittest
import os
from os import path
import sys

from .. import main
from .. import tokens
from .. import xml_helper as x

class TestMain(unittest.TestCase):


    def answers(self, file_to_parse, parsed_file, answer):
        main.Main().main(file_to_parse)
        file_result = os.getcwd() + parsed_file
        file_answer = os.getcwd() + answer
        xstr = ''
        gen_answ = x.XMLHelper.xml_tag(file_answer)
        row_no = 0
        for tag in x.XMLHelper.xml_tag(file_result):
             tag = tag.strip()
             row_no = row_no + 1
             if tag:
                 tag_answ = ""
                 while not tag_answ.strip(): # Enteriai
                     tag_answ = gen_answ.__next__().strip()
                 xstr += tag + '\n'
                 # print("TAG, TAG_ANSW 1", tag, tag_answ, len(tag), len(tag_answ), 'row_no', row_no)
                 # print(xstr)
                 self.assertEqual(tag, tag_answ)
        #
        gen_res = x.XMLHelper.xml_tag(file_result)
        row_no = 0
        for tag in x.XMLHelper.xml_tag(file_answer):
            # print("TAG", type(tag), len(tag))
            tag = tag.strip()
            row_no = row_no + 1
            if tag:
                tag_res = gen_res.__next__().strip()
                # print("tag, tag_answ 2", tag, '+', tag_res)
                self.assertEqual(tag, tag_res)


    def test_main_create_file(self):
        
        inst = main.Main()
        inst.main('Test.jack')
        f = os.getcwd() + "/tests/files/Test.xml"
        f1 = os.getcwd() + "/tests/files/TestT.xml"
        self.assertTrue(path.exists(f))
        self.assertTrue(path.exists(f1))

        inst.main('ManyFiles')
        f1 = os.getcwd() + "/tests/files/ManyFiles/T1.xml"
        f2 = os.getcwd() + "/tests/files/ManyFiles/T2.xml"
        f3 = os.getcwd() + "/tests/files/ManyFiles/T1T.xml"
        f4 = os.getcwd() + "/tests/files/ManyFiles/T2T.xml"
        self.assertTrue(path.exists(f1))
        self.assertTrue(path.exists(f2))
        self.assertTrue(path.exists(f3))
        self.assertTrue(path.exists(f4))

    def test_tokens(self):

        self.answers('Test.jack', "/tests/files/TestT.xml", "/tests/files/TestT_answ.xml")
        # self.answers('Tokens.jack', "/tests/files/TokensT.xml", "/tests/files/TokensT_answ.xml")
        # self.answers('Tokens1.jack', "/tests/files/Tokens1T.xml", "/tests/files/Tokens1T_answ.xml")

    # def test_tokens_main(self):

        # self.answers('Main.jack', "/tests/files/MainT.xml", "/tests/files/MainT_answ.xml")


    def test_tokens_main2(self):

        self.answers('Symbols.jack', "/tests/files/SymbolsT.xml", "/tests/files/SymbolsT_answ.xml")

    def test_tokens_square_tokens(self):

        self.answers('Square', "/tests/files/Square/SquareGameT.xml", "/tests/files/Square/SquareGameT_answ.xml")
        self.answers('Square', "/tests/files/Square/MainT.xml", "/tests/files/Square/MainT_answ.xml")
        self.answers('Square', "/tests/files/Square/SquareT.xml", "/tests/files/Square/SquareT_answ.xml")

    def test_compiler_class(self):

        self.answers('Class.jack',"/tests/files/Class.xml","/tests/files/Class_answ.xml")
        self.answers('ClassVar.jack', "/tests/files/ClassVar.xml", "/tests/files/ClassVar_answ.xml")

    def test_compiler_subroutine(self):

        self.answers('Subroutine_simple.jack', "/tests/files/Subroutine_simple.xml", "/tests/files/Subroutine_simple_answ.xml")
        self.answers('Subroutine.jack',"/tests/files/Subroutine.xml","/tests/files/Subroutine_answ.xml")

    def test_compiler_subroutine(self):

        self.answers('Subroutine_simple.jack', "/tests/files/Subroutine_simple.xml", "/tests/files/Subroutine_simple_answ.xml")
        self.answers('Subroutine.jack',"/tests/files/Subroutine.xml","/tests/files/Subroutine_answ.xml")

    def test_compiler_var_decl(self):

        self.answers('Var_dec.jack', "/tests/files/Var_dec.xml", "/tests/files/Var_dec_answ.xml")
        self.answers('Var_dec2.jack', "/tests/files/Var_dec2.xml", "/tests/files/Var_dec2_answ.xml")

    def test_compile_do(self):

        self.answers('Do.jack', "/tests/files/Do.xml", "/tests/files/Do_answ.xml")
        self.answers('Do2.jack', "/tests/files/Do2.xml", "/tests/files/Do2_answ.xml")

    def test_compile_if(self):

        self.answers('If.jack', "/tests/files/If.xml", "/tests/files/If_answ.xml")
        self.answers('If2.jack', "/tests/files/If2.xml", "/tests/files/If2_answ.xml")
        self.answers('If3.jack', "/tests/files/If3.xml", "/tests/files/If3_answ.xml")

    def test_compile_while(self):

        self.answers('While_simple.jack', "/tests/files/While_simple.xml", "/tests/files/While_simple_answ.xml")
        self.answers('While.jack', "/tests/files/While.xml", "/tests/files/While_answ.xml")

    def test_compile_square_less(self):

        self.answers('Square_less', "/tests/files/Square_less/SquareGame.xml", "/tests/files/Square_less/SquareGame_answ.xml")
        self.answers('Square_less', "/tests/files/Square_less/Main.xml", "/tests/files/Square_less/Main_answ.xml")
        self.answers('Square_less', "/tests/files/Square_less/Square.xml", "/tests/files/Square_less/Square_answ.xml")

    def test_compile_square(self):

        self.answers('Square', "/tests/files/Square/SquareGame.xml", "/tests/files/Square/SquareGame_answ.xml")
        self.answers('Square', "/tests/files/Square/Main.xml", "/tests/files/Square/Main_answ.xml")
        self.answers('Square/Square.jack', "/tests/files/Square/Square.xml", "/tests/files/Square/Square_answ.xml")

    def test_compile_term_urinary(self):

          self.answers('Unary0.jack', "/tests/files/Unary0.xml", "/tests/files/Unary0_answ.xml")
          self.answers('Unary1.jack', "/tests/files/Unary1.xml", "/tests/files/Unary1_answ.xml")
          self.answers('Unary2.jack', "/tests/files/Unary2.xml", "/tests/files/Unary2_answ.xml")
          self.answers('Unary3.jack', "/tests/files/Unary3.xml", "/tests/files/Unary3_answ.xml")

    def test_compile_array(self):

        self.answers('ArrayTest', "/tests/files/ArrayTest/Main.xml", "/tests/files/ArrayTest/Main_answ.xml")

