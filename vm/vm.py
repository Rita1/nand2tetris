# conda activate py3
# conda install netcdf4
# conda deactivate
# python -m pytest
# pytest -k  "debug"

import sys
import os

PATH = "/tests/files/"
INIT = "@256\nD=A\n@SP\nM=D\n"

class Main():

    """ 
    Path to Virtual machine .vm file to parse or directory
    Return assembly file .asm
    """

    def main(self, to_parse):
        
        files_to_parse = []
        if to_parse[-3:] == ".vm":
            file_to_open = self.get_file_path(to_parse)[0]
            files_to_parse.append(file_to_open)
            file_name_write = to_parse.split('.')[0] + ".asm"
        else:
            get_path = self.get_file_path(to_parse)[1]
            to_check = os.listdir(get_path)
            for f in to_check:
                if f[-3:] == ".vm":
                    new_p = to_parse + "/" + f
                    file_to_open = self.get_file_path(new_p)[0]
                    files_to_parse.append(file_to_open)
            file_name_write = "/" + to_parse + ".asm"

        file_to_write = self.get_file_path(to_parse)[1] + file_name_write
        # remove old file
        if os.path.exists(file_to_write):
            os.remove(file_to_write)
        # reset server for unit tests
        self.reset(file_to_write)
        w = WriteCode()
        # print("to_parse, file_to_parse, file_to_write", to_parse, files_to_parse, file_to_write)
        for f in files_to_parse:
            
            # print("file_to_open", f)
            try:
                with open(file_to_open) as f1:
                    for line in f1:
                        ln = Parse().parse(line)
                        # print("ln")
                        if ln:
                            w.code(f1, ln, file_to_write)
                        
            except IOError:
                print("File or directory is missing")

    """ 
    Return path's to files or directories
    If file, return full file path to open and directory to file
        First check in testing dir, if not in working dir
    if directory, only full dir path

    """

    def get_file_path(self, file_to_parse):
        
        path = ''
        file_to_open = ''
        # If file:
        if file_to_parse[-3:] == ".vm":
            # 1. Path in testing dir
            path = os.getcwd() + PATH
            file_to_open = os.getcwd() + PATH + file_to_parse
            file_to_open_w = os.getcwd() + '/' + file_to_parse
            # 2. File is in working dir
            print("file_to_parse, exits?", file_to_parse, os.path.exists(file_to_open_w), os.getcwd())
            if file_to_parse and os.path.exists(file_to_open_w):
                file_to_open = file_to_open_w
                path = os.getcwd() + '/'
        # If directory
        else:
            # First try in testing dir
            path = os.getcwd() + PATH + file_to_parse
            # TODO check in working directory
        return file_to_open, path


    def reset(self, file_to_write):
        with open(file_to_write, 'a') as fw:
            fw.write(INIT)


class Parse():

    """
    To parse given line to type and arguments
    
    Consume string and return dict of parsed commands
    
    type - selection from:
        C_ARITHMETIC
        C_PUSH
        C_POP
        C_LABEL
        C_GOTO
        C_IF
        C_FUNCTION
        C_RETURN
        C_CALL
    arg1 - string
    arg2 - string

    Exp.: 'push constant 7' = {'type': 'C_PUSH', 'arg1': 'constant', 'arg2': '7'}
          'add' = {'type': 'C_ARITHMETIC', 'arg1': 'add'}
    """

    def parse(self, line):

        command = {}
        # Strip everything from space or "//"

        ln = line.split("//", 1)[0]
        ln = ln.strip()
        if ln:
            list_commands = ln.split(" ")
            print("l_c", list_commands)
            if list_commands[0] == 'push':
                command["type"] = 'C_PUSH'
                command["arg1"] = list_commands[1]
                command["arg2"] = list_commands[2]
            else:
                command["type"] = 'C_ARITHMETIC'
                command["arg1"] = ln
        return command


