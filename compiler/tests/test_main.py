import unittest
import os
from os import path
import sys

from .. import main

class TestMain(unittest.TestCase):

    def answers(self, file_to_parse, parsed_file, answer):
        main.Main().main(file_to_parse)
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


    def test_main_create_file(self):
        
        inst = main.Main()
        inst.main('Test.jack')
        f = os.getcwd() + "/tests/files/Test.html"
        f1 = os.getcwd() + "/tests/files/TestT.html"
        self.assertTrue(path.exists(f))
        self.assertTrue(path.exists(f1))

        inst.main('ManyFiles')
        f1 = os.getcwd() + "/tests/files/ManyFiles/T1.html"
        f2 = os.getcwd() + "/tests/files/ManyFiles/T2.html"
        f3 = os.getcwd() + "/tests/files/ManyFiles/T1T.html"
        f4 = os.getcwd() + "/tests/files/ManyFiles/T2T.html"
        self.assertTrue(path.exists(f1))
        self.assertTrue(path.exists(f2))
        self.assertTrue(path.exists(f3))
        self.assertTrue(path.exists(f4))

    # def test_main_basic(self):
    #
    #     self.answers('Test.vm', "/tests/files/Test.asm", "/tests/files/Test_answ.asm")
    #     self.answers('Push.vm', "/tests/files/Push.asm", "/tests/files/Push_answ.asm")

