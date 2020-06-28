import unittest
import os
from os import path
import sys

from .. import main
from .. import tokens

class TestMain(unittest.TestCase):


# veikia tik UTF-8 XML'ams

    def xml_tag(self, file_name):

        between = False # arba reiksme tarp tag'u
        found = False   # arba tag'as
        with open(file_name, 'r') as f:
            while True: # kol nesibaige failas
                tag = ""
                c = f.read(1)
                if not c:
                    break
                tag = tag + c
                if c == "<":
                    found = True
                    between = False
                while between: #kai baigsis reiksme tarp tag'u
                    where_i_am = f.tell() # issisaugom, reikes pagrizti atgal, kad < nuskaitytume dar karta
                    c = f.read(1)
                    if c == "<":
                        f.seek(where_i_am) # griztam per simboli
                        between = False
                        break
                    if not c:
                        break
                    tag = tag + c
                while found: # kol rasim pabaiga
                    c = f.read(1)
                    tag = tag + c
                    if c == ">":
                        found = False
                        between = True
                        break
                yield tag


    def answers(self, file_to_parse, parsed_file, answer):
        main.Main().main(file_to_parse)
        file_result = os.getcwd() + parsed_file
        file_answer = os.getcwd() + answer

        gen_answ = self.xml_tag(file_answer)
        for tag in self.xml_tag(file_result):
             if tag.strip():
                 tag_answ = ""
                 while not tag_answ.strip(): # Enteriai
                     tag_answ = gen_answ.__next__().strip()
                 self.assertEqual(tag, tag_answ)
        #
        gen_res = self.xml_tag(file_result)
        for tag in self.xml_tag(file_answer):
            # print("TAG", type(tag), len(tag))
            tag = tag.strip()
            if tag:
                tag_res = gen_res.__next__()
                # print("tag, tag_answ", tag, tag_res)
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

    def test_tokens_comments(self):

        Tokens = tokens.Tokenizer
        self.assertEqual("test", Tokens.remove_comments("test   "))
        self.assertEqual("test", Tokens.remove_comments("  test   "))
        self.assertEqual("test", Tokens.remove_comments("     test"))

        self.assertEqual("test and test", Tokens.remove_comments("test and test //Comment "))
        self.assertEqual("class Test", Tokens.remove_comments("class Test /* Comment */ "))
        self.assertEqual("", Tokens.remove_comments("/** Disposes this fraction. */ "))

        self.assertEqual("", Tokens.remove_comments("""// File name: projects/09/Average/Main.jack"""))
        self.assertEqual("class Main {", Tokens.remove_comments(""" class Main {"""))

        self.assertEqual("do Output.printInt(sum / length);", Tokens.remove_comments("do Output.printInt(sum / length);"))
        # self.assertEqual("do Output.printInt(sum / length);", Tokens.remove_comments("do Output.printInt(sum / length);"))
        self.assertEqual("""do Output.printString("The average is ");""",
                         Tokens.remove_comments("""do Output.printString("The average is ");"""))

        self.assertEqual("let a = Array.new(length);", Tokens.remove_comments("let a = Array.new(length); // constructs the array"))
        self.assertEqual("let r = a - (b * (a / b));", Tokens.remove_comments("let r = a - (b * (a / b));  // r = remainder of the integer division a/b"))


    def test_tokens(self):

        self.answers('Test.jack', "/tests/files/TestT.xml", "/tests/files/TestT_answ.xml")
        self.answers('Tokens.jack', "/tests/files/TokensT.xml", "/tests/files/TokensT_answ.xml")
        self.answers('Tokens1.jack', "/tests/files/Tokens1T.xml", "/tests/files/Tokens1T_answ.xml")

    def test_tokens_main(self):

        self.answers('Main.jack', "/tests/files/MainT.xml", "/tests/files/MainT_answ.xml")

    def test_tokens_todo(self):

        Tokens = tokens.Tokenizer
        line = ""
        todo = Tokens().make_todo_list(line)
        self.assertFalse(todo)

        line = "var int i, a;"
        todo = Tokens().make_todo_list(line)
        answ = ['var', 'int', 'i', ',', 'a', ';']
        self.assertEqual(todo, answ)

        line = "class"
        todo = Tokens().make_todo_list(line)
        answ = ['class']
        self.assertEqual(todo, answ)

    def test_tokens_list_simple(self):

        Tokens = tokens.Tokenizer
        line = ""
        t_list = Tokens().make_tokens(line)
        self.assertFalse(t_list)

        line = "class"
        t_list = Tokens().make_tokens(line)
        anws = Tokens.Token(tokenType='keyword', keyWord='class')
        self.assertEqual(len(t_list), 1)
        self.assertEqual(t_list[0], anws)
    #
        line = "class {"
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='class'), Tokens.Token(tokenType='symbol', symbol='{')]
        self.assertEqual(len(t_list), 2)
        # print("T_list", t_list, "ANSW", anws)
        for i in range(len(t_list)):
            # print(i)
            self.assertEquals(t_list[i], answ[i])

    def test_tokens_list_identifier(self):

        Tokens = tokens.Tokenizer
        line = "class Main {"
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='class'), Tokens.Token(tokenType='identifier', identifier='Main'), Tokens.Token(tokenType='symbol', symbol='{')]
        self.assertEqual(len(t_list), 3)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])
    #
        line = "var int a;"
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='var'), Tokens.Token(tokenType='keyword', keyWord='integer'), Tokens.Token(tokenType='identifier', identifier='a'),
                Tokens.Token(tokenType='symbol', symbol=';')]
        self.assertEqual(len(t_list), 4)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])
    #
        line = "var int a, b;"
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='var'), Tokens.Token(tokenType='keyword', keyWord='integer'), Tokens.Token(tokenType='identifier', identifier='a'),
                Tokens.Token(tokenType='symbol', symbol=','),
                Tokens.Token(tokenType='identifier', identifier='b'),
                Tokens.Token(tokenType='symbol', symbol=';')]
        self.assertEqual(len(t_list), 6)
        print("T_LIST ****************************", t_list)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])