class WriteCode():


    "Functions counter"

    funct_c = 0


    """
    Parse given dict and file_name to assembly code and write to file
    
    String file_name - to change symbols names in assembly

    Exp.: {'type': 'C_PUSH', 'arg1': 'constant', 'arg2': 7} - #Stack'as nuo 256 , SP - 256
    @7 // Constant 7
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1

    {'type': 'C_ARITHMETIC', 'arg1': 'add'}
    @SP // Add - 258
    M=M-1 // 257
    A=M
    D=M
    M=0
    A=A-1 // 256
    D=D+M
    M=D


    """

    def code(self, file_name, parsed_dict, file_to_write):
        code = ''
        c_type = parsed_dict["type"]
        arg1 = parsed_dict["arg1"]
        arg2 = "arg2" in parsed_dict and parsed_dict["arg2"]
        if c_type == "C_PUSH":
           code = '@' + arg2 + '\n'
           code = code + 'D=A\n@SP\nA=M\nM=D\n@SP\n@M=M+1\n'
        #    print("C_PUSH code", code)
        elif c_type  == "C_ARITHMETIC":
            if arg1 == "add" or arg1 == "sub":
                code = "@SP\nM=M+1\n@SP\nM=M-1\nA=M\nD=M\nM=0\nA=A-1\n"
                if arg1 == "add":
                    code = code + "D=D+M\n"
                else:
                    code = code + "D=M-D\n"
                code = code + "M=D\n"
            elif arg1 == "neg":
                code = "@SP\nA=M-1\nD=M\n@SP\nD=A-D\nA=M-1\nM=D\n"    
            elif arg1 == "eq" or arg1 == "lt" or arg1 == "gt":
                arg1 = str(arg1)
                funct_name = arg1.upper() + str(self.funct_c) + "_"
                self.funct_c += 1

                code = "@SP\nM=M-1\nA=M\nD=M\nM=0\nA=A-1\nD=D-M\n"
                code = code + "@" + funct_name + "0\n"
                if arg1 == "eq":
                    code = code + "D;JEQ\n"
                elif arg1 == "lt":
                    code = code + "D;JGT\n"
                else:
                    code = code + "D;JLT\n"
                code = code + "@" + funct_name + "1\n" + "0;JMP\n" + "(" + funct_name + "0" + ")\n" \
                + "@SP\nA=M-1\nM=0\n" + "@" + funct_name + "2\n" + "0;JMP\n" + "(" + funct_name + "1" + ")\n" \
                + "@SP\nA=M-1\nM=-1\n" +  "(" + funct_name + "2" + ")\n" + "@SP\n"
            elif arg1 == "and" or arg1 == "or":
                arg1 = str(arg1)
                funct_name = arg1.upper() + str(self.funct_c) + "_"
                self.funct_c += 1

                code = "@SP\nM=M-1\nA=M\nD=M\nM=0\nA=A-1\nD=D+M\n"
                if arg1 == "and":
                    code = code + "@2\nD=D-A\n"
                code = code + "@" + funct_name + "0\n" + "D;JEQ\n" \
                + "@" + funct_name + "1\n" + "0;JMP\n" + "(" + funct_name + "0" + ")\n" \
                + "@SP\nA=M-1\n"
                if arg1 == "and":
                    code = code + "M=1\n"
                elif arg1 == "or":
                    code = code + "M=0\n"
                code = code + "@" + funct_name + "2\n" + "0;JMP\n" + "(" + funct_name + "1" + ")\n" \
                + "@SP\nA=M-1\n"
                if arg1 == "and":
                    code = code + "M=0\n"
                elif arg1 == "or":
                    code = code + "M=1\n"
                code = code + "(" + funct_name + "2" + ")\n" + "@SP\n"
            else:
                arg1 = str(arg1)
                funct_name = arg1.upper() + str(self.funct_c) + "_"
                self.funct_c += 1

                code = "@SP\nM=M-1\nD=M\n" + "@" + funct_name + "0\n" + "D;JEQ\n" \
                + "@" + funct_name + "1\n" + "0;JMP\n" + "(" + funct_name + "0" + ")\n" \
                + "@SP\nA=M-1\nM=1\n" + "@" + funct_name + "2\n" + "0;JMP\n" + "(" + funct_name + "1" + ")\n" \
                + "@SP\nA=M-1\nM=0\n" + "(" + funct_name + "2" + ")\n" + "@SP\n"


        with open(file_to_write, 'a') as fw:
            fw.write(code)

        return ""       

if __name__ == "__main__":
    inst = Main()
    try:
        to_parse = sys.argv[1]
        inst.main(to_parse)
    except TypeError:
        print("Vista, ijunk python3")      
    
