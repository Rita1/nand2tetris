import unittest
import os
from os import path
from .. import vm


class TestMain(unittest.TestCase):

    def answers(self, file_to_parse, parsed_file, answer):
        vm.Main().main(file_to_parse)
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
        
        inst = vm.Main()
        inst.main('Test.vm')
        f = os.getcwd() + "/tests/files/Test.asm"
        self.assertTrue(path.exists(f))

        inst.main('ManyFiles')
        f = os.getcwd() + "/tests/files/ManyFiles/ManyFiles.asm"
        self.assertTrue(path.exists(f))

    def test_main_basic(self):

        self.answers('Test.vm', "/tests/files/Test.asm", "/tests/files/Test_answ.asm")
        self.answers('Push.vm', "/tests/files/Push.asm", "/tests/files/Push_answ.asm")


    def test_main_arit(self):

        self.answers('Add.vm', "/tests/files/Add.asm", "/tests/files/Add_answ.asm")
        self.answers('Sub.vm', "/tests/files/Sub.asm", "/tests/files/Sub_answ.asm")
        self.answers('Neg.vm', "/tests/files/Neg.asm", "/tests/files/Neg_answ.asm")

    def test_main_compare(self):

        self.answers('Eq.vm', "/tests/files/Eq.asm", "/tests/files/Eq_answ.asm")
        self.answers('Gt.vm', "/tests/files/Gt.asm", "/tests/files/Gt_answ.asm")
        self.answers('Lt.vm', "/tests/files/Lt.asm", "/tests/files/Lt_answ.asm")

    def test_main_logic(self):

        self.answers('And.vm', "/tests/files/And.asm", "/tests/files/And_answ.asm")
        self.answers('Or.vm', "/tests/files/Or.asm", "/tests/files/Or_answ.asm")
        self.answers('Not.vm', "/tests/files/Not.asm", "/tests/files/Not_answ.asm")
    
    def test_pop_basic(self):

        self.answers('Pop.vm', "/tests/files/Pop.asm", "/tests/files/Pop_answ.asm")
        self.answers('Pop2.vm', "/tests/files/Pop2.asm", "/tests/files/Pop2_answ.asm")
        self.answers('BasicTest.vm', "/tests/files/BasicTest.asm", "/tests/files/Pop2_answ.asm")

    def test_pop_temp(self):

        self.answers('Pop_temp.vm', "/tests/files/Pop_temp.asm", "/tests/files/Pop_temp_answ.asm")
        

    
    def test_parse_other(self):
        # Empty
        c = vm.Parse().parse("")
        self.assertFalse(c)
        # Space
        c = vm.Parse().parse("  ")
        self.assertFalse(c)
        # Comments
        c = vm.Parse().parse("// Test")
        self.assertFalse(c)

    def test_parse_push(self):

        c = vm.Parse().parse("push constant 7")
        # print("c", c)
        is_type = 'type' in c and 'C_PUSH' == c["type"]
        is_arg1 = 'arg1' in c and 'constant' == c["arg1"]
        is_arg2 = 'arg2' in c and '7' == c["arg2"]

        self.assertTrue(is_type)
        self.assertTrue(is_arg1)
        self.assertTrue(is_arg2)
        
        # Push with comments, spaces
        c = vm.Parse().parse("push constant 8 // Testas")

        is_type = 'type' in c and 'C_PUSH' == c["type"]
        is_arg1 = 'arg1' in c and 'constant' == c["arg1"]
        is_arg2 = 'arg2' in c and '8' == c["arg2"]

        self.assertTrue(is_type)
        self.assertTrue(is_arg1)
        self.assertTrue(is_arg2)
        
        c = vm.Parse().parse("push constant 8     // Testas")

        is_type = 'type' in c and 'C_PUSH' == c["type"]
        is_arg1 = 'arg1' in c and 'constant' == c["arg1"]
        is_arg2 = 'arg2' in c and '8' == c["arg2"]

        self.assertTrue(is_type)
        self.assertTrue(is_arg1)
        self.assertTrue(is_arg2)

    
    def test_parse_pop(self):

        c = vm.Parse().parse("pop local 0")
        # print("c", c)
        is_type = 'type' in c and 'C_POP' == c["type"]
        is_arg1 = 'arg1' in c and 'local' == c["arg1"]
        is_arg2 = 'arg2' in c and '0' == c["arg2"]

        self.assertTrue(is_type)
        self.assertTrue(is_arg1)
        self.assertTrue(is_arg2)
            

    def test_parse_arit(self):
        
        c = vm.Parse().parse("add")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'add' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

        c = vm.Parse().parse("sub")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'sub' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

        c = vm.Parse().parse("neg")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'neg' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

        c = vm.Parse().parse("eq")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'eq' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

        c = vm.Parse().parse("gt")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'gt' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

        c = vm.Parse().parse("lt")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'lt' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

        c = vm.Parse().parse("and")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'and' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

        c = vm.Parse().parse("or")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'or' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

        c = vm.Parse().parse("not")

        is_type = 'type' in c and 'C_ARITHMETIC' == c["type"]
        is_arg1 = 'arg1' in c and 'not' == c["arg1"]
        self.assertTrue(is_type)
        self.assertTrue(is_arg1)

