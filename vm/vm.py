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
            
        w = WriteCode()    
        # reset server for unit tests
        self.reset(file_to_write, w)
        
        # print("to_parse, file_to_parse, file_to_write", to_parse, files_to_parse, file_to_write)
        for f in files_to_parse:
            
            # print("file_to_open", f)
            try:
                with open(f) as f1:
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
            # print("file_to_parse, exits?", file_to_parse, os.path.exists(file_to_open_w), os.getcwd())
            if file_to_parse and os.path.exists(file_to_open_w):
                file_to_open = file_to_open_w
                path = os.getcwd() + '/'
        # If directory
        else:
            # First try in testing dir
            path = os.getcwd() + PATH + file_to_parse
            # TODO check in working directory
        return file_to_open, path


    def reset(self, file_to_write, write_code):
        with open(file_to_write, 'a') as fw:
            code = write_code.write_init()
            fw.write(code)


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
            c = len(list_commands)
            if c > 1:
                command["arg1"] = list_commands[1]
            if c > 2:
                command["arg2"] = list_commands[2]
            # print("l_c", list_commands)
            if list_commands[0] == 'push':
                command["type"] = 'C_PUSH'
            elif list_commands[0] == 'pop':
                command["type"] = 'C_POP'
            elif list_commands[0] == 'label':
                command["type"] = 'C_LABEL'
            elif list_commands[0] == 'goto':
                command["type"] = 'C_GOTO'
            elif list_commands[0] == 'if-goto':
                command["type"] = 'C_IF'
            elif list_commands[0] == 'function':
                command["type"] = 'C_FUNCTION'
            elif list_commands[0] == 'return':
                command["type"] = 'C_RETURN'
            elif list_commands[0] == 'call':
                command["type"] = 'C_CALL'                    
            else:
                command["type"] = 'C_ARITHMETIC'
                command["arg1"] = ln
        return command


class WriteCode():

    
    "Functions counter"

    funct_c = 0
    
    """
    Write start assembly code to file start
    Return string with assembly
    
    Stack starts at @256
    First VM function stats at Sys.init
    
    """
    def write_init(self):
        code = ""
        code = "@256\nD=A\n@SP\nM=D\n"
        return code



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
        if c_type == "C_PUSH" or c_type == 'C_POP':
            code = self.push_pop(c_type, arg1, arg2, file_name)
        #    print("C_PUSH code", code)
        elif c_type  == "C_ARITHMETIC":
            code = self.aritmetic(c_type, arg1, arg2)

        with open(file_to_write, 'a') as fw:
            fw.write(code)

        return ""

    def push_pop(self, c_type, arg1, arg2, file_name):
        # print("Comand", c_type, arg1, arg2, "Pointer")
        
        code = ""
        base = '@' + arg2 + '\n' + 'D=A\n'
        # print("base0", base)
        if arg1 == 'pointer':
            if int(arg2) == 0:
                base = "@THIS\n"
            elif int(arg2) == 1:
                base = '@THAT\n'
            # print("Base pointer", base)   
        elif arg1 == 'static':
            
            f_name = os.path.split(file_name.name)[1][:-3]
            # print("file_name", f_name)
            base = "@" + str(f_name) + "." + arg2 + "\n"
            # base = "@"
            # print("base static", base)
        elif arg1 == "temp":
            base = '@R' + str (int (arg2) + 5) + '\n'
            # print("base temp", base)
        # print("c_type", c_type, "arg1", arg1, "arg2?", arg2, "base", base, "file_name")        
        if c_type == "C_PUSH":
            if arg1 == 'constant':
                return base + '@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            elif arg1 == 'temp' or arg1 == 'pointer' or arg1 == 'static':
                return base + 'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            elif arg1 == 'local':
                code = base + '@LCL\n'
            elif arg1 == 'argument':
                code = base + '@ARG\n'
            elif arg1 == 'this':
                code = base + '@THIS\n'
            elif arg1 == 'that':
                code = base + '@THAT\n'        
            code = code + 'A=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        if c_type == "C_POP":
            if arg1 == 'temp' or arg1 == 'pointer' or arg1 == 'static':
                return '@SP\nM=M-1\nA=M\nD=M\n' + base + 'M=D\n'
            elif arg1 == 'local':
                code = base + "@LCL\n"
            elif arg1 == 'argument':
                code = base + "@ARG\n"
            elif arg1 == 'this':
                code = base + '@THIS\n'
            elif arg1 == 'that':
                code = base + '@THAT\n'       
            code = code + "D=M+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"    
        return code

    def aritmetic(self, c_type, arg1, arg2):
        code = ""
        if arg1 == "add" or arg1 == "sub":
            code = "@SP\nM=M-1\nA=M\nD=M\nM=0\nA=A-1\n"
            if arg1 == "add":
                code = code + "D=D+M\nM=D\n"
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
            + "@SP\nA=M-1\nM=-1\n" + "@" + funct_name + "2\n" + "0;JMP\n" + "(" + funct_name + "1" + ")\n" \
            + "@SP\nA=M-1\nM=0\n" +  "(" + funct_name + "2" + ")\n" + "@SP\n"
        elif arg1 == "and" or arg1 == "or":
            arg1 = str(arg1)
            funct_name = arg1.upper() + str(self.funct_c) + "_"
            self.funct_c += 1

            code = "@SP\nM=M-1\nA=M\nD=M\nM=0\nA=A-1\n"
            if arg1 == "and":
                code = code + "M=D&M\n"
            else:
                code = code + "M=D|M\n"    
        # NOT 
        else:  
            arg1 = str(arg1)
            funct_name = arg1.upper() + str(self.funct_c) + "_"
            self.funct_c += 1

            code = "@SP\nA=M-1\nM=!M\n" 
        return code            



if __name__ == "__main__":
    inst = Main()
    try:
        to_parse = sys.argv[1]
        inst.main(to_parse)
    except TypeError:
        print("Vista, ijunk python3")      
    
