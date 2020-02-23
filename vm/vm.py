# conda activate py3
# conda install netcdf4
# conda deactivate
# python -m pytest
# pytest -k  "debug"

import sys
import os

PATH = "/tests/files/"
FILE = "Test.vm"

class Main():

    """ 
    Path to Virtual machine .vm file to parse
    Return assembly file .asm
    """

    def main(self, file_to_parse=False):
        
        if file_to_parse:
            file_name_write = file_to_parse.split('.')[0] + ".asm"
        else:
            file_name_write = FILE.split('.')[0] + ".asm"

        file_to_open = self.get_file_path(file_to_parse)[0]
        file_to_write = self.get_file_path(file_to_parse)[1] + file_name_write
        
        # remove old file
        if os.path.exists(file_to_write):
            os.remove(file_to_write)
        # reset server for unit tests
        self.reset()
        # First pass
        try:
            with open(file_to_open) as f1:
                for line in f1:
                    ln = line.strip()
                    print("ln")
                    with open(file_to_write, 'a') as fw:
                            fw.write(ln)
        except IOError:
            print("Something wrong")


    """ 
    Return path to open and realitive path to given file

    First check given file name in working directory, 
    if not, check in  testing dir
    else just get file example
    """

    def get_file_path(self, file_to_parse=False):
        
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


    def reset(self):
        pass


if __name__ == "__main__":
    inst = Main()
    try:
        try:
            file_to_parse = sys.argv[1]
            inst.main(file_to_parse)
        except IndexError:
            inst.main()
    except TypeError:
        print("Vista, ijunk python3")      
    
