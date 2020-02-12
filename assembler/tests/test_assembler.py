import unittest
import os
from os import path
from .. import assembler as ass


class TestMyClass(unittest.TestCase):

    def test_main_create_file(self):

        ass.Assembler.main('A_instr.asm')
        f = os.getcwd() + "/tests/files/A_instr.hack"
        self.assertTrue(path.exists(f))

        ass.Assembler.main('sample.asm')
        f = os.getcwd() + "/sample.hack"
        self.assertTrue(path.exists(f)) 

    def test_parser_empty(self):
        com = ass.Parser.parse('')
        self.assertFalse(com)

        com = ass.Parser.parse('   ')
        self.assertFalse(com)

        com = ass.Parser.parse('// ')
        self.assertFalse(com)

    def test_parser_A_command(self):
        com = ass.Parser.parse('@100')
        is_type = 'commandType' in com and 'A_command' == com['commandType']
        is_symbol = 'symbol' in com and '100' == com['symbol']

        self.assertTrue(is_type)
        self.assertTrue(is_symbol)

        com = ass.Parser.parse('@sum')
        is_type = 'commandType' in com and 'A_command' == com['commandType']
        is_symbol = 'symbol' in com and 'sum' == com['symbol']

        self.assertTrue(is_type)
        self.assertTrue(is_symbol)
        
        com = ass.Parser.parse('@i')
        is_type = 'commandType' in com and 'A_command' == com['commandType']
        is_symbol = 'symbol' in com and 'i' == com['symbol']

        self.assertTrue(is_type)
        self.assertTrue(is_symbol)

    def test_parser_L_command(self):

        com = ass.Parser.parse('@END')
        is_type = 'commandType' in com and 'L_command' == com['commandType']
        is_symbol = 'symbol' in com and 'END' == com['symbol']

        self.assertTrue(is_type)
        self.assertTrue(is_symbol)

        com = ass.Parser.parse('@LOOP')
        is_type = 'commandType' in com and 'L_command' == com['commandType']
        is_symbol = 'symbol' in com and 'LOOP' == com['symbol']

        self.assertTrue(is_type)
        self.assertTrue(is_symbol)

    def test_parser_C_command(self):

        com = ass.Parser.parse('M=1')
        is_type = 'commandType' in com and 'C_command' == com['commandType']
        is_dest = 'dest' in com and 'M' == com['dest']
        is_comp = 'comp' in com and '1' == com['comp']
        is_jump = 'jump' and com['jump'] == False

        self.assertTrue(is_type)
        self.assertTrue(is_dest)
        self.assertTrue(is_comp)
        self.assertTrue(is_jump)

    def test_parser_C_command2(self):

        com = ass.Parser.parse('D;JGT')
        is_type = 'commandType' in com and 'C_command' == com['commandType']
        is_dest = 'dest' and com['dest'] == False
        is_comp = 'comp' in com and 'D' == com['comp']
        is_jump = 'jump' in com and 'JGT' == com['jump']

        self.assertTrue(is_type)
        self.assertTrue(is_dest)
        self.assertTrue(is_comp)
        self.assertTrue(is_jump)

    def test_parser_A_command3(self):

        com = ass.Parser.parse('@i')

        is_type = 'commandType' in com and 'A_command' == com['commandType']
        is_symbol = 'symbol' in com and 'i' == com['symbol']

        self.assertTrue(is_type)
        self.assertTrue(is_symbol)

    def test_parser_C_command4(self):

        com = ass.Parser.parse('0;JMP')
        is_type = 'commandType' in com and 'C_command' == com['commandType']
        is_dest = 'dest' and com['dest'] == False
        is_comp = 'comp' in com and '0' == com['comp']
        is_jump = 'jump' in com and 'JMP' == com['jump']

        self.assertTrue(is_type)
        self.assertTrue(is_dest)
        self.assertTrue(is_comp)
        self.assertTrue(is_jump)

    def test_code(self):

        code = ass.Code.get_code({'commandType': 'C_command', 'dest': 'M', 'comp': '1', 'jump': False})
        self.assertEqual('1110111111001000', code)

        code = ass.Code.get_code({'commandType': 'C_command', 'dest': 'M', 'comp': '0', 'jump': False})
        self.assertEqual('11101010110001000', code)

        code = ass.Code.get_code({'commandType': 'C_command', 'dest': False, 'comp': '0', 'jump': 'JMP'})
        self.assertEqual('1110101010000111', code)

    def test_dest(self):

        dest = ass.Code.get_dest(False)
        self.assertEqual('000', dest)

        dest = ass.Code.get_dest('M')
        self.assertEqual('001', dest)

        dest = ass.Code.get_dest('AM')
        self.assertEqual('101', dest)

    def test_jump(self):

        jump = ass.Code.get_jump(False)
        self.assertEqual('000', jump)

        jump = ass.Code.get_jump('JGT')
        self.assertEqual('001', jump)

        jump = ass.Code.get_jump('JLE')
        self.assertEqual('110', jump)

    def test_comp(self):

        comp = ass.Code.get_comp('0')
        self.assertEqual('0101010', comp)

        comp = ass.Code.get_comp('1')
        self.assertEqual('0111111', comp)

        comp = ass.Code.get_comp('D')
        self.assertEqual('0001100', comp)

        comp = ass.Code.get_comp('D+1')
        self.assertEqual('0011111', comp)

        comp = ass.Code.get_comp('M')
        self.assertEqual('1110000', comp)

        comp = ass.Code.get_comp('!M')
        self.assertEqual('1110001', comp)

        comp = ass.Code.get_comp('M+1')
        self.assertEqual('1110111', comp)

        comp = ass.Code.get_comp('D&M')
        self.assertEqual('1000000', comp)

        comp = ass.Code.get_comp('D&A')
        self.assertEqual('0000000', comp)

if __name__ == '__main__':
    unittest.main()
