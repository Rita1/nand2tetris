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


class Parser():

    """
    Consume assmebler command.
    Returns command components dictionary. In addition, removes spaces and comments

    Exp. @100 = {commandType: A_command, symbol: '100'}
         M=1  = {'commandType': 'C_command', 'dest': 'M', 'comp': '1', 'jump': False}
         @LOOP  = {commandType: L_command, symbol: 'LOOP'}
    """
    
    def parse(command):
        return {'commandType': 'C_command', 'dest': 'M', 'comp': '1', 'jump': False}


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
                    print(parsed_command)
                    with open(file_to_write, 'a') as fw:
                        fw.write(line)
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
    
