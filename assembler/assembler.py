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

class Code():

    """
    Get parsed comp string
    Returns the binary code 7 bits string of the comp

    !!!
    """

    def get_comp(parsed_code):
        return '0000000'


    """
    Get parsed jump string
    Returns the binary code 3 bits string of the jump

    !!!
    """

    def get_jump(parsed_code):
        return '000'

    """
    Get parsed destination string
    Returns the binary code 3 bits string of the dest

    Exp. M - 001
    !!!
    """

    def get_dest(parsed_code):
        return '000'

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
        code = ''
        code_d = 'dest' in parsed_dict and Code.get_dest(parsed_dict['dest'])
        code_c = 'comp' in parsed_dict and Code.get_comp(parsed_dict['comp'])
        code_j = 'jump' in parsed_dict and Code.get_jump(parsed_dict['jump'])
        if code_d:
            code = code + code_d
        if code_c:
            code = code + code_c
        if code_j:
            code = code + code_j
        print("dest", code_d, "comp", code_c, "jump", code_c, "binary code", code)
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
            
        try:
            print("file to open", file_to_open, 'file_to_write', file_to_write)
            with open(file_to_open) as f:
                for line in f:
                    parsed_command = Parser.parse(line)
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
    
