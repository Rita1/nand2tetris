
import sys
import os

PATH = "/tests/files/"

class Main():

    """ 
    Path to Virtual machine .jack file to parse or directory
    Return .html file
    """

    def main(self, to_parse):

        # Files to parse consists of file path to parse and file name to write
        files_to_parse = []
        # print("to_parse", to_parse, to_parse[-4:])
        # If file
        if to_parse[-4:] == "jack":

            for_parsing = self.get_files(to_parse)
            files_to_parse.append(for_parsing)

        # If directory
        else:
            get_path = self.get_file_path(to_parse)[1]
            to_check = os.listdir(get_path)
            for f in to_check:
                if f[-4:] == "jack":
                    new_p = to_parse + "/" + f
                    for_parsing = self.get_files(new_p)
                    files_to_parse.append(for_parsing)

        for f in files_to_parse:

            # reset server for unit tests
            self.reset(f[1], f[2])
            #
            try:
                # Read
                with open(f[0]) as f1:
                    for line in f1:
                        ln = Tokens.remove_comments(line)
                        with open(f[2], 'a') as fw:
                            fw.write(ln)
                    print("file_to_open", f)
                    # Write Tokens



                # Write compiled code
                with open(f[1], 'a') as fw:
                    fw.write("2")

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
        if file_to_parse[-4:] == "jack" or file_to_parse[-4:] == "html":
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
        return file_to_open, path


    """
    Generate 3 files paths for future: file_name.jack file, file_nameT.html file for tokens and file_name.html for compiled code
    
    Gets file to parse, returns list of 3 files
    """

    def get_files(self, to_parse):
        file_list = []
        file_to_open = self.get_file_path(to_parse)[0]
        to_tokens = to_parse[:-5] + "T.html"
        file_tokens = self.get_file_path(to_tokens)[0]
        to_write = to_parse[:-4] + "html"
        file_to_write = self.get_file_path(to_write)[0]
        file_list.append(file_to_open)
        file_list.append(file_to_write)
        file_list.append(file_tokens)
        return file_list

    """
    Reset script - delete old files, add <Token> tags
    """

    @staticmethod
    def reset(file_to_write, file_to_write_tokens):

        # remove old file
        if os.path.exists(file_to_write):
            os.remove(file_to_write)

        if os.path.exists(file_to_write_tokens):
            os.remove(file_to_write_tokens)

        with open(file_to_write_tokens, 'a') as fw:
            code = "<Tokens></Tokens>"
            fw.write(code)


class Tokens:

    """Reads Jack program input and output HTML tokenizer"""

    """
    Removes comments and spaces: // 
                    /* ... */
                    /** ... **/
    Gets string, returns string
    
    TODO
    """

    @staticmethod
    def remove_comments(line):

        return line


    """
    Change symbols to HTML allowed symbols
    From < - &lt
         > - &gt
         & - &amp
    
    TODO
    """

    def change_symbols(self, s):

        return s