import unittest
import os
from os import path
import sys

from .. import main
from .. import tokens

class TestTokens(unittest.TestCase):


    def test_tokens_comments(self):

        Tokens = tokens.Tokenizer()
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

        Tokens = tokens.Tokenizer()
        line = """/**"""
        after_remove = Tokens.remove_comments(line)
        self.assertEqual("", after_remove)

        l1 = """* Implements the Square Dance game."""
        after_remove = Tokens.remove_comments(l1)
        self.assertEqual("", after_remove)

        l2 = """*/"""
        after_remove = Tokens.remove_comments(l2)
        self.assertEqual("", after_remove)

        l3 = """class SquareGame {"""
        after_remove = Tokens.remove_comments(l3)
        self.assertEqual("class SquareGame {", after_remove)

        Tokens = tokens.Tokenizer()
        l1 = """/** Computes the average of a sequence of integers. */"""
        after_remove = Tokens.remove_comments(l1)
        self.assertEqual("", after_remove)

        l2 = """class Main {"""
        after_remove = Tokens.remove_comments(l2)
        self.assertEqual("class Main {", after_remove)

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

        line = "function void main() {"
        todo = Tokens().make_todo_list(line)
        answ = ['function', 'void', 'main', '(', ')', '{']
        self.assertEqual(todo, answ)

        line = """("HOW MANY.NUMBERS? ")"""
        todo = Tokens().make_todo_list(line)
        answ = ['(', '"HOW MANY.NUMBERS? "',')']
        self.assertEqual(todo, answ)

        line = """let length = Keyboard.readInt("HOW MANY NUMBERS? ");"""
        todo = Tokens().make_todo_list(line)
        answ = ['let', 'length', '=', 'Keyboard', '.', 'readInt', '(', '"HOW MANY NUMBERS? "', ')', ';']
        self.assertEqual(todo, answ)

    def test_todo_2(self):

        Tokens = tokens.Tokenizer
        line = """while (i < length) {"""
        todo = Tokens().make_todo_list(line)
        answ = ['while', '(', 'i', '<', 'length',')', '{']
        self.assertEqual(answ, todo)

        Tokens = tokens.Tokenizer
        line = """if (direction = 1) { do square.moveUp(); }"""
        todo = Tokens().make_todo_list(line)
        answ = ['if', '(', 'direction', '=', '1',')', '{', 'do', 'square', '.', 'moveUp','(',')',';','}']
        self.assertEqual(answ, todo)


    def test_tokens_split_by_string(self):

        Tokens = tokens.Tokenizer

        line = """"""
        got = Tokens().split_by_string(line, [])
        self.assertEqual([''], got)

        line = "Test"
        got = Tokens().split_by_string(line, [])
        self.assertEqual(['Test'], got)

        line = 'Test "'
        got = Tokens().split_by_string(line, [])
        self.assertEqual(['Test "'], got)

        line = """let length = Keyboard.readInt("HOW MANY NUMBERS? ");"""
        got = Tokens().split_by_string(line, [])
        answ = ['let length = Keyboard.readInt(', '"HOW MANY NUMBERS? "', ');']
        self.assertEqual(answ, got)

        line = """let length = Keyboard.readInt("HOW MANY NUMBERS? "); Keyboard.readInt("HOW MANY NUMBERS? ");"""
        got = Tokens().split_by_string(line, [])
        answ = ['let length = Keyboard.readInt(', '"HOW MANY NUMBERS? "', '); Keyboard.readInt(','"HOW MANY NUMBERS? "',');']
        self.assertEqual(answ, got)


    def test_tokens_is_string(self):
        Tokens = tokens.Tokenizer

        line = ''
        self.assertFalse(Tokens.is_string(line))

        line = "Test"
        self.assertFalse(Tokens.is_string(line))

        line = 'readInt("HOW MANY NUMBERS? ");'
        self.assertTrue(Tokens.is_string(line))

        line = ''"HOW MANY NUMBERS?"''
        self.assertFalse(Tokens.is_string(line))

    def test_tokens_coord(self):
        Tokens = tokens.Tokenizer

        line = ''
        self.assertEqual((-1,-1), Tokens.string_coord(line))

        line = 'readInt("HOW MANY NUMBERS? ");'
        self.assertEqual((8,27), Tokens.string_coord(line))

    def test_tokens_symbol(self):
        Tokens = tokens.Tokenizer

        line = '"HOW MANY(NUMBERS? "'
        self.assertFalse(Tokens.is_symbol(line))

        line = ';'
        self.assertFalse(Tokens.is_symbol(line))

        line = 'Keyboard.readInt'
        self.assertTrue(Tokens.is_symbol(line))

        line = 'Keyboard.readInt('
        self.assertTrue(Tokens.is_symbol(line))


    def test_tokens_split_symbol(self):
        Tokens = tokens.Tokenizer()
        #
        # line = []
        # self.assertEqual([],Tokens.split_by_symbol(line, []))

        line = ['"HOW MANY NUMBERS? "']
        self.assertEqual(['"HOW MANY NUMBERS? "'], Tokens.split_by_symbol(line, []))

        line = ['let', 'Keyboard.readInt']
        todo = Tokens.split_by_symbol(line, [])
        answ = ['let','Keyboard', '.', 'readInt']
        self.assertEqual(answ, todo)

        line = ['var', 'int', 'i,', 'a;']
        todo = Tokens.split_by_symbol(line, [])
        answ = ['var', 'int', 'i', ',', 'a', ';']
        self.assertEqual(answ, todo)

        line = ['let', 'length', '=', 'Keyboard.readInt(', '"HOW MANY NUMBERS? "', ');']
        todo = Tokens.split_by_symbol(line, [])
        answ = ['let', 'length', '=', 'Keyboard', '.', 'readInt', '(', '"HOW MANY NUMBERS? "', ')', ';']
        print("Answ", answ)
        print("Todo", todo)
        self.assertEqual(answ, todo)

        line = [');']
        todo = Tokens.split_by_symbol(line, [])
        answ = [')', ';']
        self.assertEqual(answ, todo)


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
        answ = [Tokens.Token(tokenType='keyword', keyWord='var'), Tokens.Token(tokenType='keyword', keyWord='int'), Tokens.Token(tokenType='identifier', identifier='a'),
                Tokens.Token(tokenType='symbol', symbol=';')]
        self.assertEqual(len(t_list), 4)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])
    #
        line = "var int a, b;"
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='var'), Tokens.Token(tokenType='keyword', keyWord='int'), Tokens.Token(tokenType='identifier', identifier='a'),
                Tokens.Token(tokenType='symbol', symbol=','),
                Tokens.Token(tokenType='identifier', identifier='b'),
                Tokens.Token(tokenType='symbol', symbol=';')]
        self.assertEqual(len(t_list), 6)
        print("T_LIST ****************************", t_list)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])

    def test_tokens_ident_funct(self):

        Tokens = tokens.Tokenizer
        line = "function void main() {"
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='function'), Tokens.Token(tokenType='keyword', keyWord='void'),
            Tokens.Token(tokenType='identifier', identifier='main'),
            Tokens.Token(tokenType='symbol', symbol='('), Tokens.Token(tokenType='symbol', symbol=')'),
            Tokens.Token(tokenType='symbol', symbol='{')]
        self.assertEqual(len(t_list), 6)
        print("T_LIST ****************************", t_list)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])

    def test_tokens_ident_let(self):

        Tokens = tokens.Tokenizer
        line = "let i = 0;"
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='let'),
            Tokens.Token(tokenType='identifier', identifier='i'),
            Tokens.Token(tokenType='symbol', symbol='='),
            Tokens.Token(tokenType='integerConstant', integerConstant=0),
            Tokens.Token(tokenType='symbol', symbol=';')]
        self.assertEqual(len(t_list), 5)
        print("T_LIST ****************************", t_list)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])

    def test_tokens_ident_var2(self):

        Tokens = tokens.Tokenizer
        line = "var Array a;"
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='var'),
            Tokens.Token(tokenType='identifier', identifier='Array'),
            Tokens.Token(tokenType='identifier', identifier='a'),
            Tokens.Token(tokenType='symbol', symbol=';')]
        self.assertEqual(len(t_list), 4)
        print("T_LIST ****************************", t_list)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])

    def test_tokens_subroutine(self):

        Tokens = tokens.Tokenizer
        line = """let length = Keyboard.readInt("HOW MANY NUMBERS? ");"""
        t_list = Tokens().make_tokens(line)
        answ = [Tokens.Token(tokenType='keyword', keyWord='let'),
            Tokens.Token(tokenType='identifier', identifier='length'),
            Tokens.Token(tokenType='symbol', symbol='='),
            Tokens.Token(tokenType='identifier', identifier='Keyboard'),
            Tokens.Token(tokenType='symbol', symbol='.'),
            Tokens.Token(tokenType='identifier', identifier='readInt'),
            Tokens.Token(tokenType='symbol', symbol='('),
            Tokens.Token(tokenType='stringConstant', stringConstant='HOW MANY NUMBERS? '),
            Tokens.Token(tokenType='symbol', symbol=')'),
            Tokens.Token(tokenType='symbol', symbol=';')]
        self.assertEqual(len(t_list), 10)
        print("T_LIST ****************************", t_list)
        for i in range(len(t_list)):
            self.assertEquals(t_list[i], answ[i])

    # def test_tokens_subroutine2(self):
    #
    #     Tokens = tokens.Tokenizer
    #     line = """do Screen.drawRectangle(-y+x);"""
    #     t_list = Tokens().make_tokens(line)
    #     line = """do Screen.drawRectangle(x, y, x, -y);"""
    #     t_list = Tokens().make_tokens(line)
    #     answ = [Tokens.Token(tokenType='keyword', keyWord='do'),
    #         Tokens.Token(tokenType='identifier', identifier='Screen'),
    #         Tokens.Token(tokenType='symbol', symbol='.'),
    #         Tokens.Token(tokenType='identifier', identifier='drawRectangle'),
    #         Tokens.Token(tokenType='symbol', symbol='('),
    #         Tokens.Token(tokenType='identifier', identifier='x'),
    #         Tokens.Token(tokenType='symbol', symbol=','),
    #         Tokens.Token(tokenType='identifier', identifier='y'),
    #         Tokens.Token(tokenType='symbol', symbol=','),
    #         Tokens.Token(tokenType='identifier', identifier='x'),
    #         Tokens.Token(tokenType='symbol', symbol=','),
    #         Tokens.Token(tokenType='identifier', identifier='-y'),
    #         Tokens.Token(tokenType='symbol', symbol=','),
    #         Tokens.Token(tokenType='symbol', symbol=')'),
    #         Tokens.Token(tokenType='symbol', symbol=';')]
    #     self.assertEqual(len(t_list), 15)
    #     print("T_LIST ****************************", t_list)
    #     for i in range(len(t_list)):
    #         self.assertEquals(t_list[i], answ[i])

