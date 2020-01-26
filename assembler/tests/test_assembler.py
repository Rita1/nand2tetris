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
        is_jump = 'jump' in com and not com['jump']

        self.assertTrue(is_type)
        self.assertTrue(is_dest)
        self.assertTrue(is_comp)
        self.assertTrue(is_jump)


if __name__ == '__main__':
    unittest.main()
