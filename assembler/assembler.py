# conda activate py3
# conda install netcdf4
# conda deactivate
# python -m pytest
# pytest -k  "debug"
# /tests/files/Add.asm
import sys
import os

PATH = "/tests/files/"
FILE = "Add.asm"
LABELS_MEMORY_START = 16

class SymbolTable():

    """
    symbolTable - all symbols in assembler program list with info how many instructions is above them
    Memory location - 16 bits
    Exmp: "'i' : '0000 0000 0000 000'"

    instructions_counter - Calculate how many instructions is in file, for labels parsing
    
    """

    symbolTable = {}
    instructions_counter = 0
    
    """
    By given line update how many instruction is in file
    Skip if line starts with (
    If starts with (, save how many instructions is

    {'i' : 0}
    {'sum' : 5}
    
    """

    def updateSymbolTable(line):
        if line and not line[0] == "(":
            SymbolTable.instructions_counter += 1
        if line[0] == '(':
            SymbolTable.symbolTable[line[1:-1]] = SymbolTable.instructions_counter
        # print('line', line, 'address', address, 'table', SymbolTable.symbolTable)
        return


class Code():

    """
    table - for allready parsed A commands addresses
    labels_counter - counts how many labels (xxx) is curently in ROM, starts from 16 bits
    """
    
    table = {}
    labels_counter = LABELS_MEMORY_START

    """
    Make table from fixed symbols and addresses
    """

    def get_predifined_symbols():
        table = {}
        table['SP'] = '0000000000000000'
        table['LCL'] = '0000000000000001'
        table['ARG'] = '0000000000000010'
        table['THIS'] = '0000000000000011'
        table['THAT'] = '0000000000000100'
        table['SCREEN'] = '0100000000000000'
        table['KBD'] = '0110000000000000'

        for i in range(15+1):
            r = 'R' + str(i)
            address = Code.get_address(i)
            table[r] = address

        return table


    """
    Make 16bit binary address from number
    """

    def get_address(number):
        b_n = bin(int(number))[2:]
        add_zero = ''
        for i in range(16-len(b_n)):
            add_zero = add_zero + '0'
        full_address = add_zero + b_n
        return full_address

    """
    Get parsed comp strin
    Returns the binary code 7 bits string of the comp
    """

    def get_comp(parsed_code):
        code = '0000000'
        if parsed_code == '0':
            code = '0101010'
        elif parsed_code == '1':
            code = '0111111'
        elif parsed_code == '-1':
            code = '0111010'
        elif parsed_code == 'D':
            code = '0001100'
        elif parsed_code == 'A':
            code = '0110000'
        elif parsed_code == '!D':
            code = '0001101'
        elif parsed_code == '!A':
            code = '0110001'
        elif parsed_code == '-D':
            code = '0001111'
        elif parsed_code == '-A':
            code = '0110011'
        elif parsed_code == 'D+1':
            code = '0011111'
        elif parsed_code == 'A+1':
            code = '0110111'
        elif parsed_code == 'D-1':
            code = '0001110'
        elif parsed_code == 'A-1':
            code = '0110010'
        elif parsed_code == 'D+A':
            code = '0000010'
        elif parsed_code == 'D-A':
            code = '0010011'
        elif parsed_code == 'A-D':
            code = '0000111'
        elif parsed_code == 'D&A':
            code = '0000000'
        elif parsed_code == 'D|A': #
            code = '0010101' 
        # when a=1
        elif parsed_code == 'M':
            code = '1110000'
        elif parsed_code == '!M':
            code = '1110001'
        elif parsed_code == '-M':
            code = '1110011'
        elif parsed_code == 'M+1':
            code = '1110111'
        elif parsed_code == 'M-1':
            code = '1110010'
        elif parsed_code == 'D+M': #
            code = '1000010'
        elif parsed_code == 'D-M':
            code = '1010011'
        elif parsed_code == 'M-D':
            code = '1000111'
        elif parsed_code == 'D&M':
            code = '1000000'
        elif parsed_code == 'D|M':
            code = '1010101'                            
        return code


    """
    Get parsed jump string
    Returns the binary code 3 bits string of the jump
    """

    def get_jump(parsed_code):
        code = '000'
        if parsed_code == 'JGT':
            code = '001'
        elif parsed_code == 'JEQ':
            code = '010'
        elif parsed_code == 'JGE':
            code = '011'
        elif parsed_code == 'JLT':
            code = '100'
        elif parsed_code == 'JNE':
            code = '101'
        elif parsed_code == 'JLE':
            code = '110'
        elif parsed_code == 'JMP':
            code = '111'    
        return code

    """
    Get parsed destination string
    Returns the binary code 3 bits string of the dest

    Exp. M - 001
    """

    def get_dest(parsed_code):
        code = '000'
        if parsed_code == 'M':
            code = '001'
        elif parsed_code == 'D':
            code = '010'
        elif parsed_code == 'MD':
            code = '011'
        elif parsed_code == 'A':
            code = '100'
        elif parsed_code == 'AM':
            code = '101'
        elif parsed_code == 'AD':
            code = '110'
        elif parsed_code == 'AMD':
            code = '111'      
        return code

    """
    Consume parsed dict
    Return binary code
    
    For A commands:
        If number, give address from number convert to 16 bit binary
        If line is @ string, give first address starting from 16 bit - 10000
        Update allready parsed symbols by given line and give them memory location
    For L commands:
        Give address by their realeted instruction counters

    Exp. {'commandType': 'C_command', 'dest': 'M', 'comp': '1', 'jump': False}
         1110 1111 1100 1000

         {'commandType': 'C_command', 'dest': 'M', 'comp': '0', 'jump': False}
         1110 10101 1000 1000

         {'commandType': 'C_command', 'dest': False, 'comp': '0', 'jump': 'JMP'}
         1110 1010 1000 0111


    """
    def get_code(parsed_dict):
        
        code = ''
        code_final = ''
        if parsed_dict['commandType'] == 'C_command':
            code = '111'
            code_d = 'dest' in parsed_dict and Code.get_dest(parsed_dict['dest'])
            code_c = 'comp' in parsed_dict and Code.get_comp(parsed_dict['comp'])
            code_j = 'jump' in parsed_dict and Code.get_jump(parsed_dict['jump'])
            if code_c:
                code = code + code_c
            if code_d:
                code = code + code_d
            if code_j:
                code = code + code_j
        elif parsed_dict['commandType'] == 'A_command':
            if parsed_dict['symbol'] not in Code.table:
                if parsed_dict['symbol'].isnumeric():
                    address = int(parsed_dict['symbol'])
                else:
                    address = Code.labels_counter
                    Code.labels_counter += 1
                code = Code.get_address(address)
                Code.table[parsed_dict['symbol']] = code
            else:
                code = Code.table[parsed_dict['symbol']]
        elif parsed_dict['commandType'] == 'L_command':
            address = SymbolTable.symbolTable[parsed_dict['symbol']]
            code = Code.get_address(address)
        if code:
            code_final = code + '\n' 
        return code_final


