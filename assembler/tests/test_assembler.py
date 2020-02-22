import unittest
import os
from os import path
from .. import assembler as ass
reset = ass.Assembler.reset
updateSymbolTable = ass.SymbolTable.updateSymbolTable
parse = ass.Parser.parse
get_code = ass.Code.get_code


class TestMyClass(unittest.TestCase):

    def answers(self, file_to_parse, parsed_file, answer):
        ass.Assembler.main(file_to_parse)
        file_result = os.getcwd() + parsed_file
        file_answer = os.getcwd() + answer
        f_result = open(file_result, 'r')
        f_answer = open(file_answer, 'r')

        for line in f_result:
            self.assertEqual(line, f_answer.readline())

        f_result.close()
        f_answer.close()

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

        com = ass.Parser.parse('(END)')
        is_type = 'commandType' in com and 'L0_command' == com['commandType']
        is_symbol = 'symbol' in com and 'END' == com['symbol']

        self.assertTrue(is_type)
        self.assertTrue(is_symbol)

        com = ass.Parser.parse('(LOOP)')
        is_type = 'commandType' in com and 'L0_command' == com['commandType']
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

    def test_parser_C_command3(self):

        com = ass.Parser.parse('D=M')
        is_type = 'commandType' in com and 'C_command' == com['commandType']
        is_dest = 'dest' and 'D' == com['dest']
        is_comp = 'comp' in com and 'M' == com['comp']
        is_jump = 'jump' and com['jump'] == False

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

    def test_parser_C_command5(self):

        com = ass.Parser.parse('AM=M-1')
        is_type = 'commandType' in com and 'C_command' == com['commandType']
        is_dest = 'dest' in com and 'AM' == com['dest']
        is_comp = 'comp' in com and 'M-1' == com['comp']
        is_jump = 'jump' and com['jump'] == False

        self.assertTrue(is_type)
        self.assertTrue(is_dest)
        self.assertTrue(is_comp)
        self.assertTrue(is_jump)    

    def test_code(self):

        code = ass.Code.get_code({'commandType': 'C_command', 'dest': 'M', 'comp': '1', 'jump': False})
        self.assertEqual('1110111111001000\n', code)

        code = ass.Code.get_code({'commandType': 'C_command', 'dest': 'M', 'comp': '0', 'jump': False})
        self.assertEqual('1110101010001000\n', code)

        code = ass.Code.get_code({'commandType': 'C_command', 'dest': False, 'comp': '0', 'jump': 'JMP'})
        self.assertEqual('1110101010000111\n', code)

        code = ass.Code.get_code({'commandType': 'C_command', 'dest': 'D', 'comp': 'M', 'jump': False})
        self.assertEqual('1111110000010000\n', code)

        code = ass.Code.get_code({'commandType': 'C_command', 'dest': 'AM', 'comp': 'M-1', 'jump': False})
        self.assertEqual('1111110010101000\n', code)

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

    def test_symbol_table_basic(self):
        
        reset()
        updateSymbolTable('@i')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(1, count)
        self.assertEqual(0, table_len)

        updateSymbolTable('@sum')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(2, count)
        self.assertEqual(0, table_len)

        updateSymbolTable('(LOOP)')
        table_len = len(ass.SymbolTable.symbolTable)
        count0 = ass.SymbolTable.instructions_counter
        count1 = ass.SymbolTable.symbolTable['LOOP']
        self.assertEqual(2, count0)
        self.assertEqual(1, table_len)
        self.assertEqual(2, count1)

        updateSymbolTable('@LOOP')
        table_len = len(ass.SymbolTable.symbolTable)
        count0 = ass.SymbolTable.instructions_counter
        count1 = ass.SymbolTable.symbolTable['LOOP']
        self.assertEqual(3, count0)
        self.assertEqual(1, table_len)
        self.assertEqual(2, count1)

    def test_symbol_table_1(self):

        reset()
        parsed_dict = parse('@i')
        address = get_code(parsed_dict)
        self.assertEqual('0000000000010000\n', address)

        parsed_dict = parse('@sum')
        address = get_code(parsed_dict)
        self.assertEqual('0000000000010001\n', address)
    
        # parsed_dict = parse('(LOOP)')
        # ass.SymbolTable.instructions_counter = 4
        # updateSymbolTable('(LOOP)')
        # address = get_code(parsed_dict)
        # self.assertEqual('0000000000000100\n', address)

        parsed_dict = parse('@100')
        address = get_code(parsed_dict)
        self.assertEqual('0000000001100100\n', address)

        parsed_dict = parse('@sum')
        address = get_code(parsed_dict)
        self.assertEqual('0000000000010001\n', address)        

    def test_get_address(self):
        address = ass.Code.get_address(0)
        self.assertEqual('0000000000000000', address)

        address = ass.Code.get_address(1)
        self.assertEqual('0000000000000001', address)

        address = ass.Code.get_address(2)
        self.assertEqual('0000000000000010', address)

        address = ass.Code.get_address(100)
        self.assertEqual('0000000001100100', address)

    def test_main_basic(self):
        self.answers('A_instr.asm', "/tests/files/A_instr.hack", "/tests/files/A_instr.hack")

    def test_main_add(self):
        self.answers('Add.asm', "/tests/files/Add.hack", "/tests/files/Add_answ.hack")

    def test_main_dm(self):
        self.answers('DM_instr.asm', "/tests/files/DM_instr.hack", "/tests/files/DM_instr_answ.hack")

    def test_main_am(self): #AM=M-1
        self.answers('AM_instr.asm', "/tests/files/AM_instr.hack", "/tests/files/AM_instr_answ.hack")    
           
    def test_main_max(self):
        self.answers('Max.asm', "/tests/files/Max.hack", "/tests/files/Max_answ.hack")

    def test_main_maxl(self):
        self.answers('MaxL.asm', "/tests/files/MaxL.hack", "/tests/files/MaxL_answ.hack")

    def test_predefined_table(self):
        
        t = ass.Code.get_predifined_symbols()

        self.assertEqual('0000000000000000', t['R0'])
        self.assertEqual('0000000000000001', t['R1'])
        self.assertEqual('0000000000001100', t['R12'])
        self.assertEqual('0000000000001111', t['R15'])

    def test_main_pong(self):
        
        self.answers('Pong.asm', "/tests/files/Pong.hack", "/tests/files/Pong_answ.hack")

    def test_main_rect(self):
        
        self.answers('Rect.asm', "/tests/files/Rect.hack", "/tests/files/Rect_answ.hack")   
        self.answers('RectL.asm', "/tests/files/RectL.hack", "/tests/files/RectL_answ.hack")   

if __name__ == '__main__':
    unittest.main()
