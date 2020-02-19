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
        self.assertEqual('1110101010001000', code)

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

    def test_symbol_table_basic(self):
        
        ass.SymbolTable.reset()
        ass.SymbolTable.update_counter('@i')
        ass.SymbolTable.updateSymbolTable('@i')
        address = ass.SymbolTable.symbolTable['i']
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(1, count)
        self.assertEqual('0000000000010000', address)

        ass.SymbolTable.update_counter('@sum')
        ass.SymbolTable.updateSymbolTable('@sum')
        address = ass.SymbolTable.symbolTable['sum']
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(2, count)
        self.assertEqual('0000000000010001', address)

    def test_symbol_table_1(self):

        ass.SymbolTable.reset()
        ass.SymbolTable.update_counter('@i')
        ass.SymbolTable.updateSymbolTable('@i')
        address = ass.SymbolTable.symbolTable['i']
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(1, count)
        self.assertEqual('0000000000010000', address)

        ass.SymbolTable.update_counter('M=1')
        ass.SymbolTable.updateSymbolTable('M=1')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(2, count)
        self.assertEqual(1, table_len)
        
        ass.SymbolTable.update_counter('@sum')
        ass.SymbolTable.updateSymbolTable('@sum')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        address = ass.SymbolTable.symbolTable['sum']
        self.assertEqual(3, count)
        self.assertEqual(2, table_len)
        self.assertEqual('0000000000010001', address)

        ass.SymbolTable.update_counter('M=0')
        ass.SymbolTable.updateSymbolTable('M=0')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(4, count)
        self.assertEqual(2, table_len)

        ass.SymbolTable.update_counter('(LOOP)')
        ass.SymbolTable.updateSymbolTable('(LOOP)')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        address = ass.SymbolTable.symbolTable['LOOP']
        self.assertEqual(4, count)
        self.assertEqual(3, table_len)
        self.assertEqual('0000000000000100', address) #decimal - 4

        ass.SymbolTable.update_counter('@i')
        ass.SymbolTable.updateSymbolTable('@i')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        address = ass.SymbolTable.symbolTable['i']
        self.assertEqual(5, count)
        self.assertEqual(3, table_len)
        self.assertEqual('0000000000010000', address)

        ass.SymbolTable.update_counter('D=M')
        ass.SymbolTable.updateSymbolTable('D=M')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(6, count)
        self.assertEqual(3, table_len)

        ass.SymbolTable.update_counter('@100')
        ass.SymbolTable.updateSymbolTable('@100')
        table_len = len(ass.SymbolTable.symbolTable)
        count = ass.SymbolTable.instructions_counter
        address = ass.SymbolTable.symbolTable['100']
        self.assertEqual(7, count)
        self.assertEqual(4, table_len)
        self.assertEqual('0000000001100100', address)

    def test_symbol_table_2(self):

        ass.SymbolTable.reset()
        ass.SymbolTable.instructions_counter = 18
        ass.SymbolTable.update_counter('(END)')
        ass.SymbolTable.updateSymbolTable('(END)')
        address = ass.SymbolTable.symbolTable['END']
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(18, count)
        self.assertEqual('0000000000010010', address)

        ass.SymbolTable.update_counter('@END')
        ass.SymbolTable.updateSymbolTable('@END')
        address = ass.SymbolTable.symbolTable['END']
        count = ass.SymbolTable.instructions_counter
        self.assertEqual(19, count)
        self.assertEqual('0000000000010010', address)
 
        # address = ass.SymbolTable.updateSymbolTable({'commandType': 'A_command', 'symbol': 'i'}, 0)
        # self.assertEqual('0000000000010000', address)

        # address = ass.SymbolTable.updateSymbolTable({'commandType': 'A_command', 'symbol': 'sum'}, 1)
        # self.assertEqual('0000000000010001', address)

    def test_get_address(self):
        address = ass.SymbolTable.get_address(0)
        self.assertEqual('0000000000000000', address)

        address = ass.SymbolTable.get_address(1)
        self.assertEqual('0000000000000001', address)

        address = ass.SymbolTable.get_address(2)
        self.assertEqual('0000000000000010', address)

        address = ass.SymbolTable.get_address(100)
        self.assertEqual('0000000001100100', address)

    def test_main_basic(self):

        ass.Assembler.main('A_instr.asm')
        file_result = os.getcwd() + "/tests/files/A_instr.hack"
        file_answer = os.getcwd() + "/tests/files/A_instr_answ.hack"
        f_result = open(file_result, 'r')
        f_answer = open(file_answer, 'r')

        lines_count = 0
        for line in f_result:
            lines_count += 1
        f_result.seek(0)    
        for i in range(lines_count):
            self.assertEqual(f_result.readline(), f_answer.readline())
        f_result.close()
        f_answer.close()

    def test_main_add(self):

        ass.Assembler.main('Add.asm')
        file_result = os.getcwd() + "/tests/files/Add.hack"
        file_answer = os.getcwd() + "/tests/files/Add_answ.hack"
        f_result = open(file_result, 'r')
        f_answer = open(file_answer, 'r')

        lines_count = 0
        for line in f_result:
            lines_count += 1
        f_result.seek(0)    
        for i in range(lines_count):
            self.assertEqual(f_result.readline(), f_answer.readline())
        f_result.close()
        f_answer.close()
           
    def test_main_max(self):

        ass.Assembler.main('Max.asm')
        file_result = os.getcwd() + "/tests/files/Max.hack"
        file_answer = os.getcwd() + "/tests/files/Max_answ.hack"
        f_result = open(file_result, 'r')
        f_answer = open(file_answer, 'r')

        lines_count = 0
        for line in f_result:
            lines_count += 1
        f_result.seek(0)    
        for i in range(lines_count):
            self.assertEqual(f_result.readline(), f_answer.readline())
        f_result.close()
        f_answer.close()

    def test_main_maxl(self):

        ass.Assembler.main('MaxL.asm')
        file_result = os.getcwd() + "/tests/files/MaxL.hack"
        file_answer = os.getcwd() + "/tests/files/MaxL_answ.hack"
        f_result = open(file_result, 'r')
        f_answer = open(file_answer, 'r')

        lines_count = 0
        for line in f_result:
            lines_count += 1
        f_result.seek(0)    
        for i in range(lines_count):
            print("lines_count", lines_count)
            self.assertEqual(f_result.readline(), f_answer.readline())
        f_result.close()
        f_answer.close()


if __name__ == '__main__':
    unittest.main()
