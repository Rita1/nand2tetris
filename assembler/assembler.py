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
    symbolTable - all symbols in assembler program list with their memory location
    Memory location - 16 bits
    Exmp: "'i' : '0000 0000 0000 000'"

    instructions_counter - Calculate how many instructions is in file, for symbols parsing
    """

    symbolTable = {}
    instructions_counter = 0
    labels_counter = LABELS_MEMORY_START
    
    def __init__(self, name, is_male):
        self.symbolTable = SymbolTable.get_predifined_symbols()
        
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
            address = SymbolTable.get_address(i)
            table[r] = address

        return table

    

    def reset():
        SymbolTable.symbolTable = SymbolTable.get_predifined_symbols()
        SymbolTable.instructions_counter = 0
        SymbolTable.labels_counter = LABELS_MEMORY_START

    """
    By given line update how many instruction is in file
    Skip if line starts with (
    """

    def update_counter(line):
        if line and not line[0] == "(":
            SymbolTable.instructions_counter += 1
        return
    
    """
    Make 16bit binary address from number
    """

    def get_address(number):
        # print("number", number)
        b_n = bin(int(number))[2:]
        # print("b_n", "len", b_n, len(b_n))
        add_zero = ''
        for i in range(16-len(b_n)):
            add_zero = add_zero + '0'
        full_address = add_zero + b_n
        # print("add_zero","full_address", add_zero, full_address)
        return full_address

    """
    Update Symbol Table by given line and give them memory location
    If line is @ string, give first address starting from 16 bit - 10000
    If number, give address from number convert to 16 bit binary
    If starts with (, give address from counter

    {'i' : '0000 0000 0001 0000'}
    {'sum' : '0000 0000 0001 0001'}
    
    """

    def updateSymbolTable(line):
        # print('line', line)
        address = ''
        if line[0] == '@':
            ln = line[1:]
            if ln.isnumeric():
                address = SymbolTable.get_address(ln)
                SymbolTable.symbolTable[ln] = address
            elif ln not in SymbolTable.symbolTable:
                address = SymbolTable.get_address(SymbolTable.labels_counter)
                SymbolTable.labels_counter += 1              
                SymbolTable.symbolTable[ln] = address
        if line[0] == '(':
            address = SymbolTable.get_address(SymbolTable.instructions_counter)
            SymbolTable.symbolTable[line[1:-1]] = address
        # print('line', line, 'address', address, 'table', SymbolTable.symbolTable)
        return


class Code():

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

    Exp. {'commandType': 'C_command', 'dest': 'M', 'comp': '1', 'jump': False}
         1110 1111 1100 1000

         {'commandType': 'C_command', 'dest': 'M', 'comp': '0', 'jump': False}
         1110 10101 1000 1000

         {'commandType': 'C_command', 'dest': False, 'comp': '0', 'jump': 'JMP'}
         1110 1010 1000 0111


    """
    def get_code(parsed_dict):
        print("parsed_dict", parsed_dict)
        code = ''
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
            print("dest", code_d, "comp", code_c, "jump", code_j, "binary code", code)
        else:
            print("ST", SymbolTable.symbolTable)
            label = parsed_dict['symbol']
            code = SymbolTable.symbolTable[label]  
        
        return code


class Parser():
    
    """
    Consume assmebler command.
    Returns command components dictionary. In addition, removes spaces and comments

    Exp. @100 = {commandType: A_command, symbol: '100'}
         M=1  = {'commandType': 'C_command', 'dest': 'M', 'comp': '1', 'jump': False}
         @LOOP  = {commandType: L_command, symbol: 'LOOP'}
    """
    
    def parse(command):

        parsed_command = {}
        # Empty, spaces, comment
        if not command or command[0] == ' ' or command[0] == '/' or command[0] == '\n':
            return parsed_command
        if command[0] == '@':
            if command[1:].isupper():
                parsed_command['commandType'] = 'L_command'
            else:
                parsed_command['commandType'] = 'A_command'
        else:
            parsed_command['commandType'] = 'C_command'  
        if parsed_command['commandType'] == 'A_command' or parsed_command['commandType'] == 'L_command':
            
            symbol = command[1:].rstrip()
            parsed_command['symbol'] = symbol
        else:
            if command[1] == '=':
                parsed_command["dest"] = command[0]
                parsed_command["comp"] = command[2:]
                parsed_command["jump"] = False
            else:
                parsed_command["dest"] = False
                parsed_command["comp"] = command[0]
                parsed_command["jump"] = command[2:]

        print("parsed_command", parsed_command)
        return parsed_command


class Assembler():

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
        SymbolTable.reset()
        # First pass - go line by line and update memory_counter + Symbolic table
        try:
            with open(file_to_open) as f1:
                for line in f1:
                    ln = line.strip()
                    # print("my ln", ln)
                    # print(not bool(ln))
                    if ln and not ln[0] == '/':
                        # print("ln", ln)
                        SymbolTable.update_counter(ln)
                        SymbolTable.updateSymbolTable(ln)

        except IOError:
            print("Something wrong")

        # Second pass         
        try:
            print("file to open", file_to_open, 'file_to_write', file_to_write)
            with open(file_to_open) as f:               
                for line in f:
                    ln = line.strip()
                    parsed_command = Parser.parse(ln)
                    if parsed_command:
                        code = Code.get_code(parsed_command) + '\n'
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
    