class Parser():
    
    """
    Consume assmebler command.
    Returns command components dictionary. In addition, removes spaces and comments

    Exp. @100 = {commandType: A_command, symbol: '100'}
         M=1  = {'commandType': 'C_command', 'dest': 'M', 'comp': '1', 'jump': False}
         (LOOP)  = {commandType: L_command, symbol: 'LOOP'}
    """
    
    def parse(command):

        parsed_command = {}
        # Empty, spaces, comment
        if not command or command[0] == ' ' or command[0] == '/' or command[0] == '\n':
            return parsed_command
        # Strip everything from space
        command = command.split(" ", 1)[0]
        if command[0] == '@':
            symbol = command[1:].rstrip()
            # if this command is allready in SymbolTable, it is Label type command
            if symbol not in SymbolTable.symbolTable:
                parsed_command['commandType'] = 'A_command'
                parsed_command['symbol'] = symbol
            else:
                parsed_command['commandType'] = 'L_command'
                parsed_command['symbol'] = symbol
        # It is label, which don;t generate binary code        
        elif command[0] == '(':
            parsed_command['commandType'] = 'L0_command'
            symbol = command.rstrip()[1:-1]
            parsed_command['symbol'] = symbol
        else:
            parsed_command['commandType'] = 'C_command'  
            if command[1] == '=' or command[2] == '=' or command[3] == '=':
                parsed_command["dest"] = command.split('=')[0]
                parsed_command["comp"] = command.split('=')[1]
                parsed_command["jump"] = False
            else:
                parsed_command["dest"] = False
                parsed_command["comp"] = command[0]
                parsed_command["jump"] = command[2:]
        return parsed_command


class Assembler():

    def reset():

        SymbolTable.symbolTable = {}
        SymbolTable.instructions_counter = 0
        Code.labels_counter = LABELS_MEMORY_START
        Code.table = Code.get_predifined_symbols()
        print("Reseting", Code.labels_counter)

    """ 
    Return path to open and realitive path to given file

    First check given file name in working directory, 
    if not, check in  testing dir
    else just get file example
    """

    def get_file_path(file_to_parse=False):
        
        # 1. Path in testing dir
        path = os.getcwd() + PATH
        file_to_open_t = path + FILE
        file_to_open = ''

        if file_to_parse:
            file_to_open_t = os.getcwd() + PATH + file_to_parse
            file_to_open_w = os.getcwd() + '/' + file_to_parse
        
        # if is file in working dir
        if file_to_parse and os.path.exists(file_to_open_w):
            file_to_open = file_to_open_w
            path = os.getcwd() + '/'
        # check if file is in testing dir    
        elif os.path.exists(file_to_open_t):
            file_to_open = file_to_open_t
        return file_to_open, path

    """ 
    Path to Assembly .asm file to parse
    Return binary file .hack
    """

    def main(file_to_parse=False):
        
        if file_to_parse:
            file_name_write = file_to_parse.split('.')[0] + ".hack"
        else:
            file_name_write = FILE.split('.')[0] + ".hack"

        file_to_open = Assembler.get_file_path(file_to_parse)[0]
        file_to_write = Assembler.get_file_path(file_to_parse)[1] + file_name_write
        
        # remove old file
        if os.path.exists(file_to_write):
            os.remove(file_to_write)
        # reset server for unit tests
        Assembler.reset()
        # First pass - go line by line and update Symbolic table
        try:
            with open(file_to_open) as f1:
                for line in f1:
                    ln = line.strip()
                    if ln and not ln[0] == '/':
                        SymbolTable.updateSymbolTable(ln)

        except IOError:
            print("Something wrong")

        # Second pass         
        try:
            # print("file to open", file_to_open, 'file_to_write', file_to_write)
            with open(file_to_open) as f:               
                for line in f:
                    ln = line.strip()
                    parsed_command = Parser.parse(ln)
                    if parsed_command:
                        code = Code.get_code(parsed_command)
                        with open(file_to_write, 'a') as fw:
                            fw.write(code)
        except IOError:
            print("No file")


if __name__ == "__main__":
    try:
        try:
            file_to_parse = sys.argv[1]
            Assembler.main(file_to_parse)
        except IndexError:
            Assembler.main()
    except TypeError:
        print("Vista, ijunk python3")      
    
